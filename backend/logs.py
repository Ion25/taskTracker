"""
Sistema de logs en tiempo real para TaskTracker usando Server-Sent Events (SSE)
"""
import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any
from fastapi import Request
from fastapi.responses import StreamingResponse

class LogManager:
    """
    Maneja los logs del sistema y los envía a los clientes conectados via SSE
    """
    
    def __init__(self):
        self.clients: List[asyncio.Queue] = []
        self.log_history: List[Dict[str, Any]] = []
        
    def add_client(self, queue: asyncio.Queue):
        """Agrega un cliente SSE a la lista"""
        self.clients.append(queue)
        
    def remove_client(self, queue: asyncio.Queue):
        """Remueve un cliente SSE de la lista"""
        if queue in self.clients:
            self.clients.remove(queue)
            
    async def log_event(self, event_type: str, message: str, data: Dict[str, Any] = None):
        """
        Registra un evento y lo envía a todos los clientes conectados
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "type": event_type,
            "message": message,
            "data": data or {}
        }
        
        # Guardar en historial (máximo 100 entradas)
        self.log_history.append(log_entry)
        if len(self.log_history) > 100:
            self.log_history.pop(0)
            
        # Formatear mensaje para mostrar
        formatted_message = f"[{timestamp}] {message}"
        
        # Enviar a todos los clientes conectados
        disconnected_clients = []
        for client_queue in self.clients:
            try:
                await client_queue.put(formatted_message)
            except Exception:
                # Cliente desconectado
                disconnected_clients.append(client_queue)
                
        # Limpiar clientes desconectados
        for client_queue in disconnected_clients:
            self.remove_client(client_queue)
            
    def get_recent_logs(self, limit: int = 20) -> List[str]:
        """Obtiene los logs recientes formateados"""
        recent_logs = self.log_history[-limit:] if limit > 0 else self.log_history
        return [f"[{log['timestamp']}] {log['message']}" for log in recent_logs]

# Instancia global del gestor de logs
log_manager = LogManager()

async def event_stream_generator(request: Request):
    """
    Generador de eventos SSE para logs en tiempo real
    """
    client_queue = asyncio.Queue()
    log_manager.add_client(client_queue)
    
    try:
        # Enviar logs recientes al conectar
        recent_logs = log_manager.get_recent_logs(10)
        for log_message in recent_logs:
            yield f"data: {log_message}\n\n"
            
        # Enviar nuevos logs en tiempo real
        while True:
            try:
                # Esperar por nuevos logs (con timeout)
                log_message = await asyncio.wait_for(client_queue.get(), timeout=30.0)
                yield f"data: {log_message}\n\n"
            except asyncio.TimeoutError:
                # Enviar ping para mantener conexión viva
                yield f"data: [PING] Conexión activa\n\n"
            except Exception:
                break
                
    except asyncio.CancelledError:
        pass
    finally:
        log_manager.remove_client(client_queue)

def create_sse_response(request: Request):
    """Crea respuesta SSE para logs en tiempo real"""
    return StreamingResponse(
        event_stream_generator(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )