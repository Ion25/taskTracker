#!/bin/bash
echo "🌍 Probando clima real con diferentes ciudades..."
echo ""

cities=("Lima" "Madrid" "Tokyo" "New_York" "Londres" "Buenos_Aires" "Mexico_City")

for city in "${cities[@]}"; do
    echo "🌤️  Clima en $city:"
    response=$(curl -s "http://localhost:8000/api/weather?city=$city")
    
    # Extraer datos usando grep y cut (sin jq)
    ciudad=$(echo "$response" | grep -o '"ciudad":"[^"]*"' | cut -d'"' -f4)
    temperatura=$(echo "$response" | grep -o '"temperatura":[0-9-]*' | cut -d':' -f2)
    descripcion=$(echo "$response" | grep -o '"descripcion":"[^"]*"' | cut -d'"' -f4)
    source=$(echo "$response" | grep -o '"source":"[^"]*"' | cut -d'"' -f4)
    
    echo "   📍 Ciudad: $ciudad"
    echo "   🌡️  Temperatura: ${temperatura}°C"
    echo "   Descripción: $descripcion"
    echo "   📡 Fuente: $source"
    echo ""
    
    sleep 1
done

echo "Todas las consultas completadas usando API gratuita wttr.in"
echo "💡 Para mayor precisión, configura WEATHERAPI_KEY o OPENWEATHER_API_KEY"