import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def calcular_histograma(canal):
    """
    Calcula el histograma de un canal de imagen.
    """

    histograma, bins = np.histogram(
        canal.flatten(),
        bins=256,
        range=(0, 256)
    )

    return histograma


def ecualizar_canal(canal):
    """
    Ecualización de histograma mediante CDF.
    """

    histograma = calcular_histograma(canal)

    # Función de distribución acumulada
    cdf = histograma.cumsum()

    # Eliminar valores donde no hay píxeles
    cdf_no_cero = cdf[cdf > 0]

    if len(cdf_no_cero) == 0:
        return canal

    cdf_min = cdf_no_cero[0]

    # Ecualización
    cdf_normalizada = (
        (cdf - cdf_min)
        / (cdf[-1] - cdf_min)
        * 255
    )

    cdf_normalizada = np.clip(
        cdf_normalizada,
        0,
        255
    )

    # Transformar cada pixel
    canal_ecualizado = cdf_normalizada[
        canal
    ]

    return canal_ecualizado.astype(np.uint8)


def mostrar_histograma(canal, titulo):

    fig, ax = plt.subplots()

    ax.hist(
        canal.flatten(),
        bins=256,
        range=(0, 256)
    )

    ax.set_title(titulo)
    ax.set_xlabel("Intensidad")
    ax.set_ylabel("Número de píxeles")

    ax.set_xlim(0, 255)

    st.pyplot(
        fig,
        #use_container_width=True
    )

    plt.close(fig)


def run():

    st.set_page_config(
        page_title="Histogramas RGB"
    )

    st.title("Histogramas RGB")

    archivo = st.file_uploader(
        "Selecciona una imagen",
        type=[
            "png",
            "jpg",
            "jpeg",
            "bmp",
            "webp"
        ]
    )

    if archivo is None:
        return


    # Cargar imagen

    imagen = Image.open(
        archivo
    ).convert("RGB")

    img = np.array(imagen)

    st.subheader("Imagen original")

    st.image(
        imagen,
        #use_container_width=True
    )


    # Separar canales
    
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]


    # Histogramas originales
    

    st.subheader("Histogramas originales")

    with st.expander("Histograma R"):
        mostrar_histograma(
            R,
            "Histograma del canal R"
        )

    with st.expander("Histograma G"):
        mostrar_histograma(
            G,
            "Histograma del canal G"
        )

    with st.expander("Histograma B"):
        mostrar_histograma(
            B,
            "Histograma del canal B"
        )


    # Ecualización
    

    if st.button("Ecualizar canales RGB"):

        R_eq = ecualizar_canal(R)
        G_eq = ecualizar_canal(G)
        B_eq = ecualizar_canal(B)

        # Reconstruir imagen
        imagen_ecualizada = np.stack(
            [R_eq, G_eq, B_eq],
            axis=2
        )

        st.subheader(
            "Imagen después de la ecualización"
        )

        st.image(
            imagen_ecualizada,
            #use_container_width=True
        )


        # Histogramas ecualizados
        

        st.subheader(
            "Histogramas después de la ecualización"
        )

        with st.expander("Histograma R ecualizado"):
            mostrar_histograma(
                R_eq,
                "R ecualizado"
            )

        with st.expander("Histograma G ecualizado"):
            mostrar_histograma(
                G_eq,
                "G ecualizado"
            )

        with st.expander("Histograma B ecualizado"):
            mostrar_histograma(
                B_eq,
                "B ecualizado"
            )