import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

def run():
    st.title("Invertir colores")

    st.write("Aquí va el código del inversor.")
    
    st.set_page_config(
        page_title="Color Inverter",
    )

    st.title("Color Inverter")

    archivo = st.file_uploader(
        "Select an image",
        type=["png", "jpg", "jpeg", "bmp", "gif", "webp"]
    )

    if archivo is not None:

        imagen = Image.open(archivo)

        st.subheader("Original Image")
        st.image(imagen, use_container_width=True)

        img_np = np.array(imagen)

        # Contrast
        min_val = np.min(img_np)
        max_val = np.max(img_np)
        def contrast_stretching(pixel):
            return (pixel - min_val) * (255 / (max_val - min_val))

        # Con función logaritmo
        def log_transform(pixel):
            c = 255 / np.log(1 + np.max(pixel))
            return c * np.log(1 + pixel)

        # Invertir colores
        if len(img_np.shape) == 3:
            img_invertida = 255 - img_np
        else:
            img_invertida = 255 - img_np

        #if len(img_np.shape) == 3:
        #    img_invertida = log_transform(img_np)
        #else:
        #    img_invertida = log_transform(img_np)

        imagen_invertida = Image.fromarray(
            img_invertida.astype(np.uint8)
        )

        st.subheader("Transformed Image")
        st.image(imagen_invertida, use_container_width=True)

        buffer = BytesIO()

        imagen_invertida.save(
            buffer,
            format="PNG"
        )

        st.download_button(
            label="Download Transformed Image",
            data=buffer.getvalue(),
            file_name="imagen_invertida.png",
            mime="image/png"
        )