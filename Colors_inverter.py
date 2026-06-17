import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

st.set_page_config(
    page_title="Inversor de Colores",
    page_icon="🎨"
)

st.title("🎨 Inversor de Colores")

archivo = st.file_uploader(
    "Selecciona una imagen",
    type=["png", "jpg", "jpeg", "bmp", "gif", "webp"]
)

if archivo is not None:

    imagen = Image.open(archivo)

    st.subheader("Imagen Original")
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

    st.subheader("Imagen Invertida")
    st.image(imagen_invertida, use_container_width=True)

    buffer = BytesIO()

    imagen_invertida.save(
        buffer,
        format="PNG"
    )

    st.download_button(
        label="⬇️ Descargar Imagen Invertida",
        data=buffer.getvalue(),
        file_name="imagen_invertida.png",
        mime="image/png"
    )