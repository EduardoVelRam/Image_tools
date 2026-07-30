import streamlit as st
import importlib
import os

st.set_page_config(
    page_title="Herramientas para Imágenes",
    page_icon="🖼️",
    layout="wide"
)

st.title("Colección de Herramientas")

CARPETA = "tools"

archivos = []

for archivo in os.listdir(CARPETA):

    if archivo.endswith(".py") and archivo != "__init__.py":

        archivos.append(archivo[:-3])

archivos.sort()

opcion = st.sidebar.selectbox(

    "Selecciona una herramienta",

    archivos

)

modulo = importlib.import_module(f"{CARPETA}.{opcion}")

modulo.run()