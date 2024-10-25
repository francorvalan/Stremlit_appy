import streamlit as st
import pandas as pd
import geopandas as gpd
from pyproj import CRS
from io import BytesIO
import folium
from streamlit_folium import st_folium

from io import BytesIO

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

# if uploaded_file:
#     # Cargar el archivo Excel
#     df = pd.read_excel(uploaded_file, decimal=',')
#     st.write("Datos cargados:")
#     st.write(df.head())

#     # # Selección de columnas para X y Y
#     # x_col = st.selectbox("Selecciona la columna para X", df.columns, key="x_col_select")
#     # y_col = st.selectbox("Selecciona la columna para Y", df.columns, key="y_col_select")

#     # # Convertir todas las columnas a numérico donde sea posible, reemplazando errores por NaN
#     # df = df.apply(pd.to_numeric, errors='coerce')

#     # # Filtrar filas que no tengan NA en las columnas seleccionadas para X e Y
#     # df = df.dropna(subset=[x_col, y_col])
#     # Selección de columnas para X y Y con claves únicas
#     x_col = st.selectbox("Selecciona la columna para X", df.columns, key="x_col_select")
#     y_col = st.selectbox("Selecciona la columna para Y", df.columns, key="y_col_select")

#     # Limpieza de datos en columnas seleccionadas: eliminar caracteres no numéricos
#     df[x_col] = df[x_col].replace(r'[^\d,.-]', '', regex=True).replace('', pd.NA)
#     df[y_col] = df[y_col].replace(r'[^\d,.-]', '', regex=True).replace('', pd.NA)

#     # Convertir las columnas seleccionadas a numérico, sin afectar otras columnas
#     df[x_col] = pd.to_numeric(df[x_col], errors='coerce')
#     df[y_col] = pd.to_numeric(df[y_col], errors='coerce')

#     # Filtrar filas que no tengan NA en las columnas seleccionadas para X e Y
#     df = df.dropna(subset=[x_col, y_col])
    
#     st.write("Datos después de limpieza:")
#     st.write(df.head())

#     # 2. Selección de columnas para X y Y
#     x_col = st.selectbox("Selecciona la columna para X", df.columns)
#     y_col = st.selectbox("Selecciona la columna para Y", df.columns)

#     # 3. Sistema de referencia original
#     crs_origen_name = st.selectbox("Sistema de referencia de origen", list(crs_dict.keys()))
#     crs_origen = crs_dict[crs_origen_name]

#     # 4. Sistema de referencia de destino
#     crs_destino_name = st.selectbox("Sistema de referencia de destino", list(crs_dict.keys()))
#     crs_destino = crs_dict[crs_destino_name]

#     # Transformación y reproyección
#     if st.button("Transformar y re-proyectar"):
#         # Crear el GeoDataFrame a partir de los datos cargados
#         gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[x_col], df[y_col]), crs=CRS.from_epsg(crs_origen))

#         # 5. Reproyectar al CRS de destino
#         gdf = gdf.to_crs(epsg=crs_destino)

#         # 6. Extraer nuevas coordenadas y añadirlas al DataFrame original
#         df['X_nuevo'] = gdf.geometry.x
#         df['Y_nuevo'] = gdf.geometry.y

#         # 7. Mostrar el GeoDataFrame re-proyectado
#         st.write("Datos transformados:")
#         st.write(df.head())

#         # 8. Visualizar en mapa interactivo
#         st.subheader("Mapa interactivo de los puntos transformados")
#         centro_mapa = [gdf.geometry.y.mean(), gdf.geometry.x.mean()]
#         mapa = folium.Map(location=centro_mapa, zoom_start=5)
#         for _, row in gdf.iterrows():
#             folium.Marker(location=[row.geometry.y, row.geometry.x]).add_to(mapa)
#         st_folium(mapa, width=700, height=500)

#         # 9. Descargar el DataFrame con las nuevas coordenadas
#         output = BytesIO()
#         df.to_excel(output, index=False)
#         output.seek(0)
#         st.download_button(
#             label="Descargar Excel con nuevas coordenadas",
#             data=output,
#             file_name="datos_transformados.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )


####################################### Version B: funciona muy bien, no exporta el excel ###############
# if uploaded_file:
#     # Cargar el archivo Excel
#     df = pd.read_excel(uploaded_file, decimal=',')
#     st.write("Datos cargados:")
#     st.write(df.head())

#     # Selección de columnas para X y Y con claves únicas
#     x_col = st.selectbox("Selecciona la columna para X", df.columns, key="x_col_select")
#     y_col = st.selectbox("Selecciona la columna para Y", df.columns, key="y_col_select")

#     # Limpieza de datos en columnas seleccionadas: eliminar caracteres no numéricos
#     df[x_col] = df[x_col].replace(r'[^\d,.-]', '', regex=True).replace('', pd.NA)
#     df[y_col] = df[y_col].replace(r'[^\d,.-]', '', regex=True).replace('', pd.NA)

#     # Convertir las columnas seleccionadas a numérico, sin afectar otras columnas
#     df[x_col] = pd.to_numeric(df[x_col], errors='coerce')
#     df[y_col] = pd.to_numeric(df[y_col], errors='coerce')

#     # Filtrar filas que no tengan NA en las columnas seleccionadas para X e Y
#     df = df.dropna(subset=[x_col, y_col])
    
#     st.write("Datos después de limpieza:")
#     st.write(df.head())
    
#     # Selección del CRS de origen y destino usando el diccionario
#     crs_origen = st.selectbox("Selecciona el sistema de referencia de origen", options=list(crs_dict.keys()), key="crs_origen")
#     crs_destino = st.selectbox("Selecciona el sistema de referencia de destino", options=list(crs_dict.keys()), key="crs_destino")

#     # Crear un GeoDataFrame con los datos de coordenadas y el CRS de origen
#     gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[x_col], df[y_col]), crs=f"EPSG:{crs_dict[crs_origen]}")
    
#     # Reproyectar al CRS de destino
#     gdf = gdf.to_crs(f"EPSG:{crs_dict[crs_destino]}")
    
#     # Agregar las nuevas coordenadas reproyectadas al DataFrame original
#     df['X_transformado'] = gdf.geometry.x
#     df['Y_transformado'] = gdf.geometry.y

#     # Visualizar en mapa interactivo
#     st.subheader("Mapa interactivo de los puntos transformados")
#     centro_mapa = [gdf.geometry.y.mean(), gdf.geometry.x.mean()]
#     mapa = folium.Map(location=centro_mapa, zoom_start=5)
#     for _, row in gdf.iterrows():
#         folium.Marker(location=[row.geometry.y, row.geometry.x]).add_to(mapa)
#     st_folium(mapa, width=700, height=500)

#     # Descargar el DataFrame con coordenadas transformadas
#     st.download_button(
#         label="Descargar datos con coordenadas transformadas",
#         data=df.to_excel(index=False, engine='openpyxl'),
#         file_name="datos_transformados.xlsx",
#         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )


import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import streamlit as st
from io import BytesIO

# Diccionario de sistemas de referencia
# crs_dict = {
#     "Latitud y longitud": 4326,
#     "Posgar 94, Faja 2": 22182
# }

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
