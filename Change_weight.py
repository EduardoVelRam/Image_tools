import streamlit as st
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="Image Compressor",
    page_icon="🗜️"
)

st.title("Image Weight Reduction")

archivo = st.file_uploader(
    "Select one image",
    type=["jpg", "jpeg", "png", "webp", "bmp"]
)

niveles = {
    "Alta": 90,
    "Media": 60,
    "Baja": 30,
    "Muy Baja": 10
}

nivel = st.selectbox(
    "Quality Level",
    list(niveles.keys())
)

if archivo is not None:

    imagen = Image.open(archivo).convert("RGB")

    st.subheader("Imagen original")
    st.image(imagen, use_container_width=True)

    calidad = niveles[nivel]

    buffer = BytesIO()

    imagen.save(
        buffer,
        format="JPEG",
        quality=calidad,
        optimize=True
    )

    buffer.seek(0)

    imagen_comprimida = Image.open(buffer)

    st.subheader("Imagen comprimida")
    st.image(imagen_comprimida, use_container_width=True)

    tamaño_original = len(archivo.getvalue()) / 1024
    tamaño_comprimido = len(buffer.getvalue()) / 1024

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Original Size",
            f"{tamaño_original:.1f} KB"
        )

    with col2:
        st.metric(
            "Tamaño comprimido",
            f"{tamaño_comprimido:.1f} KB"
        )

    ahorro = 100 * (
        1 - tamaño_comprimido / tamaño_original
    )

    st.success(
        f"Reducción aproximada: {ahorro:.1f}%"
    )

    st.download_button(
        label="⬇️ Descargar imagen comprimida",
        data=buffer.getvalue(),
        file_name=f"comprimida_{nivel.lower()}.jpg",
        mime="image/jpeg"
    )