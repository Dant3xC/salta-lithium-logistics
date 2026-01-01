import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt

# Importar la logica de negocio del script main.py
from main import load_data, create_geodataframe, calculate_distances, DATA_PATH, GUEMES_COORDS, PROXIMITY_THRESHOLD_KM

# Configuración de la página
st.set_page_config(
    page_title="Tablero Logístico de Litio",
    page_icon="🔋",
    layout="wide"
)

# Título y Descripción
st.title("🔋 Dashboard de Logística del Litio - Salta")
st.markdown("""
Este tablero interactivo permite analizar la ubicación de proyectos de litio, 
su distancia a nodos logísticos clave y potenciales clústeres de colaboración.
""")

# Sidebar para controles
st.sidebar.header("Configuración")
radio_cluster = st.sidebar.slider("Radio de posible colaboración (km)", 10, 100, PROXIMITY_THRESHOLD_KM)
mostrar_radio = st.sidebar.checkbox("Mostrar radios de influencia", value=True)

# Carga de Datos
try:
    df = load_data(DATA_PATH)
    gdf = create_geodataframe(df)
    dist_series, gdf_metros = calculate_distances(gdf, GUEMES_COORDS)
    gdf["Distancia a Guemes (km)"] = dist_series
except Exception as e:
    st.error(f"Error cargando datos: {e}")
    st.stop()

# Métricas Clave (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Proyectos", len(gdf))
with col2:
    st.metric("Distancia Promedio a Güemes", f"{gdf['Distancia a Guemes (km)'].mean():.1f} km")
with col3:
    # Contar críticas
    criticas = len(gdf[gdf['Distancia al parque industrial Güemes (km)'] > 300])
    st.metric("Logística Crítica (>300km)", criticas, delta_color="inverse")

# Mapa Interactivo
st.subheader("📍 Mapa Geoespacial")

m = folium.Map(location=[-24.7, -66.5], zoom_start=7, tiles="OpenStreetMap")

# Nodo Güemes
folium.Marker(
    location=GUEMES_COORDS,
    popup="<b>Nodo Logístico Güemes</b>",
    icon=folium.Icon(color='red', icon='truck', prefix='fa')
).add_to(m)

# Proyectos
for _, row in gdf.iterrows():
    dist = row["Distancia a Guemes (km)"]
    color = "orange" if dist > 300 else "green"
    
    # Marcador
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f"<b>{row['Proyecto']}</b><br>{dist:.1f} km a Güemes",
        icon=folium.Icon(color=color, icon='bolt', prefix='fa')
    ).add_to(m)
    
    # Radio variable 
    if mostrar_radio:
        folium.Circle(
            location=[row.geometry.y, row.geometry.x],
            radius=radio_cluster * 1000,
            color=color,
            fill=True,
            fill_opacity=0.05
        ).add_to(m)

# Renderizar mapa en Streamlit
folium_static(m)

# Tabla de Datos y Gráficos
col_tabla, col_grafico = st.columns([1, 1])

with col_tabla:
    st.subheader("Datos Detallados")
    st.dataframe(gdf[["Proyecto", "Empresa", "Salar", "Distancia al parque industrial Güemes (km)"]].sort_values("Distancia al parque industrial Güemes (km)"))

with col_grafico:
    st.subheader("Comparativa de Distancias")
    fig, ax = plt.subplots()
    bars = ax.barh(gdf["Proyecto"], gdf["Distancia al parque industrial Güemes (km)"])
    ax.set_xlabel("Distancia al parque industrial Güemes (km)")
    ax.set_title("Proyectos ordenados por distancia")
    
    # Destacar barras largas
    for bar, dist in zip(bars, gdf["Distancia al parque industrial Güemes (km)"]):
        if dist > 300:
            bar.set_color("#FF9800")
            
    st.pyplot(fig)

st.success("Análisis generado dinámicamente.")
