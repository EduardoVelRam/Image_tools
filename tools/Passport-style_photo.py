import streamlit as st
from PIL import Image, ImageOps
from io import BytesIO

st.set_page_config(
    page_title="Foto tamaño Infantil",
    page_icon="📷"
)

st.title("Generador de Fotografía Infantil")

st.write(
    "Carga una fotografía y genera una imagen con "
    "formato de fotografía tamaño infantil."
)

archivo = st.file_uploader(
    "Selecciona una fotografía",
    type=["jpg", "jpeg", "png", "webp"]
)

if archivo is not None:

    imagen = Image.open(archivo).convert("RGB")

    st.subheader("Fotografía original")

    st.image(
        imagen,
        use_container_width=True
    )

    # --------------------------------
    # Dimensiones fotografía tamaño infantil

    dpi = 300

    ancho_cm = 2.5
    alto_cm = 3.0

    ancho_px = round(ancho_cm / 2.54 * dpi)
    alto_px = round(alto_cm / 2.54 * dpi)

    st.write(
        f"Tamaño: {ancho_cm} × {alto_cm} cm "
        f"({ancho_px} × {alto_px} px a 300 DPI)"
    )

    # --------------------------------
    # Recorte automático

    proporcion = ancho_px / alto_px

    ancho, alto = imagen.size

    proporcion_actual = ancho / alto

    if proporcion_actual > proporcion:

        # Imagen demasiado ancha
        nuevo_ancho = round(alto * proporcion)

        izquierda = (ancho - nuevo_ancho) // 2

        imagen = imagen.crop(
            (
                izquierda,
                0,
                izquierda + nuevo_ancho,
                alto
            )
        )

    else:

        # Imagen demasiado alta
        nuevo_alto = round(ancho / proporcion)

        arriba = (alto - nuevo_alto) // 2

        imagen = imagen.crop(
            (
                0,
                arriba,
                ancho,
                arriba + nuevo_alto
            )
        )

    # --------------------------------
    # Redimensionar

    foto = imagen.resize(
        (ancho_px, alto_px),
        Image.Resampling.LANCZOS
    )

    st.subheader("Vista previa")

    st.image(
        foto,
        width=250
    )

    buffer = BytesIO()

    foto.save(
        buffer,
        format="JPEG",
        quality=95,
        dpi=(dpi, dpi)
    )

    st.download_button(
        label="Descargar fotografía",
        data=buffer.getvalue(),
        file_name="EVR_foto_infantil.jpg",
        mime="image/jpeg"
    )