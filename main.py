import streamlit as st
import importlib
import os

st.set_page_config(
    page_title="Image Tools",
    layout="wide"
)

st.title("Image Tools Collection")

CARPETA = "tools"

archivos = []

for archivo in os.listdir(CARPETA):

    if archivo.endswith(".py") and archivo != "__init__.py":

        archivos.append(archivo[:-3])

archivos.sort()

opcion = st.sidebar.selectbox(

    "Select one tool",

    archivos

)

modulo = importlib.import_module(f"{CARPETA}.{opcion}")

modulo.run()