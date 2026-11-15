from geopy.geocoders import Nominatim
import requests

# Inicializamos el geolocalizador con un nombre de identificación para la app
geolocalizador = Nominatim(user_agent="presupuesto_viaje_app")

def obtener_coordenadas(ciudad):
    try:
        # Le sumamos ", Argentina" para que la búsqueda sea precisa en el país
        locacion = geolocalizador.geocode(ciudad + ", Argentina")
        if locacion:
            return locacion.longitude, locacion.latitude
    except Exception as e:
        print(f"Error al buscar la ciudad: {e}")
    return None, None


#Calcular la ruta usando la latitud y longitud
def calcular_ruta_osrm(ciudad_origen, ciudad_destino):
    # 1. Obtenemos las coordenadas de ambas ciudades
    longitud1, latitud1 = obtener_coordenadas(ciudad_origen)
    longitud2, latitud2 = obtener_coordenadas(ciudad_destino)

    # Si alguna de las dos no se encuentra, salimos
    if not longitud1 or not longitud2:
        print("No se pudieron encontrar una o ambas ciudades en el mapa.")
        return None, None

    # 2. Armamos la URL para consultar el servicio OSRM
    url = f"http://router.project-osrm.org/route/v1/driving/{longitud1},{latitud1};{longitud2},{latitud2}?overview=false"
    
    try:
        # Hacemos la petición web
        response = requests.get(url)
        data = response.json()
        
        # Verificamos que la ruta se haya calculado con éxito
        if data["code"] == "Ok":
            # OSRM devuelve la distancia en metros, la pasamos a kilómetros
            distancia_km = data["routes"][0]["distance"] / 1000
            # Y la duración en segundos
            duracion_segundos = data["routes"][0]["duration"]
            
            # Convertimos los segundos a horas y minutos legibles
            horas = int(duracion_segundos // 3600)
            minutos = int((duracion_segundos % 3600) // 60)
            tiempo_formato = f"{horas} horas {minutos} minutos"
            
            return round(distancia_km, 2), tiempo_formato
        else:
            print("No se pudo calcular una ruta entre esos puntos.")
            return None, None
            
    except Exception as e:
        print(f"Error al conectar con el servicio de rutas: {e}")
        return None, None

SALIDA="Victoria, Entre Rios, Argentina"    
destinos=[SALIDA]
distancia_total=0
def recorridos(parada,distancia_total):
    inicio=destinos[-1]
    distancia,tiempo=calcular_ruta_osrm(inicio,parada)
    destinos.append(parada)
    distancia_total+=distancia
    return distancia_total

def vuelta(distancia_total):
    km_vuelta,tiempo_vuelta=calcular_ruta_osrm(destinos[-1],SALIDA)
    distancia_total+=km_vuelta
    return km_vuelta,distancia_total