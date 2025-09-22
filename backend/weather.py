"""
Integración con APIs de datos climáticos externos
"""
import httpx
import os
from typing import Dict, Any, Optional
from fastapi import HTTPException
from datetime import datetime, timedelta

class WeatherService:
    """
    Cliente para múltiples servicios de clima
    """
    
    def __init__(self):
        # API Keys de diferentes servicios (configurar en variables de entorno)
        self.openweather_key = os.getenv("OPENWEATHER_API_KEY")
        self.weatherapi_key = os.getenv("WEATHERAPI_KEY")
        self.accuweather_key = os.getenv("ACCUWEATHER_API_KEY")
        
        # URLs base de diferentes APIs
        self.openweather_url = "https://api.openweathermap.org/data/2.5/weather"
        self.weatherapi_url = "https://api.weatherapi.com/v1/current.json"
        self.accuweather_url = "https://dataservice.accuweather.com/currentconditions/v1"
        
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)  # Cache por 5 minutos
        
    async def get_weather(self, city: str = "Lima") -> Dict[str, Any]:
        """
        Obtiene información del clima para una ciudad usando múltiples APIs
        """
        # Verificar cache
        cache_key = f"weather_{city}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_duration:
                return cached_data

        # Intentar diferentes APIs en orden de preferencia
        weather_data = None
        
        # 1. Intentar WeatherAPI (más generoso)
        if self.weatherapi_key:
            weather_data = await self._get_weatherapi_data(city)
            if weather_data and weather_data.get("success"):
                return self._cache_and_return(cache_key, weather_data)
        
        # 2. Intentar OpenWeatherMap
        if self.openweather_key:
            weather_data = await self._get_openweather_data(city)
            if weather_data and weather_data.get("success"):
                return self._cache_and_return(cache_key, weather_data)
        
        # 3. Intentar AccuWeather
        if self.accuweather_key:
            weather_data = await self._get_accuweather_data(city)
            if weather_data and weather_data.get("success"):
                return self._cache_and_return(cache_key, weather_data)
        
        # 4. Si no hay APIs configuradas, usar API pública gratuita (sin key)
        weather_data = await self._get_free_weather_data(city)
        if weather_data and weather_data.get("success"):
            return self._cache_and_return(cache_key, weather_data)
        
        # 5. Fallback a datos de prueba
        print(f"[Weather] Usando datos de prueba para {city} (configurar API keys para datos reales)")
        return self._get_demo_weather_data(city)
    
    async def get_weather_by_coords(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Obtiene información del clima para coordenadas usando múltiples APIs
        """
        # Verificar cache
        cache_key = f"weather_{lat}_{lon}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_duration:
                return cached_data

        # Intentar diferentes APIs en orden de preferencia
        weather_data = None
        
        # 1. Intentar WeatherAPI (más generoso)
        if self.weatherapi_key:
            weather_data = await self._get_weatherapi_data_coords(lat, lon)
            if weather_data and weather_data.get("success"):
                return self._cache_and_return(cache_key, weather_data)
        
        # 2. Intentar OpenWeatherMap
        if self.openweather_key:
            weather_data = await self._get_openweather_data_coords(lat, lon)
            if weather_data and weather_data.get("success"):
                return self._cache_and_return(cache_key, weather_data)
        
        # 3. Si no hay APIs configuradas, usar API pública gratuita
        # Necesitamos convertir coords a ciudad para wttr.in
        try:
            # Usar reverse geocoding simple o fallback a Lima
            city = await self._coords_to_city(lat, lon)
            weather_data = await self._get_free_weather_data(city)
            if weather_data and weather_data.get("success"):
                # Actualizar con coordenadas reales
                weather_data["lat"] = lat
                weather_data["lon"] = lon
                return self._cache_and_return(cache_key, weather_data)
        except:
            pass
        
        # 4. Fallback a datos de prueba con coordenadas
        print(f"[Weather] Usando datos de prueba para coords {lat}, {lon}")
        demo_data = self._get_demo_weather_data("Ubicación actual")
        demo_data["lat"] = lat
        demo_data["lon"] = lon
        return demo_data
    
    def _cache_and_return(self, cache_key: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Guarda en cache y devuelve los datos"""
        self.cache[cache_key] = (data, datetime.now())
        return data
    
    async def _get_weatherapi_data(self, city: str) -> Optional[Dict[str, Any]]:
        """Consulta WeatherAPI.com para datos climáticos"""
        try:
            params = {
                "key": self.weatherapi_key,
                "q": city,
                "lang": "es"
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.weatherapi_url, params=params)
                response.raise_for_status()
                
            data = response.json()
            
            processed_data = {
                "ciudad": data["location"]["name"],
                "temperatura": round(data["current"]["temp_c"]),
                "descripcion": data["current"]["condition"]["text"],
                "icono": self._weatherapi_icon_to_emoji(data["current"]["condition"]["code"]),
                "humedad": data["current"]["humidity"],
                "sensacion_termica": round(data["current"]["feelslike_c"]),
                "ultima_actualizacion": datetime.now().strftime("%H:%M"),
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "source": "WeatherAPI"
            }
            
            print(f"[Weather] Clima actualizado desde WeatherAPI: {processed_data['ciudad']} - {processed_data['temperatura']}°C")
            
            return processed_data
            
        except Exception as e:
            print(f"[Weather] Error en WeatherAPI: {str(e)}")
            return None
    
    async def _get_openweather_data(self, city: str) -> Optional[Dict[str, Any]]:
        """Consulta OpenWeatherMap API para información climática"""
        try:
            params = {
                "q": city,
                "appid": self.openweather_key,
                "units": "metric",
                "lang": "es"
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.openweather_url, params=params)
                response.raise_for_status()
                
            data = response.json()
            
            processed_data = {
                "ciudad": data["name"],
                "temperatura": round(data["main"]["temp"]),
                "descripcion": data["weather"][0]["description"].title(),
                "icono": self._openweather_icon_to_emoji(data["weather"][0]["icon"]),
                "humedad": data["main"]["humidity"],
                "sensacion_termica": round(data["main"]["feels_like"]),
                "ultima_actualizacion": datetime.now().strftime("%H:%M"),
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "source": "OpenWeatherMap"
            }
            
            print(f"[Weather] Clima actualizado desde OpenWeather: {processed_data['ciudad']} - {processed_data['temperatura']}°C")
            
            return processed_data
            
        except Exception as e:
            print(f"[Weather] Error en OpenWeather: {str(e)}")
            return None
    
    async def _get_accuweather_data(self, city: str) -> Optional[Dict[str, Any]]:
        """Consulta AccuWeather API (implementación básica)"""
        try:
            # AccuWeather requiere primero obtener la location key, luego el clima
            # Por simplicidad, este es un placeholder
            print("[Weather] AccuWeather no implementado completamente")
            return None
            
        except Exception as e:
            print(f"[Weather] Error en AccuWeather: {str(e)}")
            return None
    
    async def _get_free_weather_data(self, city: str) -> Optional[Dict[str, Any]]:
        """Consulta wttr.in API gratuita sin autenticación"""
        try:
            # wttr.in es una API gratuita sin necesidad de key
            url = f"https://wttr.in/{city}?format=j1"
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
            data = response.json()
            current = data["current_condition"][0]
            
            processed_data = {
                "ciudad": city.title(),
                "temperatura": round(float(current["temp_C"])),
                "descripcion": current["weatherDesc"][0]["value"],
                "icono": self._wttr_icon_to_emoji(current["weatherCode"]),
                "humedad": int(current["humidity"]),
                "sensacion_termica": round(float(current["FeelsLikeC"])),
                "ultima_actualizacion": datetime.now().strftime("%H:%M"),
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "source": "wttr.in (gratis)",
                "free_api": True
            }
            
            print(f"[Weather] Clima actualizado desde API gratuita: {processed_data['ciudad']} - {processed_data['temperatura']}°C")
            
            return processed_data
            
        except Exception as e:
            print(f"[Weather] Error en API gratuita: {str(e)}")
            return None
    
    async def _get_weatherapi_data_coords(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Consulta WeatherAPI.com usando coordenadas"""
        try:
            params = {
                "key": self.weatherapi_key,
                "q": f"{lat},{lon}",
                "lang": "es"
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.weatherapi_url, params=params)
                response.raise_for_status()
                
            data = response.json()
            
            # Obtener zona horaria local del usuario
            from datetime import datetime, timezone
            import pytz
            
            try:
                # Intentar obtener zona horaria de la respuesta
                tz_info = data["location"].get("tz_id", "UTC")
                local_tz = pytz.timezone(tz_info)
                local_time = datetime.now(local_tz)
                time_str = local_time.strftime("%H:%M")
            except:
                # Fallback a hora local del servidor
                time_str = datetime.now().strftime("%H:%M")
            
            processed_data = {
                "ciudad": f"{data['location']['name']}, {data['location']['country']}",
                "temperatura": round(data["current"]["temp_c"]),
                "descripcion": data["current"]["condition"]["text"],
                "icono": self._weatherapi_icon_to_emoji(data["current"]["condition"]["code"]),
                "humedad": data["current"]["humidity"],
                "sensacion_termica": round(data["current"]["feelslike_c"]),
                "ultima_actualizacion": time_str,
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "source": "WeatherAPI (GPS)",
                "lat": lat,
                "lon": lon,
                "timezone": data["location"].get("tz_id", "UTC")
            }
            
            print(f"[Weather] Clima actualizado desde WeatherAPI (GPS): {processed_data['ciudad']} - {processed_data['temperatura']}°C")
            
            return processed_data
            
        except Exception as e:
            print(f"[Weather] Error en WeatherAPI (coords): {str(e)}")
            return None
    
    async def _get_openweather_data_coords(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Consulta OpenWeatherMap usando coordenadas"""
        try:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.openweather_key,
                "units": "metric",
                "lang": "es"
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.openweather_url, params=params)
                response.raise_for_status()
                
            data = response.json()
            
            # Calcular hora local usando timezone offset
            from datetime import datetime, timezone, timedelta
            try:
                offset_seconds = data.get("timezone", 0)
                local_tz = timezone(timedelta(seconds=offset_seconds))
                local_time = datetime.now(local_tz)
                time_str = local_time.strftime("%H:%M")
            except:
                time_str = datetime.now().strftime("%H:%M")
            
            processed_data = {
                "ciudad": f"{data['name']}, {data['sys']['country']}",
                "temperatura": round(data["main"]["temp"]),
                "descripcion": data["weather"][0]["description"].title(),
                "icono": self._openweather_icon_to_emoji(data["weather"][0]["icon"]),
                "humedad": data["main"]["humidity"],
                "sensacion_termica": round(data["main"]["feels_like"]),
                "ultima_actualizacion": time_str,
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "source": "OpenWeatherMap (GPS)",
                "lat": lat,
                "lon": lon
            }
            
            print(f"[Weather] Clima actualizado desde OpenWeatherMap (GPS): {processed_data['ciudad']} - {processed_data['temperatura']}°C")
            
            return processed_data
            
        except Exception as e:
            print(f"[Weather] Error en OpenWeatherMap (coords): {str(e)}")
            return None
    
    async def _coords_to_city(self, lat: float, lon: float) -> str:
        """Convierte coordenadas a nombre de ciudad (simple reverse geocoding)"""
        try:
            # Usar un servicio gratuito de reverse geocoding
            url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=es"
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
            data = response.json()
            city = data.get("city") or data.get("locality") or data.get("principalSubdivision", "Ubicación actual")
            return city
            
        except:
            return "Ubicación actual"
    
    def _get_demo_weather_data(self, city: str) -> Dict[str, Any]:
        """Datos de prueba cuando no hay API disponible"""
        return {
            "ciudad": city,
            "temperatura": 22,
            "descripcion": "Parcialmente Nublado",
            "icono": "⛅",
            "humedad": 65,
            "sensacion_termica": 24,
            "ultima_actualizacion": datetime.now().strftime("%H:%M"),
            "timestamp": datetime.now().isoformat(),
            "success": True,
            "demo": True,
            "source": "Demo"
        }
    
    def _weatherapi_icon_to_emoji(self, code: int) -> str:
        """Convierte códigos de WeatherAPI a emojis"""
        icon_map = {
            1000: "☀️",  # Sunny
            1003: "⛅",  # Partly cloudy
            1006: "☁️",  # Cloudy
            1009: "☁️",  # Overcast
            1030: "🌫️",  # Mist
            1063: "🌦️",  # Patchy rain possible
            1066: "🌨️",  # Patchy snow possible
            1069: "🌨️",  # Patchy sleet possible
            1072: "🌨️",  # Patchy freezing drizzle possible
            1087: "⛈️",  # Thundery outbreaks possible
            1114: "❄️",  # Blowing snow
            1117: "❄️",  # Blizzard
            1135: "🌫️",  # Fog
            1147: "🌫️",  # Freezing fog
            1150: "🌦️",  # Patchy light drizzle
            1153: "🌦️",  # Light drizzle
            1168: "🌧️",  # Freezing drizzle
            1171: "🌧️",  # Heavy freezing drizzle
            1180: "🌦️",  # Patchy light rain
            1183: "🌧️",  # Light rain
            1186: "🌧️",  # Moderate rain at times
            1189: "🌧️",  # Moderate rain
            1192: "🌧️",  # Heavy rain at times
            1195: "🌧️",  # Heavy rain
            1198: "🌧️",  # Light freezing rain
            1201: "🌧️",  # Moderate or heavy freezing rain
            1204: "🌨️",  # Light sleet
            1207: "🌨️",  # Moderate or heavy sleet
            1210: "🌨️",  # Patchy light snow
            1213: "❄️",  # Light snow
            1216: "❄️",  # Patchy moderate snow
            1219: "❄️",  # Moderate snow
            1222: "❄️",  # Patchy heavy snow
            1225: "❄️",  # Heavy snow
            1237: "🌨️",  # Ice pellets
            1240: "🌦️",  # Light rain shower
            1243: "🌧️",  # Moderate or heavy rain shower
            1246: "🌧️",  # Torrential rain shower
            1249: "🌨️",  # Light sleet showers
            1252: "🌨️",  # Moderate or heavy sleet showers
            1255: "🌨️",  # Light snow showers
            1258: "❄️",  # Moderate or heavy snow showers
            1261: "🌨️",  # Light showers of ice pellets
            1264: "🌨️",  # Moderate or heavy showers of ice pellets
            1273: "⛈️",  # Patchy light rain with thunder
            1276: "⛈️",  # Moderate or heavy rain with thunder
            1279: "⛈️",  # Patchy light snow with thunder
            1282: "⛈️",  # Moderate or heavy snow with thunder
        }
        return icon_map.get(code, "🌤️")
    
    def _openweather_icon_to_emoji(self, icon: str) -> str:
        """Convierte códigos de OpenWeatherMap a emojis"""
        icon_map = {
            '01d': '☀️', '01n': '🌙',
            '02d': '⛅', '02n': '☁️',
            '03d': '☁️', '03n': '☁️',
            '04d': '☁️', '04n': '☁️',
            '09d': '🌧️', '09n': '🌧️',
            '10d': '🌦️', '10n': '🌦️',
            '11d': '⛈️', '11n': '⛈️',
            '13d': '❄️', '13n': '❄️',
            '50d': '🌫️', '50n': '🌫️'
        }
        return icon_map.get(icon, "🌤️")
    
    def _wttr_icon_to_emoji(self, code: str) -> str:
        """Convierte códigos de wttr.in a emojis"""
        code = str(code)
        icon_map = {
            '113': '☀️',  # Sunny
            '116': '⛅',  # Partly cloudy
            '119': '☁️',  # Cloudy
            '122': '☁️',  # Overcast
            '143': '🌫️',  # Mist
            '176': '🌦️',  # Nearby rain
            '179': '🌨️',  # Nearby snow
            '182': '🌨️',  # Nearby sleet
            '185': '🌨️',  # Nearby freezing drizzle
            '200': '⛈️',  # Nearby thundery outbreaks
            '227': '❄️',  # Blowing snow
            '230': '❄️',  # Blizzard
            '248': '🌫️',  # Fog
            '260': '🌫️',  # Freezing fog
            '263': '🌦️',  # Patchy light drizzle
            '266': '🌦️',  # Light drizzle
            '281': '🌧️',  # Freezing drizzle
            '284': '🌧️',  # Heavy freezing drizzle
            '293': '🌦️',  # Patchy light rain
            '296': '🌧️',  # Light rain
            '299': '🌧️',  # Moderate rain at times
            '302': '🌧️',  # Moderate rain
            '305': '🌧️',  # Heavy rain at times
            '308': '🌧️',  # Heavy rain
            '311': '🌧️',  # Light freezing rain
            '314': '🌧️',  # Moderate or heavy freezing rain
            '317': '🌨️',  # Light sleet
            '320': '🌨️',  # Moderate or heavy sleet
            '323': '🌨️',  # Patchy light snow
            '326': '❄️',  # Light snow
            '329': '❄️',  # Patchy moderate snow
            '332': '❄️',  # Moderate snow
            '335': '❄️',  # Patchy heavy snow
            '338': '❄️',  # Heavy snow
            '350': '🌨️',  # Ice pellets
            '353': '🌦️',  # Light rain shower
            '356': '🌧️',  # Moderate or heavy rain shower
            '359': '🌧️',  # Torrential rain shower
            '362': '🌨️',  # Light sleet showers
            '365': '🌨️',  # Moderate or heavy sleet showers
            '368': '🌨️',  # Light snow showers
            '371': '❄️',  # Moderate or heavy snow showers
            '374': '🌨️',  # Light showers of ice pellets
            '377': '🌨️',  # Moderate or heavy showers of ice pellets
            '386': '⛈️',  # Patchy light rain with thunder
            '389': '⛈️',  # Moderate or heavy rain with thunder
            '392': '⛈️',  # Patchy light snow with thunder
            '395': '⛈️',  # Moderate or heavy snow with thunder
        }
        return icon_map.get(code, "🌤️")
    
    def _get_error_weather_data(self, error_message: str) -> Dict[str, Any]:
        """Datos de error cuando falla la API"""
        return {
            "ciudad": "Error",
            "temperatura": "--",
            "descripcion": "No disponible",
            "icono": "unknown",
            "humedad": "--",
            "sensacion_termica": "--",
            "ultima_actualizacion": datetime.now().strftime("%H:%M"),
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "error": error_message
        }

# Instancia global del servicio de clima
weather_service = WeatherService()

async def get_current_weather(city: str = "Lima") -> Dict[str, Any]:
    """
    Endpoint function para obtener el clima actual por nombre de ciudad
    """
    return await weather_service.get_weather(city)

async def get_current_weather_by_coords(lat: float, lon: float) -> Dict[str, Any]:
    """
    Endpoint function para obtener el clima actual por coordenadas
    """
    return await weather_service.get_weather_by_coords(lat, lon)