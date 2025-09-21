#!/bin/bash

echo "🚀 Configurando y subiendo TaskTracker a GitHub..."

# Variables (personaliza estas)
GITHUB_USER="tu-usuario-github"
REPO_NAME="tasktracker"

echo "📝 Configurando Git..."
git init
git branch -M main

echo "📦 Agregando archivos..."
git add .

echo "💾 Creando commit inicial..."
git commit -m "Initial commit: TaskTracker Portfolio Project

✨ Features:
- FastAPI REST API with SQLAlchemy ORM  
- Vanilla JavaScript responsive frontend
- Real-time weather widget with multiple APIs
- Automatic Swagger documentation
- Docker containerization ready
- Fly.io deployment configuration
- Complete CRUD operations
- Real-time task statistics

🛠️ Tech Stack:
- Backend: FastAPI, SQLAlchemy, Uvicorn
- Frontend: HTML5, CSS3, Vanilla JavaScript
- Database: SQLite
- Container: Docker
- Deploy: Fly.io
- Documentation: Swagger/OpenAPI"

echo "🔗 Conectando con GitHub..."
git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git

echo "⬆️ Subiendo a GitHub..."
echo "Se te pedirá:"
echo "  Username: $GITHUB_USER"
echo "  Password: [Tu Token de GitHub - NO tu contraseña]"
echo ""

git push -u origin main

echo "✅ ¡Proyecto subido exitosamente!"
echo "🌐 Ver en: https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo "🎯 Próximos pasos:"
echo "  1. Actualizar README.md con tu información personal"
echo "  2. Agregar topics en GitHub: fastapi, python, docker, portfolio"
echo "  3. Configurar deployment en Fly.io con ./deploy.sh"