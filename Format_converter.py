import streamlit as st
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="Image format converter",
    page_icon="🖼️"
)

st.title("Image format converter")

archivo = st.file_uploader(
    "Select an image",
    type=["png", "jpg", "jpeg", "bmp", "gif", "tiff", "webp"]
)

formatos = {
    "PNG": "png",
    "JPEG": "jpg",
    "BMP": "bmp",
    "GIF": "gif",
    "TIFF": "tiff",
    "WEBP": "webp"
}

formato_salida = st.selectbox(
    "Output format",
    list(formatos.keys())
)

if archivo is not None:

    imagen = Image.open(archivo)

    st.subheader("Vista previa")
    st.image(imagen, use_container_width=True)

    buffer = BytesIO()

    if formato_salida == "JPEG":
        imagen = imagen.convert("RGB")

    imagen.save(
        buffer,
        format=formato_salida
    )

    buffer.seek(0)

    nombre_original = archivo.name.rsplit(".", 1)[0]

    st.download_button(
        label=f"Download as {formato_salida}",
        data=buffer,
        file_name=f"{nombre_original}.{formatos[formato_salida]}",
        mime=f"image/{formatos[formato_salida]}"
    )