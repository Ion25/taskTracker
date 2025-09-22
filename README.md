# TaskTracker

> Sistema completo de gestión de tareas con API REST y widget de clima en tiempo real.

[![Live Demo](https://img.shields.io/badge/Demo-Live-brightgreen)](https://tu-tasktracker.onrender.com/app) 
[![API Docs](https://img.shields.io/badge/API-Swagger-orange)](https://tu-tasktracker.onrender.com/docs)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://hub.docker.com)

## Stack Técnico

**Backend**
- **FastAPI** - Framework web moderno para APIs REST
- **SQLAlchemy** - ORM para gestión de base de datos
- **SQLite** - Base de datos ligera para persistencia
- **Pydantic** - Validación de datos y serialización
- **Uvicorn** - Servidor ASGI de alto rendimiento

**Frontend**
- **Vanilla JavaScript** - JavaScript puro sin frameworks
- **CSS3** - Diseño responsive y moderno
- **HTML5** - Estructura semántica

**DevOps & Deploy**
- **Docker** - Containerización multiplataforma
- **Render/Koyeb** - Deploy gratuito en la nube
- **GitHub Actions** - CI/CD (opcional)

## Características

- **CRUD Completo** - Crear, leer, actualizar y eliminar tareas
- **API REST** - Endpoints documentados con Swagger/OpenAPI
- **Base de Datos** - Persistencia con SQLAlchemy ORM
- **Widget de Clima** - Integración con APIs externas (WeatherAPI, OpenWeatherMap, wttr.in)
- **Estadísticas en Tiempo Real** - Dashboard con métricas de tareas
- **Interfaz Moderna** - UI responsive sin dependencias externas
- **Containerizado** - Listo para deploy con Docker
- **Documentación Automática** - Swagger UI integrado

## Demo en Vivo

**Aplicación:** [https://tu-tasktracker.onrender.com/app](https://tu-tasktracker.onrender.com/app)  
**API Docs:** [https://tu-tasktracker.onrender.com/docs](https://tu-tasktracker.onrender.com/docs)

> **Nota:** Actualiza estas URLs después del deploy en Render o Koyeb

## Inicio Rápido

### Opción 1: Docker (Recomendado - Más Fácil)

> ✅ **Render Ready:** Este Dockerfile está optimizado y probado para Render.com

```bash
# 1. Clonar repositorio
git clone https://github.com/tuusuario/tasktracker.git
cd tasktracker

# 2. Levantar con Docker
docker-compose up -d

# 3. Verificar que esté funcionando
docker-compose ps
```

**Abrir aplicación:** http://localhost:8000/app  
**Ver API docs:** http://localhost:8000/docs

```bash
# Para detener
docker-compose down

# Para probar build individual (como lo hace Render)
docker build -t tasktracker .
docker run -p 8000:8000 tasktracker
```

### Opción 2: Instalación Local

#### Prerrequisitos
- Python 3.10+ instalado
- Git instalado

```bash
# 1. Clonar repositorio
git clone https://github.com/tuusuario/tasktracker.git
cd tasktracker

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno virtual
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Crear directorio de base de datos
mkdir -p db

# 6. Levantar el servidor
./run_tasktracker.sh

# Alternativamente, manual:
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Abrir aplicación:** http://localhost:8000/app

#### Detener el servidor local
```bash
# Si usaste el script
./stop_tasktracker.sh

# O buscar y matar el proceso
ps aux | grep uvicorn
kill [PID]
```

### Opción 3: Solo Backend (Para desarrolladores)

```bash
# Después de los pasos 1-4 de la opción local
cd backend
python main.py

# O con uvicorn directamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**API REST disponible en:** http://localhost:8000/api/  
**Documentación:** http://localhost:8000/docs

## Estructura del Proyecto

```
tasktracker/
├── backend/
│   ├── main.py          # Aplicación FastAPI
│   ├── models.py        # Modelos SQLAlchemy
│   ├── routes.py        # Endpoints API REST
│   └── weather.py       # Integración APIs clima
├── frontend/
│   ├── index.html       # Interfaz principal
│   ├── styles.css       # Estilos CSS
│   └── script.js        # Lógica JavaScript
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Local development
├── render.yaml          # Render.com deploy config
├── .koyeb/config.yaml   # Koyeb.com deploy config
└── requirements.txt    # Python dependencies
```

## API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/tasks` | Obtener todas las tareas |
| `POST` | `/api/tasks` | Crear nueva tarea |
| `GET` | `/api/tasks/{id}` | Obtener tarea específica |
| `PUT` | `/api/tasks/{id}` | Actualizar tarea |
| `DELETE` | `/api/tasks/{id}` | Eliminar tarea |
| `GET` | `/api/stats` | Estadísticas de tareas |
| `GET` | `/api/weather` | Datos del clima actual |

**Documentación completa:** `/docs` (Swagger UI)

