import streamlit as st
import cv2
import numpy as np

from PIL import Image
from io import BytesIO


def run():
    st.title("Opening Morphological Operator")

    st.write(
        """
        Applies the morphological opening operator (*Opening*) to
        remove small objects, reduce noise, and suppress
        isolated regions in an image.
        """
    )

    # Cargar imagen
    archivo = st.file_uploader(
        "Select an image to process",
        type=["png", "jpg", "jpeg", "bmp", "webp"]
    )

    if archivo is None:
        return

    imagen = Image.open(archivo).convert("RGB")
    img = np.array(imagen)

   
    # Mostrar imagen original
    st.subheader("Original Image")
    st.image(
        imagen,
        caption="Input Image",
        width="stretch"
    )

    st.divider()

    # Configuración del operador
    st.subheader("Operator Configuration")

    forma_kernel = st.selectbox(
        "Shape of the structuring element",
        options=["Rectangular", "Elíptico", "Cruz"],
        index=0
    )

    tamano_kernel = st.slider(
        "Size of the kernel",
        min_value=1,
        max_value=51,
        value=5,
        step=2,
        help=(
            "A larger kernel allows removing larger objects, "
            "but it may also remove details from the image."
        )
    )

    iteraciones = st.slider(
        "Number of iterations",
        min_value=1,
        max_value=5,
        value=1,
        step=1,
        help=(
            "Increasing the number of iterations can intensify "
            "the effect of opening."
        )
    )

    # Crear elemento estructurante
    formas = {
        "Rectangular": cv2.MORPH_RECT,
        "Elíptico": cv2.MORPH_ELLIPSE,
        "Cruz": cv2.MORPH_CROSS
    }

    kernel = cv2.getStructuringElement(
        formas[forma_kernel],
        (tamano_kernel, tamano_kernel)
    )

    # Aplicar apertura morfológica
    resultado = cv2.morphologyEx(
        img,
        cv2.MORPH_OPEN,
        kernel,
        iterations=iteraciones
    )

    imagen_resultado = Image.fromarray(resultado)

    # Mostrar elemento estructurante
    st.subheader("Structuring Element")

    kernel_visual = (kernel * 255).astype(np.uint8)

    st.image(
        kernel_visual,
        caption=(
            f"Kernel {forma_kernel.lower()} de "
            f"{tamano_kernel} × {tamano_kernel}"
        ),
        width=200
    )

    # Comparación de resultados
    st.subheader("Comparison of Results")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            imagen,
            caption="Original Image",
            width="stretch"
        )

    with col2:
        st.image(
            imagen_resultado,
            caption="Image after Opening",
            width="stretch"
        )

    # Descargar resultado
    buffer = BytesIO()
    imagen_resultado.save(buffer, format="PNG")

    st.download_button(
        label="Download Processed Image",
        data=buffer.getvalue(),
        file_name="imagen_apertura_morfologica.png",
        mime="image/png"
    )


if __name__ == "__main__":
    run()