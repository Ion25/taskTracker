#!/bin/bash
echo "Iniciando servidor TaskTracker en segundo plano..."
cd /home/chirimoya/projects/taskTracker/backend
/home/chirimoya/projects/taskTracker/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
SERVER_PID=$!
echo "Servidor iniciado con PID: $SERVER_PID"
echo "📖 Log del servidor en: server.log"
echo "🌐 Acceso a la aplicación: http://localhost:8000/app"
echo "📚 Documentación API: http://localhost:8000/docs"
echo ""
echo "Para detener el servidor ejecuta: kill $SERVER_PID"