import os
from typing import Optional

class Settings:
    """Configuración de la aplicación"""
    
    # Base configuration
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = ENV == "development"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./db/tasks.db")
    
    # Weather APIs
    WEATHERAPI_KEY: Optional[str] = os.getenv("WEATHERAPI_KEY")
    OPENWEATHER_API_KEY: Optional[str] = os.getenv("OPENWEATHER_API_KEY")
    ACCUWEATHER_API_KEY: Optional[str] = os.getenv("ACCUWEATHER_API_KEY")
    
    # CORS settings
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://*.fly.dev"
    ] if DEBUG else ["https://*.fly.dev"]
    
    # App metadata
    APP_NAME: str = "TaskTracker"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Sistema completo de gestión de tareas con API REST y widget de clima"
    
    # Performance
    WEATHER_CACHE_DURATION: int = 300  # 5 minutes
    
settings = Settings()