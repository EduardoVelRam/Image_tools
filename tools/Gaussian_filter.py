import streamlit as st
import cv2
import numpy as np

from PIL import Image
from io import BytesIO


def run():

    st.title("Gaussian Filter")

    st.write(
        "Applies a Gaussian filter to smooth an image. "
        "You can adjust the intensity of the blur and "
        "download the result."
    )

    # Cargar imagen
    archivo = st.file_uploader(
        "Select an image to process",
        type=["png", "jpg", "jpeg", "bmp", "webp"]
    )

    if archivo is None:
        return

    # Abrir imagen
    imagen = Image.open(archivo).convert("RGB")

    img = np.array(imagen)

    st.subheader("Original Image")

    st.image(
        imagen,
        use_container_width=True
    )

    st.divider()

    # Parámetros del filtro
    st.subheader("Filter Configuration")

    intensidad = st.slider(
        "Blur Intensity (Kernel Size)",
        min_value=1,
        max_value=51,
        value=11,
        step=2,
        help=(
            "Higher values generate a more intense blur. "
            "The kernel size must be odd."
        )
    )

    sigma = st.slider(
        "Sigma (standard deviation)",
        min_value=0.1,
        max_value=15.0,
        value=3.0,
        step=0.1,
        help=(
            "Controls the spread of the Gaussian function. "
            "Higher values produce a more intense smoothing."
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
    st.subheader("Comparison")

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
            caption="Gaussian Filter",
            use_container_width=True
        )

    # Descargar resultado
    buffer = BytesIO()

    imagen_resultado.save(
        buffer,
        format="PNG"
    )

    st.download_button(
        label="Download Processed Image",
        data=buffer.getvalue(),
        file_name="imagen_filtro_gaussiano.png",
        mime="image/png"
    )


if __name__ == "__main__":
    run()