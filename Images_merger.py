import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

st.set_page_config(
    page_title="Image merger",
    page_icon="🖼️",
    layout="wide"
)

st.title("Image merger")

col1, col2 = st.columns(2)

with col1:
    archivo1 = st.file_uploader(
        "Image A",
        type=["png", "jpg", "jpeg", "bmp", "webp"],
        key="img1"
    )

with col2:
    archivo2 = st.file_uploader(
        "Image B",
        type=["png", "jpg", "jpeg", "bmp", "webp"],
        key="img2"
    )

if archivo1 and archivo2:

    img1 = Image.open(archivo1).convert("RGB")
    img2 = Image.open(archivo2).convert("RGB")

    ancho = min(img1.width, img2.width)
    alto = min(img1.height, img2.height)

    img1 = img1.resize((ancho, alto))
    img2 = img2.resize((ancho, alto))

    np1 = np.array(img1)
    np2 = np.array(img2)

    porcentaje = st.slider(
        "Image A contribution (%)",
        min_value=0,
        max_value=100,
        value=50
    )

    alpha = porcentaje / 100
    beta = 1 - alpha

    mezcla = cv2.addWeighted(
        np1,
        alpha,
        np2,
        beta,
        0
    )

    imagen_resultado = Image.fromarray(mezcla)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Image A")
        st.image(img1)

    with col2:
        st.subheader("Image B")
        st.image(img2)

    with col3:
        st.subheader("Result")
        st.image(imagen_resultado)

    buffer = BytesIO()

    imagen_resultado.save(
        buffer,
        format="PNG"
    )

    st.download_button(
        label="Download result",
        data=buffer.getvalue(),
        file_name="imagen_combinada.png",
        mime="image/png"
    )