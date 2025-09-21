# TaskTracker

> Sistema completo de gestión de tareas con API REST y widget de clima en tiempo real.

[![Live Demo](https://img.shields.io/badge/Demo-Live-brightgreen)](https://tasktracker-portfolio.fly.dev/app) 
[![API Docs](https://img.shields.io/badge/API-Swagger-orange)](https://tasktracker-portfolio.fly.dev/docs)
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
- **Fly.io** - Deploy en la nube
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

**Aplicación:** [https://tasktracker-portfolio.fly.dev/app](https://tasktracker-portfolio.fly.dev/app)  
**API Docs:** [https://tasktracker-portfolio.fly.dev/docs](https://tasktracker-portfolio.fly.dev/docs)

## Inicio Rápido

### Opción 1: Docker (Recomendado - Más Fácil)

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
├── fly.toml            # Deploy configuration
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

## Deploy en Fly.io

```bash
# Instalar Fly CLI
curl -L https://fly.io/install.sh | sh

# Autenticarse y desplegar
fly auth login
./deploy.sh
```

## Variables de Entorno (Opcional)

Para funcionalidad completa del clima:

```env
WEATHERAPI_KEY=tu_api_key_aqui
OPENWEATHER_API_KEY=tu_api_key_aqui
```

## Decisiones Técnicas

- **FastAPI**: Elegido por su performance, tipado automático y documentación integrada
- **SQLAlchemy**: ORM robusto para escalabilidad futura
- **Vanilla JS**: Evita dependencias innecesarias, demuestra conocimiento de JavaScript puro
- **Docker**: Garantiza consistencia entre entornos de desarrollo y producción
- **SQLite**: Base de datos ligera, ideal para demos y prototipos

---

## Troubleshooting

### Problemas Comunes

**Puerto 8000 ya en uso:**
```bash
# Ver qué proceso usa el puerto
lsof -i :8000

# Matar proceso
kill -9 [PID]

# O usar otro puerto
uvicorn main:app --host 0.0.0.0 --port 8001
```

**Error "ModuleNotFoundError":**
```bash
# Verificar que el venv esté activado
which python
# Debería mostrar: /ruta/a/tasktracker/.venv/bin/python

# Reinstalar dependencias
pip install -r requirements.txt
```

**Error de permisos en scripts:**
```bash
chmod +x run_tasktracker.sh
chmod +x stop_tasktracker.sh
chmod +x deploy.sh
```

**Base de datos corrupta:**
```bash
# Eliminar y recrear base de datos
rm -f db/tasks.db
# El sistema la recreará automáticamente
```

**Docker no funciona:**
```bash
# Verificar Docker instalado
docker --version
docker-compose --version

# Reconstruir imagen
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Variables de Entorno de Desarrollo

```bash
# Crear archivo .env (opcional)
echo "ENV=development" > .env
echo "WEATHERAPI_KEY=tu_api_key" >> .env
```