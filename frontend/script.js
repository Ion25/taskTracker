/**
 * TaskTracker Frontend JavaScript
 * Maneja toda la lógica del cliente incluyendo CRUD, SSE logs y clima
 */

class TaskTracker {
    constructor() {
        this.tasks = [];
        this.currentFilter = 'todas';
        this.editingTaskId = null;
        this.weatherUpdateInterval = null;
        
        // URLs dinámicas de la API (funciona tanto en localhost como en producción)
        const currentHost = window.location.origin;
        this.API_BASE = `${currentHost}/api`;
        
        this.initializeApp();
    }
    
    async initializeApp() {
        console.log('Inicializando TaskTracker...');
        
        // Configurar event listeners
        this.setupEventListeners();
        
        // Cargar datos iniciales
        await this.loadInitialData();
        
        // Configurar actualizaciones automáticas
        this.setupAutoUpdates();
        
        console.log('TaskTracker inicializado correctamente');
    }
    
    setupEventListeners() {
        // Formulario de tareas
        document.getElementById('addTaskBtn').addEventListener('click', () => this.handleTaskSubmit());
        document.getElementById('cancelEditBtn').addEventListener('click', () => this.cancelEdit());
        
        // Enter en el input de título
        document.getElementById('taskTitle').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleTaskSubmit();
        });
        
        // Filtros
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.setFilter(e.target.dataset.filter));
        });
        
        // Botón de documentación
        document.getElementById('docsBtn').addEventListener('click', () => this.openDocs());
        
        // Modal de confirmación
        document.getElementById('confirmYes').addEventListener('click', () => this.confirmAction());
        document.getElementById('confirmNo').addEventListener('click', () => this.closeConfirmModal());
    }
    
    async loadInitialData() {
        try {
            // Cargar tareas
            await this.loadTasks();
            
            // Cargar estadísticas
            await this.updateStats();
            
            // Cargar clima
            await this.updateWeather();
            
        } catch (error) {
            console.error('Error cargando datos iniciales:', error);
        }
    }
    
    setupAutoUpdates() {
        // Actualizar clima cada 5 minutos
        this.weatherUpdateInterval = setInterval(() => {
            this.updateWeather();
        }, 5 * 60 * 1000);
        
        // Actualizar estadísticas cada 30 segundos
        setInterval(() => {
            this.updateStats();
        }, 30 * 1000);
    }
    
    // === GESTIÓN DE TAREAS ===
    
    async loadTasks() {
        console.log('🔄 Cargando tareas...');
        try {
            const response = await fetch(`${this.API_BASE}/tasks`);
            console.log('📡 Respuesta del servidor:', response.status);
            if (!response.ok) throw new Error(`Error ${response.status}`);
            
            this.tasks = await response.json();
            console.log('📋 Tareas cargadas:', this.tasks.length, this.tasks);
            this.renderTasks();
            console.log('✅ Tareas renderizadas correctamente');
            
        } catch (error) {
            console.error('❌ Error cargando tareas:', error);
        }
    }
    
    async handleTaskSubmit() {
        const title = document.getElementById('taskTitle').value.trim();
        const description = document.getElementById('taskDescription').value.trim();
        
        if (!title) {
            alert('Por favor ingresa un título para la tarea');
            return;
        }
        
        try {
            if (this.editingTaskId) {
                await this.updateTask(this.editingTaskId, { titulo: title, descripcion: description });
            } else {
                await this.createTask({ titulo: title, descripcion: description });
            }
            
            // Limpiar formulario
            this.clearForm();
            
        } catch (error) {
            console.error('Error en operación de tarea:', error);
        }
    }
    
    async createTask(taskData) {
        const response = await fetch(`${this.API_BASE}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(taskData)
        });
        
        if (!response.ok) throw new Error(`Error ${response.status}`);
        
        const newTask = await response.json();
        this.tasks.unshift(newTask);
        this.renderTasks();
        this.updateStats();
    }
    
    async updateTask(taskId, updates) {
        const response = await fetch(`${this.API_BASE}/tasks/${taskId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updates)
        });
        
        if (!response.ok) throw new Error(`Error ${response.status}`);
        
        const updatedTask = await response.json();
        const index = this.tasks.findIndex(task => task.id === taskId);
        if (index !== -1) {
            this.tasks[index] = updatedTask;
            this.renderTasks();
            this.updateStats();
        }
    }
    
    async deleteTask(taskId) {
        const response = await fetch(`${this.API_BASE}/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error(`Error ${response.status}`);
        
        this.tasks = this.tasks.filter(task => task.id !== taskId);
        this.renderTasks();
        this.updateStats();
    }
    
    async toggleTaskStatus(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        if (!task) return;
        
        const newStatus = task.estado === 'pendiente' ? 'completada' : 'pendiente';
        await this.updateTask(taskId, { estado: newStatus });
    }
    
    // === RENDERIZADO ===
    
    renderTasks() {
        const tasksList = document.getElementById('tasksList');
        const emptyState = document.getElementById('emptyState');
        
        // Filtrar tareas
        let filteredTasks = this.tasks;
        if (this.currentFilter !== 'todas') {
            filteredTasks = this.tasks.filter(task => task.estado === this.currentFilter);
        }
        
        if (filteredTasks.length === 0) {
            tasksList.style.display = 'none';
            emptyState.style.display = 'block';
            return;
        }
        
        tasksList.style.display = 'block';
        emptyState.style.display = 'none';
        
        tasksList.innerHTML = filteredTasks.map(task => this.createTaskHTML(task)).join('');
        
        // Agregar event listeners a los elementos de tarea
        tasksList.querySelectorAll('.task-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const taskId = parseInt(e.target.dataset.taskId);
                this.toggleTaskStatus(taskId);
            });
        });
        
        tasksList.querySelectorAll('.task-btn.edit').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const taskId = parseInt(e.target.dataset.taskId);
                this.editTask(taskId);
            });
        });
        
        tasksList.querySelectorAll('.task-btn.delete').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const taskId = parseInt(e.target.dataset.taskId);
                const taskTitle = e.target.dataset.taskTitle;
                this.confirmDelete(taskId, taskTitle);
            });
        });
    }
    
    createTaskHTML(task) {
        const date = new Date(task.fecha_creacion);
        const formattedDate = date.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        return `
            <div class="task-item ${task.estado}">
                <input type="checkbox" 
                       class="task-checkbox" 
                       data-task-id="${task.id}"
                       ${task.estado === 'completada' ? 'checked' : ''}>
                <div class="task-content">
                    <div class="task-title ${task.estado}">${this.escapeHtml(task.titulo)}</div>
                    ${task.descripcion ? `<div class="task-description">${this.escapeHtml(task.descripcion)}</div>` : ''}
                    <div class="task-meta">
                        <span class="task-date">Creada: ${formattedDate}</span>
                        <div class="task-actions">
                            <button class="task-btn edit" 
                                    data-task-id="${task.id}">
                                Editar
                            </button>
                            <button class="task-btn delete" 
                                    data-task-id="${task.id}"
                                    data-task-title="${this.escapeHtml(task.titulo)}">
                                Eliminar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    // === FILTROS ===
    
    setFilter(filter) {
        this.currentFilter = filter;
        
        // Actualizar botones activos
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.filter === filter);
        });
        
        this.renderTasks();
    }
    
    // === EDICIÓN DE TAREAS ===
    
    editTask(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        if (!task) return;
        
        // Llenar formulario con datos de la tarea
        document.getElementById('taskTitle').value = task.titulo;
        document.getElementById('taskDescription').value = task.descripcion || '';
        
        // Cambiar estado del formulario
        this.editingTaskId = taskId;
        document.getElementById('addTaskBtn').textContent = 'Actualizar Tarea';
        document.getElementById('cancelEditBtn').style.display = 'inline-block';
        document.querySelector('.task-form h3').textContent = 'Editar Tarea';
        
        // Scroll al formulario
        document.getElementById('taskForm').scrollIntoView({ behavior: 'smooth' });
    }
    
    cancelEdit() {
        this.editingTaskId = null;
        this.clearForm();
    }
    
    clearForm() {
        document.getElementById('taskTitle').value = '';
        document.getElementById('taskDescription').value = '';
        document.getElementById('addTaskBtn').textContent = 'Agregar Tarea';
        document.getElementById('cancelEditBtn').style.display = 'none';
        document.querySelector('.task-form h3').textContent = 'Nueva Tarea';
        this.editingTaskId = null;
    }
    
    // === CONFIRMACIÓN DE ELIMINACIÓN ===
    
    confirmDelete(taskId, taskTitle) {
        this.pendingDeleteId = taskId;
        document.getElementById('confirmMessage').textContent = 
            `¿Estás seguro de que quieres eliminar la tarea "${taskTitle}"?`;
        document.getElementById('confirmModal').style.display = 'flex';
    }
    
    async confirmAction() {
        if (this.pendingDeleteId) {
            await this.deleteTask(this.pendingDeleteId);
            this.pendingDeleteId = null;
        }
        this.closeConfirmModal();
    }
    
    closeConfirmModal() {
        document.getElementById('confirmModal').style.display = 'none';
        this.pendingDeleteId = null;
    }
    
    // === DOCUMENTACIÓN ===
    
    openDocs() {
        const currentHost = window.location.origin;
        window.open(`${currentHost}/docs`, '_blank');
    }
    
    // === ESTADÍSTICAS ===
    
    async updateStats() {
        try {
            const response = await fetch(`${this.API_BASE}/stats`);
            if (!response.ok) throw new Error(`Error ${response.status}`);
            
            const stats = await response.json();
            
            document.getElementById('statTotal').textContent = stats.total;
            document.getElementById('statPendientes').textContent = stats.pendientes;
            document.getElementById('statCompletadas').textContent = stats.completadas;
            
        } catch (error) {
            console.error('Error actualizando estadísticas:', error);
        }
    }
    
    // === CLIMA ===
    
    async updateWeather() {
        try {
            // Intentar obtener ubicación del usuario
            let city = 'Lima'; // Fallback por defecto
            
            if (navigator.geolocation) {
                try {
                    const position = await this.getCurrentPosition();
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    
                    // Usar coordenadas en lugar de nombre de ciudad
                    const response = await fetch(`${this.API_BASE}/weather?lat=${lat}&lon=${lon}`);
                    if (!response.ok) throw new Error(`Error ${response.status}`);
                    
                    const weather = await response.json();
                    this.renderWeather(weather);
                    return;
                    
                } catch (geoError) {
                    console.log('Geolocalización no disponible, usando Lima como fallback');
                }
            }
            
            // Fallback: usar Lima
            const response = await fetch(`${this.API_BASE}/weather?city=${city}`);
            if (!response.ok) throw new Error(`Error ${response.status}`);
            
            const weather = await response.json();
            this.renderWeather(weather);
            
        } catch (error) {
            console.error('Error actualizando clima:', error);
            this.renderWeatherError();
        }
    }
    
    // Promisificar geolocation
    getCurrentPosition(options = {}) {
        return new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject, {
                timeout: 10000,
                enableHighAccuracy: true,
                maximumAge: 300000, // Cache por 5 minutos
                ...options
            });
        });
    }
    
    renderWeather(weather) {
        const widget = document.getElementById('weatherWidget');
        
        if (weather.success) {
            widget.classList.remove('weather-error');
            document.getElementById('weatherCity').textContent = weather.ciudad;
            document.getElementById('weatherTemp').textContent = `${weather.temperatura}°C`;
            document.getElementById('weatherDesc').textContent = weather.descripcion;
            document.getElementById('weatherUpdate').textContent = 
                `Última actualización: ${weather.ultima_actualizacion}`;
            
            // Usar el icono emoji directamente de la API
            document.getElementById('weatherIcon').textContent = weather.icono;
            
            // Mostrar fuente de datos
            let sourceText = weather.descripcion;
            if (weather.source) {
                if (weather.source === "wttr.in (gratis)") {
                    sourceText += " (API gratuita)";
                } else if (weather.source === "Demo") {
                    sourceText += " (Demo)";
                } else {
                    sourceText += ` (${weather.source})`;
                }
            }
            document.getElementById('weatherDesc').textContent = sourceText;
                
        } else {
            this.renderWeatherError(weather.error);
        }
    }
    
    renderWeatherError(errorMsg = 'Error de conexión') {
        const widget = document.getElementById('weatherWidget');
        widget.classList.add('weather-error');
        
        document.getElementById('weatherCity').textContent = 'Error';
        document.getElementById('weatherTemp').textContent = '--°C';
        document.getElementById('weatherDesc').textContent = errorMsg;
        document.getElementById('weatherUpdate').textContent = 
            `Error: ${new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}`;
        document.getElementById('weatherIcon').textContent = '⚠️';
    }
    
    // === UTILIDADES ===
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Cleanup cuando se cierra la página
    disconnect() {
        if (this.weatherUpdateInterval) {
            clearInterval(this.weatherUpdateInterval);
        }
    }
}

// Inicializar la aplicación cuando se carga la página
document.addEventListener('DOMContentLoaded', () => {
    window.taskTracker = new TaskTracker();
});

// Limpiar conexiones cuando se cierra la página
window.addEventListener('beforeunload', () => {
    if (window.taskTracker) {
        window.taskTracker.disconnect();
    }
});