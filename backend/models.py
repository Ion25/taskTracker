"""
Modelos de base de datos SQLAlchemy para TaskTracker
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import os

# Base para modelos
Base = declarative_base()

# Configuración de la base de datos
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "tasks.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Motor de base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Task(Base):
    """
    Modelo para gestión de tareas del usuario
    """
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String, nullable=False, index=True)
    descripcion = Column(String, nullable=True)
    estado = Column(String, default="pendiente")  # pendiente | completada
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Serializa la tarea a diccionario JSON"""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

def create_tables():
    """Inicializa las tablas de la base de datos"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Genera sesiones de base de datos SQLAlchemy"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()