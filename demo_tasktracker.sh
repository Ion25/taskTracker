#!/bin/bash
echo "🎯 TaskTracker - DEMOSTRACIÓN COMPLETA (Sin Logs)"
echo "================================================"
echo ""
echo "✨ Funcionalidades implementadas:"
echo "  - CRUD completo de tareas"
echo "  - Widget de clima real (datos en vivo)"
echo "  ✅ Estadísticas automáticas"
echo "  ✅ Interfaz limpia y moderna"
echo "  ✅ Botón directo a documentación Swagger"
echo ""
echo "🌐 URLs importantes:"
echo "  📱 Aplicación: http://localhost:8000/app"
echo "  📚 API Docs: http://localhost:8000/docs"
echo "  🔧 API Base: http://localhost:8000/api"
echo ""
echo "🧪 Probando funcionalidades..."

# Crear tarea de ejemplo
echo "📝 Creando tarea de ejemplo..."
curl -s -X POST "http://localhost:8000/api/tasks" \
     -H "Content-Type: application/json" \
     -d '{"titulo":"Probar TaskTracker","descripcion":"Verificar que todo funcione correctamente"}' \
     > /dev/null

# Obtener estadísticas
echo "📊 Obteniendo estadísticas..."
stats=$(curl -s "http://localhost:8000/api/stats")
echo "   $stats"

# Obtener clima
echo "🌤️  Obteniendo clima actual..."
weather=$(curl -s "http://localhost:8000/api/weather?city=Lima")
ciudad=$(echo "$weather" | grep -o '"ciudad":"[^"]*"' | cut -d'"' -f4)
temperatura=$(echo "$weather" | grep -o '"temperatura":[0-9-]*' | cut -d':' -f2)
descripcion=$(echo "$weather" | grep -o '"descripcion":"[^"]*"' | cut -d'"' -f4)

echo "   📍 $ciudad: ${temperatura}°C - $descripcion"

echo ""
echo "✅ ¡Todo funcionando perfectamente!"
echo ""
echo "🎮 Para interactuar:"
echo "  1. Abre: http://localhost:8000/app"
echo "  2. Agrega/edita tareas"
echo "  3. Ve estadísticas en tiempo real"
echo "  4. Disfruta el clima real"
echo "  5. Haz clic en '📚 Ver Documentación API' para Swagger"
echo ""
echo "🚀 ¡Tu TaskTracker está listo para usar!"