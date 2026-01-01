# Análisis Logístico del Litio en Salta 🇦🇷 (Lithium Logistics Analysis)

## 📖 Resumen / Abstract

### 🇪🇸 Español
Este proyecto implementa una herramienta de **Inteligencia Geoespacial (Geo-Intelligence)** para optimizar la logística de extracción de litio en la Puna Argentina. Utiliza Python para calcular distancias reales de transporte desde los principales proyectos mineros (como Mariana y Centenario Ratones) hacia el Nodo Logístico de Güemes, un punto estratégico para la exportación. El sistema identifica ineficiencias logísticas y propone clústeres de colaboración basándose en la proximidad geográfica.

### 🇺🇸 English
This project implements a **Geo-Intelligence** tool designed to optimize lithium extraction logistics in the Argentine Puna. It leverages Python to calculate real-world transport distances from major mining projects (e.g., Mariana, Centenario Ratones) to the Güemes Logistics Hub, a strategic export point. The system identifies logistical inefficiencies and proposes collaboration clusters based on geographic proximity.

---

## 🚀 Capacidades y Funcionalidades / Key Capabilities

*   **Cálculo de Rutas Reales (Real-world Routing)**: Integración con la API OSRM para calcular distancias de conducción (driving distances) precisas, superando las estimaciones lineales simples.
*   **Detección de Clústeres (Cluster Detection)**: Algoritmo espacial que identifica proyectos vecinos dentro de un radio configurable (ej. 50 km) para sugerir infraestructura compartida.
*   **Dashboard Interactivo (Interactive Dashboard)**: Interfaz web construida con Streamlit que permite a los tomadores de decisiones visualizar mapas, filtrar por radios de influencia y analizar KPIs y métricas en tiempo real.
*   **Visualización Geoespacial (Geospatial Visualization)**: Mapas dinámicos generados con Folium que muestran el estado crítico/estándar de la logística mediante codificación de colores.

## Stack Tecnológico / Tech Stack

Este proyecto demuestra el dominio de librerías avanzadas de análisis de datos y desarrollo web:

*   **Python 3.10+**: Lenguaje base.
*   **GeoPandas & Shapely**: Manipulación de datos espaciales y proyecciones cartográficas (WGS84 -> UTM Zone 19S).
*   **Streamlit**: Framework para la creación rápida de Data Apps interactivas.
*   **Folium & Streamlit-Folium**: Renderizado de mapas interactivos basados en Leaflet.js.
*   **Pandas**: Procesamiento y transformación de estructuras de datos.
*   **Matplotlib**: Generación de gráficos estáticos para reportes.
*   **Requests**: Consumo de APIs REST (OSRM) para datos de rutas.

## Instalación y Uso / Installation & Usage

1.  **Clonar el repositorio / Clone repository**:
    ```bash
    git clone https://github.com/tu-usuario/salta-lithium-logistics.git
    cd salta-lithium-logistics
    ```

2.  **Instalar dependencias / Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar la aplicación / Run the app**:
    ```bash
    streamlit run scripts/app.py
    ```

## Metodología Analítica / Analytical Methodology

**Proyección Cartográfica / Map Projection**:
Se utiliza `EPSG:32719` (UTM Zone 19S) para garantizar la precisión métrica en los cálculos de distancia dentro de la región de Salta, minimizando la distorsión inherente a las coordenadas geográficas (Lat/Lon).

**Lógica de Negocio / Business Logic**:
Se definen umbrales de criticidad logística (> 350 km) para alertar sobre costos de transporte elevados. La validación de rutas incluye un mecanismo de "fallback" matemático lineal en caso de fallos en el servicio de rutas externo.
