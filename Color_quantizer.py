import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

st.set_page_config(
    page_title="Cuantizador de Colores",
    page_icon="🎨"
)

st.title("🎨 Cuantizador de Colores")

st.write(
    "Reduce la cantidad de colores de una imagen "
    "sin utilizar algoritmos de IA."
)

archivo = st.file_uploader(
    "Selecciona una imagen",
    type=["png", "jpg", "jpeg", "bmp", "webp"]
)

if archivo is not None:

    imagen = Image.open(archivo).convert("RGB")

    st.subheader("Imagen Original")
    st.image(imagen, use_container_width=True)

    niveles = st.slider(
        "Número de niveles por canal RGB",
        min_value=2,
        max_value=256,
        value=8,
        step=2
    )

    img = np.array(imagen).astype(np.float32)

    paso = 255 / (niveles - 1)

    cuantizada = np.round(img / paso) * paso

    cuantizada = np.clip(cuantizada, 0, 255)

    cuantizada = cuantizada.astype(np.uint8)

    resultado = Image.fromarray(cuantizada)

    st.subheader("Imagen Cuantizada")
    st.image(resultado, use_container_width=True)

    buffer = BytesIO()

    resultado.save(
        buffer,
        format="PNG"
    )

    st.download_button(
        "⬇️ Descargar imagen",
        buffer.getvalue(),
        "imagen_cuantizada.png",
        "image/png"
    )