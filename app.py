import streamlit as st
import pandas as pd
import geopandas as gpd
from pyproj import CRS
from io import BytesIO
import folium
from streamlit_folium import st_folium

# streamlit run app.py
# Diccionario de sistemas de referencia
crs_dict = {
    "Latitud y longitud": 4326,
    "Posgar 94, Faja 2": 22182,
    "Posgar 94, Faja 3": 22183,
    "Posgar 94, Faja 1": 22181
}

# 1. Cargar archivo Excel
st.title("Aplicación de Transformación de Coordenadas")
uploaded_file = st.file_uploader("Sube un archivo Excel", type="xlsx")



if uploaded_file:
    # Cargar el archivo Excel
    df = pd.read_excel(uploaded_file, decimal=',')
    st.write("Datos cargados:")
    st.write(df.head())

    # Selección de columnas para X y Y
    x_col = st.selectbox("Selecciona la columna para X", df.columns, key="x_col_select")
    y_col = st.selectbox("Selecciona la columna para Y", df.columns, key="y_col_select")
    id_col = st.selectbox("Selecciona la columna del Nombre del Sitio", df.columns, key="id_col_select")
    
    # Limpieza de datos en columnas seleccionadas: eliminar caracteres no numéricos
    df[x_col] = df[x_col].replace(r'[^\d,.-]', '', regex=True).replace('', pd.NA)
    df[y_col] = df[y_col].replace(r'[^\d,.-]', '', regex=True).replace('', pd.NA)

    # Convertir las columnas seleccionadas a numérico, sin afectar otras columnas
    df[x_col] = pd.to_numeric(df[x_col], errors='coerce')
    df[y_col] = pd.to_numeric(df[y_col], errors='coerce')

    # Filtrar filas que no tengan NA en las columnas seleccionadas para X e Y
    df = df.dropna(subset=[x_col, y_col])
    

    
    # Selección del CRS de origen y destino
    crs_origen = st.selectbox("Selecciona el sistema de referencia de origen", options=list(crs_dict.keys()), key="crs_origen")
    crs_destino = st.selectbox("Selecciona el sistema de referencia de destino", options=list(crs_dict.keys()), key="crs_destino")

    # Crear un GeoDataFrame con los datos de coordenadas y el CRS de origen
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[x_col], df[y_col]), crs=f"EPSG:{crs_dict[crs_origen]}")
    
    # Reproyectar al CRS de destino
    gdf = gdf.to_crs(f"EPSG:{crs_dict[crs_destino]}")
    
    # Agregar las nuevas coordenadas reproyectadas al DataFrame original
    df['X_transformado'] = gdf.geometry.x
    df['Y_transformado'] = gdf.geometry.y

    st.write("Datos transformados:")
    st.write(df.head())

    # Visualizar en mapa interactivo
    st.subheader("Mapa interactivo de los puntos transformados")
    centro_mapa = [gdf.geometry.y.mean(), gdf.geometry.x.mean()]
    mapa = folium.Map(location=centro_mapa, zoom_start=4)
    
    # Añadir marcadores con popups
    for _, row in gdf.iterrows():
        popup_text = f"{row[id_col]}"  # Utiliza la columna seleccionada como popup
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=popup_text
        ).add_to(mapa)
    
    # Mostrar el mapa en Streamlit
    st_folium(mapa, width=700, height=500)

    # Descargar el DataFrame con coordenadas transformadas
    output = BytesIO()  # Crear un objeto BytesIO para el archivo en memoria
    df.to_excel(output, index=False, engine='openpyxl')  # Escribir el DataFrame en el objeto BytesIO
    output.seek(0)  # Volver al principio del objeto

    st.download_button(
        label="Descargar datos con coordenadas transformadas",
        data=output,
        file_name="datos_transformados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
