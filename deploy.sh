#!/bin/bash

# Script universal para deployment en múltiples plataformas
echo "🚀 TaskTracker Universal Deployer"
echo "=================================="

echo "Selecciona tu plataforma de deployment:"
echo "1) Render.com (Recomendado - Más fácil)"
echo "2) Koyeb.com (Muy rápido)"
echo "3) Manual Docker build"
echo "4) Local development"

read -p "Opción [1-4]: " choice

case $choice in
    1)
        echo "🎨 Desplegando en Render.com..."
        echo ""
        echo "� Pasos para Render:"
        echo "1. Ve a https://render.com"
        echo "2. Conecta tu cuenta de GitHub"
        echo "3. Crear 'Web Service' desde tu repo"
        echo "4. Environment: Docker"
        echo "5. Region: Oregon"
        echo "6. Instance: Free"
        echo ""
        echo "✅ render.yaml ya está configurado"
        echo "� El deploy será automático al conectar el repo"
        echo ""
        echo "🌐 URL final: https://tu-tasktracker.onrender.com/app"
        ;;
        
    2)
        echo "⚡ Desplegando en Koyeb.com..."
        echo ""
        echo "📝 Pasos para Koyeb:"
        echo "1. Ve a https://koyeb.com"
        echo "2. Crear cuenta gratuita"
        echo "3. Click 'Create App'"
        echo "4. Selecciona 'GitHub repository'"
        echo "5. Build type: Dockerfile"
        echo "6. Port: 8000"
        echo "7. Instance: Nano (gratis)"
        echo ""
        echo "✅ .koyeb/config.yaml ya está configurado"
        echo "🚀 Deploy automático desde GitHub"
        echo ""
        echo "🌐 URL final: https://tu-tasktracker-[id].koyeb.app/app"
        ;;
        
    3)
        echo "🐳 Build manual con Docker..."
        echo ""
        
        # Verificar Docker
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker no está instalado"
            echo "📥 Instalar desde: https://docs.docker.com/get-docker/"
            exit 1
        fi
        
        # Build de la imagen
        echo "🏗️  Building Docker image..."
        docker build -t tasktracker:latest .
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Docker image construida exitosamente!"
            echo ""
            echo "🚀 Para ejecutar localmente:"
            echo "   docker run -p 8000:8000 tasktracker:latest"
            echo ""
            echo "🌐 Accede a: http://localhost:8000/app"
        else
            echo "❌ Error building Docker image"
            exit 1
        fi
        ;;
        
    4)
        echo "� Modo desarrollo local..."
        echo ""
        
        # Verificar Python
        if ! command -v python3 &> /dev/null; then
            echo "❌ Python3 no está instalado"
            exit 1
        fi
        
        # Verificar venv
        if [ ! -d "venv" ]; then
            echo "🏗️  Creando entorno virtual..."
            python3 -m venv venv
        fi
        
        # Activar venv
        echo "🔧 Activando entorno virtual..."
        source venv/bin/activate
        
        # Instalar dependencias
        echo "📦 Instalando dependencias..."
        pip install -r backend/requirements.txt
        
        # Ejecutar servidor
        echo ""
        echo "� Iniciando servidor de desarrollo..."
        echo "   Ctrl+C para detener"
        echo ""
        cd backend
        python main.py
        ;;
        
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

echo ""
echo "🎯 Tu TaskTracker está listo para impresionar reclutadores!"