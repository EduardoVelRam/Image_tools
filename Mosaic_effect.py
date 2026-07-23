import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO
import math

st.set_page_config(
    page_title="Mosaic effect",
    page_icon="🧩"
)

st.title("Mosaic Generator")

archivo = st.file_uploader(
    "Select one image",
    type=["png","jpg","jpeg","bmp","webp"]
)

if archivo is not None:

    imagen = Image.open(archivo).convert("RGB")

    st.subheader("Original image")
    st.image(imagen, use_container_width=True)

    tamaño = st.slider(
        "Mosaic size",
        5,
        80,
        20
    )

    figura = st.selectbox(
        "Figure",
        [
            "Squares",
            "Circles",
            "Hexagons"
        ]
    )

    img = np.array(imagen)

    alto, ancho = img.shape[:2]

    salida = np.full_like(img, 255)

    for y in range(0, alto, tamaño):

        for x in range(0, ancho, tamaño):

            bloque = img[
                y:min(y+tamaño,alto),
                x:min(x+tamaño,ancho)
            ]

            color = bloque.mean(axis=(0,1)).astype(np.uint8)

            cx = x + tamaño//2
            cy = y + tamaño//2

            if figura == "Squares":

                cv2.rectangle(
                    salida,
                    (x,y),
                    (
                        min(x+tamaño,ancho),
                        min(y+tamaño,alto)
                    ),
                    color.tolist(),
                    -1
                )

            elif figura == "Circles":

                radio = tamaño//2

                cv2.circle(
                    salida,
                    (cx,cy),
                    radio,
                    color.tolist(),
                    -1
                )

            elif figura == "Hexagons":

                r = tamaño//2

                puntos = []

                for angulo in range(6):

                    a = math.radians(60*angulo)

                    px = int(cx + r*np.cos(a))
                    py = int(cy + r*np.sin(a))

                    puntos.append([px,py])

                puntos = np.array(puntos,np.int32)

                cv2.fillPoly(
                    salida,
                    [puntos],
                    color.tolist()
                )

    resultado = Image.fromarray(salida)

    st.subheader("Result")

    st.image(resultado, use_container_width=True)

    buffer = BytesIO()

    resultado.save(buffer,format="PNG")

    st.download_button(
        "Download mosaic",
        buffer.getvalue(),
        "mosaico.png",
        "image/png"
    )