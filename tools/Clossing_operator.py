import streamlit as st
import cv2
import numpy as np

from PIL import Image
from io import BytesIO


def run():
    st.title("Operador morfológico de Cerradura")

    st.write(
        """
        Aplica el operador morfológico de cerradura (*Closing*) para
        cerrar pequeños agujeros, unir regiones cercanas y eliminar
        espacios estrechos en una imagen.
        """
    )

    # --------------------------------------------------
    # Cargar imagen
    # --------------------------------------------------
    archivo = st.file_uploader(
        "Selecciona una imagen",
        type=["png", "jpg", "jpeg", "bmp", "webp"]
    )

    if archivo is None:
        return

    imagen = Image.open(archivo).convert("RGB")
    img = np.array(imagen)

    # --------------------------------------------------
    # Mostrar imagen original
    # --------------------------------------------------
    st.subheader("Imagen original")
    st.image(imagen, caption="Imagen de entrada", width="stretch")

    st.divider()

    # --------------------------------------------------
    # Configuración del operador
    # --------------------------------------------------
    st.subheader("Configuración del operador")

    forma_kernel = st.selectbox(
        "Forma del elemento estructurante",
        options=["Rectangular", "Elíptico", "Cruz"],
        index=0
    )

    tamano_kernel = st.slider(
        "Tamaño del kernel",
        min_value=1,
        max_value=51,
        value=5,
        step=2,
        help="Un kernel mayor puede cerrar espacios más grandes."
    )

    iteraciones = st.slider(
        "Número de iteraciones",
        min_value=1,
        max_value=5,
        value=1,
        step=1,
        help="Aumentar las iteraciones intensifica el efecto morfológico."
    )

    # --------------------------------------------------
    # Crear elemento estructurante
    # --------------------------------------------------
    formas = {
        "Rectangular": cv2.MORPH_RECT,
        "Elíptico": cv2.MORPH_ELLIPSE,
        "Cruz": cv2.MORPH_CROSS
    }

    kernel = cv2.getStructuringElement(
        formas[forma_kernel],
        (tamano_kernel, tamano_kernel)
    )

    # --------------------------------------------------
    # Aplicar cerradura morfológica
    # --------------------------------------------------
    resultado = cv2.morphologyEx(
        img,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=iteraciones
    )

    imagen_resultado = Image.fromarray(resultado)

    # --------------------------------------------------
    # Mostrar kernel
    # --------------------------------------------------
    st.subheader("Elemento estructurante")

    kernel_visual = (kernel * 255).astype(np.uint8)

    st.image(
        kernel_visual,
        caption=f"Kernel {forma_kernel.lower()} de {tamano_kernel} × {tamano_kernel}",
        width=200
    )

    # --------------------------------------------------
    # Comparación de resultados
    # --------------------------------------------------
    st.subheader("Comparación de resultados")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            imagen,
            caption="Imagen original",
            width="stretch"
        )

    with col2:
        st.image(
            imagen_resultado,
            caption="Imagen después de la cerradura",
            width="stretch"
        )

    # --------------------------------------------------
    # Descargar resultado
    # --------------------------------------------------
    buffer = BytesIO()
    imagen_resultado.save(buffer, format="PNG")

    st.download_button(
        label="Descargar imagen procesada",
        data=buffer.getvalue(),
        file_name="imagen_cerradura_morfologica.png",
        mime="image/png"
    )


if __name__ == "__main__":
    run()