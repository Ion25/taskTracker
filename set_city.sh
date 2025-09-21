#!/bin/bash
echo "🌟 TaskTracker - Configurador de Ciudad para Clima"
echo "=================================================="
echo ""
echo "Ciudades disponibles:"
echo "1. Lima (Perú)"
echo "2. Madrid (España)"
echo "3. Tokyo (Japón)"
echo "4. New York (USA)"
echo "5. Londres (Reino Unido)"
echo "6. Buenos Aires (Argentina)"
echo "7. Mexico City (México)"
echo "8. Bogotá (Colombia)"
echo "9. Santiago (Chile)"
echo "10. Personalizada"
echo ""

read -p "Elige una opción (1-10): " opcion

case $opcion in
    1) city="Lima" ;;
    2) city="Madrid" ;;
    3) city="Tokyo" ;;
    4) city="New_York" ;;
    5) city="Londres" ;;
    6) city="Buenos_Aires" ;;
    7) city="Mexico_City" ;;
    8) city="Bogota" ;;
    9) city="Santiago" ;;
    10) 
        read -p "Ingresa el nombre de tu ciudad: " city
        city=$(echo $city | sed 's/ /_/g') # Reemplazar espacios con underscore
        ;;
    *)
        echo "Opción inválida. Usando Lima por defecto."
        city="Lima"
        ;;
esac

echo ""
echo "🌤️ Obteniendo clima actual de $city..."
response=$(curl -s "http://localhost:8000/api/weather?city=$city")

if echo "$response" | grep -q '"success":true'; then
    ciudad=$(echo "$response" | grep -o '"ciudad":"[^"]*"' | cut -d'"' -f4)
    temperatura=$(echo "$response" | grep -o '"temperatura":[0-9-]*' | cut -d':' -f2)
    descripcion=$(echo "$response" | grep -o '"descripcion":"[^"]*"' | cut -d'"' -f4)
    humedad=$(echo "$response" | grep -o '"humedad":[0-9]*' | cut -d':' -f2)
    sensacion=$(echo "$response" | grep -o '"sensacion_termica":[0-9-]*' | cut -d':' -f2)
    
    echo ""
    echo "✅ Clima obtenido exitosamente:"
    echo "   📍 Ciudad: $ciudad"
    echo "   🌡️  Temperatura: ${temperatura}°C (Sensación: ${sensacion}°C)"
    echo "   ☁️  Descripción: $descripcion"
    echo "   💧 Humedad: ${humedad}%"
    echo ""
    echo "🌐 Tu TaskTracker está mostrando el clima real de $ciudad"
    echo "📱 Ve la aplicación en: http://localhost:8000/app"
else
    echo "❌ Error obteniendo clima. Verifica el nombre de la ciudad."
fi