import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

st.set_page_config(
    page_title="Color Inverter",
    page_icon="🎨"
)

st.title("Color Inverter")

archivo = st.file_uploader(
    "Select an image",
    type=["png", "jpg", "jpeg", "bmp", "gif", "webp"]
)

if archivo is not None:

    imagen = Image.open(archivo)

    st.subheader("Original Image")
    st.image(imagen, use_container_width=True)

    img_np = np.array(imagen)

    # Invertir colores
    if len(img_np.shape) == 3:
        img_invertida = 255 - img_np
    else:
        img_invertida = 255 - img_np

    imagen_invertida = Image.fromarray(
        img_invertida.astype(np.uint8)
    )

    st.subheader("Inverted Image")
    st.image(imagen_invertida, use_container_width=True)

    buffer = BytesIO()

    imagen_invertida.save(
        buffer,
        format="PNG"
    )

    st.download_button(
        label="Download Inverted Image",
        data=buffer.getvalue(),
        file_name="imagen_invertida.png",
        mime="image/png"
    )