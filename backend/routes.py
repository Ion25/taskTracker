"""
Endpoints API para operaciones CRUD de tareas
"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from models import Task, get_db

# Router para las rutas de tareas
router = APIRouter()

# Schemas de Pydantic para validación
class TaskCreate(BaseModel):                
    titulo: str
    descripcion: str = ""

class TaskUpdate(BaseModel):
    titulo: str = None
    descripcion: str = None
    estado: str = None  # pendiente | completada

class TaskResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str
    estado: str
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def crear_tarea(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva tarea en el sistema
    """
    try:
        # Crear nueva tarea
        db_task = Task(
            titulo=task.titulo,
            descripcion=task.descripcion,
            estado="pendiente"
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        return db_task
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear la tarea"
        )

@router.get("/tasks", response_model=List[TaskResponse])
async def listar_tareas(db: Session = Depends(get_db)):
    """
    Obtiene la lista completa de tareas
    """
    try:
        tasks = db.query(Task).order_by(Task.fecha_creacion.desc()).all()
        return tasks
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener las tareas"
        )

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def obtener_tarea(task_id: int, db: Session = Depends(get_db)):
    """
    Busca una tarea específica por su ID
    """
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarea con ID {task_id} no encontrada"
            )
        return task
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener la tarea"
        )

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def actualizar_tarea(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """
    Actualizar una tarea existente
    """
    try:
        # Buscar tarea
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarea con ID {task_id} no encontrada"
            )
        
        # Guardar estado anterior para el log
        estado_anterior = task.estado
        
        # Actualizar campos si se proporcionan
        if task_update.titulo is not None:
            task.titulo = task_update.titulo
        if task_update.descripcion is not None:
            task.descripcion = task_update.descripcion
        if task_update.estado is not None:
            if task_update.estado not in ["pendiente", "completada"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Estado debe ser 'pendiente' o 'completada'"
                )
            task.estado = task_update.estado
            
        db.commit()
        db.refresh(task)
        
        return task
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar la tarea"
        )

@router.delete("/tasks/{task_id}")
async def eliminar_tarea(task_id: int, db: Session = Depends(get_db)):
    """
    Elimina una tarea del sistema permanentemente
    """
    try:
        # Buscar tarea
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarea con ID {task_id} no encontrada"
            )
            
        # Guardar título para el log
        titulo_tarea = task.titulo
        
        # Eliminar tarea
        db.delete(task)
        db.commit()
        
        return {"message": f"Tarea '{titulo_tarea}' eliminada correctamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la tarea"
        )