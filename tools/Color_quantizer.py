import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

st.set_page_config(
    page_title="Color Quantizer",
    page_icon="🎨"
)

st.title("Color Quantizer")

st.write(
    "Reduce the quantity of colors of one image "
    "without using AI algorithms."
)

archivo = st.file_uploader(
    "Select one image",
    type=["png", "jpg", "jpeg", "bmp", "webp"]
)

if archivo is not None:

    imagen = Image.open(archivo).convert("RGB")

    st.subheader("Original Image")
    st.image(imagen, use_container_width=True)

    niveles = st.slider(
        "Number of levels for RGB channel",
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

    st.subheader("Quantized Image")
    st.image(resultado, use_container_width=True)

    buffer = BytesIO()

    resultado.save(
        buffer,
        format="PNG"
    )

    st.download_button(
        "Download image",
        buffer.getvalue(),
        "imagen_cuantizada.png",
        "image/png"
    )