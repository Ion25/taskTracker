#!/bin/bash

# Script para deployment en Fly.io
echo "🚀 Desplegando TaskTracker en Fly.io..."

# Verificar que fly CLI esté instalado
if ! command -v fly &> /dev/null; then
    echo "❌ Fly CLI no está instalado"
    echo "📥 Instalar desde: https://fly.io/docs/getting-started/installing-flyctl/"
    exit 1
fi

# Autenticarse (si no está ya autenticado)
echo "🔐 Verificando autenticación..."
fly auth whoami || fly auth login

# Crear app si no existe
echo "🏗️  Configurando aplicación..."
if ! fly apps list | grep -q "tasktracker-portfolio"; then
    fly apps create tasktracker-portfolio --generate-name=false
fi

# Configurar secretos (opcional - APIs de clima)
echo "⚙️  Configurar variables de entorno (opcional):"
echo "   fly secrets set WEATHERAPI_KEY=tu_api_key"
echo "   fly secrets set OPENWEATHER_API_KEY=tu_api_key"

# Desplegar
echo "🚀 Desplegando aplicación..."
fly deploy

# Mostrar información de la app desplegada
echo ""
echo "✅ Deployment completado!"
echo "🌐 URL: https://tasktracker-portfolio.fly.dev"
echo "📊 Status: fly status"
echo "📝 Logs: fly logs"

echo ""
echo "🎯 Tu TaskTracker ya está live para reclutadores!"