import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO
import torch
import torch.nn as nn
import torch.optim as optim


#def run():

    # Red neuronal de una sola capa
class Inversor(nn.Module):
    def __init__(self):
        super().__init__()

            # Una entrada -> una salida
        self.capa = nn.Linear(1, 1)

    def forward(self, x):
        return self.capa(x)


def entrenar_red():

        # Valores de entrada: 0-255
    x = torch.arange(256, dtype=torch.float32).reshape(-1, 1)

        # Valores objetivo: 255-x
    y = 255 - x

    modelo = Inversor()

        # Función de pérdida
    criterio = nn.MSELoss()

        # Optimizador
    optimizador = optim.SGD(
        modelo.parameters(),
        lr=0.001
        )

        # Entrenamiento
    for epoch in range(5000):

            # Forward
        prediccion = modelo(x)

            # Error
        perdida = criterio(prediccion, y)

            # Backpropagation
        optimizador.zero_grad()
        perdida.backward()
        optimizador.step()

    return modelo

def run():

    st.set_page_config(
        page_title="Color Inverter"
    )

    st.title("Color Inverter with Neural Network")

    st.write(
        "Inversión de colores mediante una red neuronal "
        "de una sola capa."
    )

    # Entrenar la red
    modelo = entrenar_red()

    # Mostrar parámetros aprendidos
    peso = modelo.capa.weight.item()
    bias = modelo.capa.bias.item()

    st.write(f"Peso aprendido: {peso:.6f}")
    st.write(f"Bias aprendido: {bias:.6f}")

    archivo = st.file_uploader(
        "Select an image",
        type=[
            "png",
            "jpg",
            "jpeg",
            "bmp",
            "gif",
            "webp"
        ]
    )

    if archivo is not None:

        imagen = Image.open(archivo).convert("RGB")

        st.subheader("Original Image")
        st.image(imagen, width='stretch')

        # Convertir imagen a NumPy
        img_np = np.array(imagen)

        # Convertir los pixeles a tensor
        pixeles = torch.tensor(
            img_np,
            dtype=torch.float32
        )

        # Guardar dimensiones
        shape_original = pixeles.shape

        # Convertir a una columna
        pixeles = pixeles.reshape(-1, 1)

        # Aplicar la red neuronal
        with torch.no_grad():
            pixeles_invertidos = modelo(pixeles)

        # Limitar valores al rango 0-255
        pixeles_invertidos = torch.clamp(
            pixeles_invertidos,
            0,
            255
        )

        # Regresar a NumPy
        img_invertida = (pixeles_invertidos.reshape(shape_original).numpy().astype(np.uint8))

        # Convertir a imagen
        imagen_invertida = Image.fromarray(
            img_invertida
        )

        st.subheader("Inverted Image")
        st.image(
            imagen_invertida,
            width='stretch'
        )

        # Descargar
        buffer = BytesIO()

        imagen_invertida.save(
            buffer,
            format="PNG"
        )

        st.download_button(
            label="Download Inverted Image",
            data=buffer.getvalue(),
            file_name="imagen_invertida.png",
            mime="image/png"
        )