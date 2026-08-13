import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

st.set_page_config(
    page_title="Blanco y Azul",
    page_icon="🔵"
)

st.title("Conversor Blanco y Azul")

archivo = st.file_uploader(
    "Selecciona una imagen",
    type=["png", "jpg", "jpeg", "bmp", "webp"]
)

if archivo is not None:

    imagen = Image.open(archivo).convert("L")

    st.subheader("Imagen original")

    st.image(
        imagen,
        use_container_width=True
    )

    # Convertir imagen a NumPy
    gris = np.array(imagen).astype(np.float32)

    # -----------------------------------------
    # Color azul seleccionado por el usuario
    # -----------------------------------------

    st.subheader("Configuración")

    azul = st.color_picker(
        "Selecciona el color azul",
        "#0057B8"
    )

    # Convertir HEX a RGB
    azul = azul.lstrip("#")

    azul_r = int(azul[0:2], 16)
    azul_g = int(azul[2:4], 16)
    azul_b = int(azul[4:6], 16)

    # -----------------------------------------
    # Crear imagen
    # -----------------------------------------

    resultado = np.zeros(
        (gris.shape[0], gris.shape[1], 3),
        dtype=np.uint8
    )

    intensidad = gris / 255.0

    # Negro -> azul
    # Blanco -> blanco

    resultado[:, :, 0] = (
        azul_r * (1 - intensidad) +
        255 * intensidad
    )

    resultado[:, :, 1] = (
        azul_g * (1 - intensidad) +
        255 * intensidad
    )

    resultado[:, :, 2] = (
        azul_b * (1 - intensidad) +
        255 * intensidad
    )

    resultado = resultado.astype(np.uint8)

    imagen_final = Image.fromarray(
        resultado
    )

    st.subheader("Resultado")

    st.image(
        imagen_final,
        use_container_width=True
    )

    # -----------------------------------------
    # Descargar
    # -----------------------------------------

    buffer = BytesIO()

    imagen_final.save(
        buffer,
        format="PNG"
    )

    st.download_button(
        label="Descargar imagen",
        data=buffer.getvalue(),
        file_name="imagen_blanco_azul.png",
        mime="image/png"
    )