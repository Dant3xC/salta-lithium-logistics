import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium
import os

# Constantes
PROJECTION_CRS = "EPSG:32719"  # UTM Zone 19S
GEOGRAPHIC_CRS = "EPSG:4326"   # WGS84
GUEMES_COORDS = (-24.6932, -65.0435)  # Lat, Lon
CRITICAL_DISTANCE_KM = 300
PROXIMITY_THRESHOLD_KM = 50
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'proyectos.csv')
OUTPUT_MAP = "mapa_litio_final.html"

def load_data(path):
    #Carga los datos de proyectos desde un CSV.
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo de datos: {path}")
    return pd.read_csv(path)

def create_geodataframe(df):
    #Convierte el DataFrame en un GeoDataFrame.
    # GeoPandas usa (Longitud, Latitud) -> (X, Y)
    geometry = [Point(xy) for xy in zip(df["Longitud"], df["Latitud"])]
    return gpd.GeoDataFrame(df, geometry=geometry, crs=GEOGRAPHIC_CRS)

def calculate_distances(gdf, target_point_coords):
    #Calcula la distancia de cada proyecto a un punto objetivo (Güemes).
    # Proyectar a UTM para cálculos métricos precisos
    gdf_metros = gdf.to_crs(PROJECTION_CRS)
     
    # Crear punto objetivo en el mismo sistema
    target_point = Point(target_point_coords[1], target_point_coords[0]) # Lon, Lat
    target_series = gpd.GeoSeries([target_point], crs=GEOGRAPHIC_CRS)
    target_metros = target_series.to_crs(PROJECTION_CRS).iloc[0]
    
    # Calcular distancia
    gdf_metros["Distancia a Guemes (km)"] = gdf_metros.geometry.distance(target_metros) / 1000
    
    # Devuelve la columna de distancias 
    return gdf_metros["Distancia a Guemes (km)"], gdf_metros

def analyze_proximity(gdf_metros, threshold_km):
    #Analiza y muestra proyectos cercanos 
    print(f"\n--- ANÁLISIS DE COLABORACIÓN (Radio {threshold_km}km) ---")
    for i, row in gdf_metros.iterrows():
        distances = gdf_metros.geometry.distance(row.geometry) / 1000
        nearby = gdf_metros[(distances <= threshold_km) & (gdf_metros.index != i)]
        
        if not nearby.empty:
            print(f"Proyecto: {row['Proyecto']} tiene vecinos potenciales:")
            for j, nearby_row in nearby.iterrows():
                dist = row.geometry.distance(nearby_row.geometry) / 1000
                print(f"   -> {nearby_row['Proyecto']} a {dist:.2f} km")

def generate_map(gdf, target_point_coords):
    #Genera un mapa interactivo con Folium
    # Centrar el mapa aproximadamente en el promedio de las coordenadas 
    map_center = folium.Map(location=[-24.7, -66.5], zoom_start=8, tiles="OpenStreetMap")
    
    # Agregar Nodo Logístico Güemes
    folium.Marker(
        location=target_point_coords,
        popup="<b>Nodo Logístico Güemes</b><br>Parque Industrial",
        icon=folium.Icon(color='red', icon='truck', prefix='fa')
    ).add_to(map_center)

    for _, row in gdf.iterrows():
        distancia = row["Distancia a Guemes (km)"]
        
        # Determinar estilo basado en la distancia
        if distancia > CRITICAL_DISTANCE_KM:
            color_marker = "orange" 
            estado_logistica = "Crítica (>300 km)"
        else:
            color_marker = "green"
            estado_logistica = "Estándar (<=300 km)"
            
        # Contenido del Popup
        popup_content = (
            f"<b>{row['Proyecto']}</b><br>"
            f"Empresa: {row['Empresa']}<br>"
            f"Salar: {row['Salar']}<br>"
            f"Logística: {estado_logistica}<br>"
            f"Distancia: {distancia:.1f} km"
        )
        
        # Marcador único
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=popup_content,
            icon=folium.Icon(color=color_marker, icon='hammer', prefix='fa')
        ).add_to(map_center)
        
        # Círculo de influencia (50km)
        folium.Circle(
            location=[row.geometry.y, row.geometry.x],
            radius=PROXIMITY_THRESHOLD_KM * 1000,
            color=color_marker,
            fill=True,
            fill_opacity=0.1,
            popup=f"Radio de influencia {row['Proyecto']}"
        ).add_to(map_center)
        
    map_path = os.path.join(os.path.dirname(__file__), '..', OUTPUT_MAP)
    map_center.save(map_path)
    print(f"\nMapa guardado en: {os.path.abspath(map_path)}")

def main():
    print("Iniciando análisis logístico de litio...")
    
    # Cargar Datos
    try:
        df = load_data(DATA_PATH)
    except FileNotFoundError as e:
        print(e)
        return

    # Crear GeoDataFrame
    gdf = create_geodataframe(df)
    
    # Calcular Distancias
    dist_series, gdf_metros = calculate_distances(gdf, GUEMES_COORDS)
    gdf["Distancia a Guemes (km)"] = dist_series
    
    # Reporte de distancias
    print("\n--- DISTANCIAS AL NODO LOGÍSTICO (GÜEMES) ---")
    print(gdf[["Proyecto", "Distancia a Guemes (km)"]])
    
    # Análisis de Clustering
    analyze_proximity(gdf_metros, PROXIMITY_THRESHOLD_KM)
    
    # Generar Mapa
    generate_map(gdf, GUEMES_COORDS)
    print("\nProceso finalizado con éxito.")

if __name__ == "__main__":
    main()