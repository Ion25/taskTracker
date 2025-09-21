"""
TaskTracker API - Si# Configurar middleware CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS if not settings.DEBUG else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) gestión de tareas con información climática
Desarrollado con FastAPI, SQLAlchemy y APIs de clima externas
"""
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
from pathlib import Path

# Importar módulos locales
from models import create_tables, get_db, Task, SessionLocal
from routes import router as tasks_router
from weather import get_current_weather
from config import settings

# Configurar aplicación FastAPI con metadatos
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Configurar CORS para permitir requests del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas de tareas
app.include_router(tasks_router, prefix="/api", tags=["tasks"])

@app.on_event("startup")
async def startup_event():
    """
    Inicializar la aplicación y crear tareas de ejemplo
    """
    # Crear tablas de base de datos
    create_tables()
    
    # Crear tareas de ejemplo si no existen
    db = SessionLocal()
    try:
        # Verificar si ya existen tareas
        existing_tasks = db.query(Task).count()
        
        if existing_tasks == 0:
            # Crear tareas de ejemplo
            sample_tasks = [
                Task(
                    titulo="Probar TaskTracker",
                    descripcion="Explorar todas las funcionalidades de la aplicación",
                    estado="pendiente"
                ),
                Task(
                    titulo="Crear mi primera tarea",
                    descripcion="Usar el formulario para agregar una tarea personalizada",
                    estado="pendiente"
                ),
                Task(
                    titulo="Revisar el clima",
                    descripcion="Verificar que el widget de clima muestre información actualizada",
                    estado="completada"
                ),
                Task(
                    titulo="Explorar la documentación",
                    descripcion="Hacer clic en el botón 'Docs' para ver la API en Swagger",
                    estado="pendiente"
                ),
                Task(
                    titulo="Marcar tarea como completada",
                    descripcion="Usar el checkbox para cambiar el estado de una tarea",
                    estado="completada"
                )
            ]
            
            for task in sample_tasks:
                db.add(task)
            
            db.commit()
            print("Tareas de ejemplo creadas correctamente")
        else:
            print(f"Base de datos ya contiene {existing_tasks} tareas")
            
    except Exception as e:
        print(f"Error creando tareas de ejemplo: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("TaskTracker iniciado correctamente")

@app.get("/")
async def root():
    """
    Información básica de la API
    """
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENV,
        "docs": "/docs",
        "endpoints": {
            "tasks": "/api/tasks",
            "weather": "/api/weather",
            "stats": "/api/stats"
        }
    }

@app.get("/api/weather")
async def weather_endpoint(city: str = "Lima"):
    """
    Endpoint para obtener información del clima
    """
    return await get_current_weather(city)

@app.get("/api/stats")
async def stats_endpoint(db: Session = Depends(get_db)):
    """
    Estadísticas de las tareas
    """
    try:
        # Contar tareas por estado
        total_tareas = db.query(Task).count()
        tareas_pendientes = db.query(Task).filter(Task.estado == "pendiente").count()
        tareas_completadas = db.query(Task).filter(Task.estado == "completada").count()
        
        stats_data = {
            "total": total_tareas,
            "pendientes": tareas_pendientes,
            "completadas": tareas_completadas,
            "porcentaje_completadas": round((tareas_completadas / total_tareas * 100) if total_tareas > 0 else 0, 1)
        }
        
        return stats_data
        
    except Exception as e:
        return {
            "total": 0,
            "pendientes": 0,
            "completadas": 0,
            "porcentaje_completadas": 0,
            "error": "Error al obtener estadísticas"
        }

# Montar archivos estáticos del frontend
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
    
    @app.get("/app")
    async def serve_frontend():
        """Servir el frontend HTML"""
        index_path = frontend_path / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        return {"error": "Frontend no encontrado"}
    
    # Servir archivos estáticos directamente
    @app.get("/styles.css")
    async def serve_css():
        css_path = frontend_path / "styles.css"
        if css_path.exists():
            return FileResponse(str(css_path), media_type="text/css")
        return {"error": "CSS no encontrado"}
    
    @app.get("/script.js")
    async def serve_js():
        js_path = frontend_path / "script.js"
        if js_path.exists():
            return FileResponse(str(js_path), media_type="application/javascript")
        return {"error": "JavaScript no encontrado"}

# Manejo de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Manejo de errores generales
    """
    print(f"Error no manejado: {str(exc)} en {request.url.path}")
    return {
        "error": "Error interno del servidor",
        "message": str(exc) if settings.DEBUG else "Contactar al administrador"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )