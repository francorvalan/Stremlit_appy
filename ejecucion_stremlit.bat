@echo off
REM Cambiar al directorio del script
cd /d "%~dp0"

REM Activar el entorno de Conda
call conda activate JM_wetlands

REM Ejecutar la aplicación Streamlit
streamlit run app.py
