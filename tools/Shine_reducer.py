
import streamlit as st
import cv2
import numpy as np
from pathlib import Path
from PIL import Image
from io import BytesIO


@st.cache_resource

def cargar_detector():
    ruta = (
        Path(__file__).resolve().parent.parent
        / "models"
        / "haarcascade_frontalface_default.xml"
    )

    if not ruta.is_file():
        raise FileNotFoundError(
            f"No se encontró el clasificador facial: {ruta}"
        )

    detector = cv2.CascadeClassifier(str(ruta))

    if detector.empty():
        raise RuntimeError(
            f"OpenCV encontró el archivo, pero no pudo cargarlo: {ruta}"
        )

    return detector



def reducir_brillo(imagen, factor):
    """
    Reduce el brillo multiplicando los valores de intensidad RGB.
    factor = 1.0: brillo original.
    factor = 0.5: aproximadamente la mitad de la intensidad.
    factor = 0.0: imagen negra.
    """
    resultado = imagen.astype(np.float32) * factor
    return np.clip(resultado, 0, 255).astype(np.uint8)


def run():
    st.title("Reductor de brillo facial")

    st.write(
        """
        Reduce el brillo de una imagen completa o solamente del rostro
        detectado. Puedes ajustar la intensidad y comparar los resultados.
        """
    )

    archivo = st.file_uploader(
        "Selecciona una fotografía",
        type=["png", "jpg", "jpeg", "bmp", "webp"]
    )

    if archivo is None:
        return

    imagen_pil = Image.open(archivo).convert("RGB")
    imagen = np.array(imagen_pil)

    st.subheader("Imagen original")
    st.image(imagen_pil, width="stretch")

    st.divider()

    # Configuración
    st.subheader("Configuración")

    modo = st.radio(
        "Área de aplicación",
        options=[
            "Imagen completa",
            "Solo el rostro"
        ],
        horizontal=True
    )

    intensidad = st.slider(
        "Reducción del brillo (%)",
        min_value=0,
        max_value=90,
        value=30,
        step=5,
        help="Un valor mayor produce una imagen más oscura."
    )

    factor = 1.0 - intensidad / 100.0

    # Aplicar el filtro
    if modo == "Imagen completa":
        resultado = reducir_brillo(imagen, factor)

    else:
        detector = cargar_detector()

        # OpenCV utiliza BGR; la imagen de entrada está en RGB.
        imagen_bgr = cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)
        gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)

        rostros = detector.detectMultiScale(
            gris,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(40, 40)
        )

        resultado = imagen.copy()

        if len(rostros) == 0:
            st.warning(
                "No se detectó ningún rostro. "
                "Prueba con una fotografía frontal y bien iluminada."
            )
        else:
            # Crear una máscara para limitar el efecto al rostro.
            mascara = np.zeros(imagen.shape[:2], dtype=np.uint8)

            for (x, y, w, h) in rostros:
                # Óvalo aproximado para evitar una región rectangular.
                centro = (x + w // 2, y + h // 2)
                ejes = (max(1, w // 2), max(1, h // 2))

                cv2.ellipse(
                    mascara,
                    centro,
                    ejes,
                    0,
                    0,
                    360,
                    255,
                    thickness=-1
                )

            # Suavizar los bordes para integrar el efecto.
            mascara = cv2.GaussianBlur(
                mascara,
                (0, 0),
                sigmaX= max(1.0, imagen.shape[1] / 300.0)
            )

            rostro_oscurecido = reducir_brillo(imagen, factor)

            # Combinar el rostro oscurecido con el fondo original.
            alpha = mascara.astype(np.float32)[:, :, None] / 255.0

            resultado = (
                imagen.astype(np.float32) * (1.0 - alpha)
                + rostro_oscurecido.astype(np.float32) * alpha
            )

            resultado = np.clip(resultado, 0, 255).astype(np.uint8)

            st.success(f"Rostros detectados: {len(rostros)}")

    # Comparación
    st.subheader("Comparación")

    col1, col2 = st.columns(2)

    with col1:
        st.image(imagen, caption="Original", width="stretch")

    with col2:
        st.image(resultado, caption="Brillo reducido", width="stretch")

    # Descarga
    buffer = BytesIO()
    Image.fromarray(resultado).save(buffer, format="PNG")

    st.download_button(
        label="Descargar imagen procesada",
        data=buffer.getvalue(),
        file_name="rostro_brillo_reducido.png",
        mime="image/png"
    )


if __name__ == "__main__":
    run()
