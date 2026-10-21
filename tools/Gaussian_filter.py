import streamlit as st
import cv2
import numpy as np

from PIL import Image
from io import BytesIO


def run():

    st.title("Filtro Gaussiano")

    st.write(
        "Aplica un filtro gaussiano para suavizar una imagen. "
        "Puedes ajustar la intensidad del desenfoque y "
        "descargar el resultado."
    )

    # Cargar imagen
    archivo = st.file_uploader(
        "Selecciona una imagen",
        type=["png", "jpg", "jpeg", "bmp", "webp"]
    )

    if archivo is None:
        return

    # Abrir imagen
    imagen = Image.open(archivo).convert("RGB")

    img = np.array(imagen)

    st.subheader("Imagen original")

    st.image(
        imagen,
        use_container_width=True
    )

    st.divider()

    # Parámetros del filtro
    st.subheader("Configuración del filtro")

    intensidad = st.slider(
        "Intensidad del desenfoque",
        min_value=1,
        max_value=51,
        value=11,
        step=2,
        help=(
            "Valores mayores generan un desenfoque más intenso. "
            "El tamaño del kernel debe ser impar."
        )
    )

    sigma = st.slider(
        "Sigma (desviación estándar)",
        min_value=0.1,
        max_value=15.0,
        value=3.0,
        step=0.1,
        help=(
            "Controla la dispersión de la función gaussiana. "
            "Valores mayores producen un suavizado más intenso."
        )
    )

    # Aplicar filtro gaussiano
    resultado = cv2.GaussianBlur(
        img,
        (intensidad, intensidad),
        sigmaX=sigma,
        sigmaY=sigma
    )

    imagen_resultado = Image.fromarray(resultado)

    # Mostrar comparación
    st.subheader("Comparación")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            imagen,
            caption="Original",
            use_container_width=True
        )

    with col2:
        st.image(
            imagen_resultado,
            caption="Filtro gaussiano",
            use_container_width=True
        )

    # Descargar resultado
    buffer = BytesIO()

    imagen_resultado.save(
        buffer,
        format="PNG"
    )

    st.download_button(
        label="Descargar imagen procesada",
        data=buffer.getvalue(),
        file_name="imagen_filtro_gaussiano.png",
        mime="image/png"
    )


if __name__ == "__main__":
    run()