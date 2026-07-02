import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np


class RomboPuzzle:

    def __init__(self, root):

        self.root = root
        self.root.title("Rhombus puzzle")
        self.root.geometry("1100x750")

        self.imagen_original = None
        self.imagen_resultado = None

        panel = tk.Frame(root)
        panel.pack(fill="x", pady=10)

        tk.Button(
            panel,
            text="  Load image",
            command=self.cargar_imagen
        ).pack(side="left", padx=5)

        tk.Label(panel, text="Tamaño del rombo:").pack(side="left")

        self.tamano = tk.IntVar(value=60)

        tk.Scale(
            panel,
            from_=20,
            to=150,
            orient="horizontal",
            variable=self.tamano,
            length=200
        ).pack(side="left")

        tk.Button(
            panel,
            text="Generate",
            command=self.generar_rombos
        ).pack(side="left", padx=10)

        tk.Button(
            panel,
            text="Save JPG",
            command=self.guardar
        ).pack(side="left")

        self.lbl_img = tk.Label(root)
        self.lbl_img.pack(expand=True)

    def cargar_imagen(self):

        ruta = filedialog.askopenfilename(
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.bmp")
            ]
        )

        if not ruta:
            return

        self.imagen_original = cv2.imread(ruta)

        self.mostrar(self.imagen_original)

    def dibujar_rombos(self, img, lado):

        h, w = img.shape[:2]

        color = (0, 0, 0)
        grosor = 2

        altura = lado

        y = 0

        while y < h + altura:

            desplazamiento = 0

            if (y // altura) % 2:
                desplazamiento = lado

            x = -lado + desplazamiento

            while x < w + lado:

                puntos = np.array([
                    [x, y],
                    [x + lado, y - altura],
                    [x + 2 * lado, y],
                    [x + lado, y + altura]
                ], np.int32)

                cv2.polylines(
                    img,
                    [puntos],
                    True,
                    color,
                    grosor
                )

                x += 2 * lado

            y += altura

        return img

    def generar_rombos(self):

        if self.imagen_original is None:
            messagebox.showwarning(
                "Aviso",
                "Primero cargue una imagen"
            )
            return

        lado = self.tamano.get()

        resultado = self.imagen_original.copy()

        resultado = self.dibujar_rombos(
            resultado,
            lado
        )

        self.imagen_resultado = resultado

        self.mostrar(resultado)

    def mostrar(self, img):

        rgb = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )

        pil = Image.fromarray(rgb)

        preview = pil.copy()
        preview.thumbnail((1000, 650))

        photo = ImageTk.PhotoImage(preview)

        self.lbl_img.configure(image=photo)
        self.lbl_img.image = photo

    def guardar(self):

        if self.imagen_resultado is None:

            messagebox.showwarning(
                "Aviso",
                "Generate first the puzzle"
            )

            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[
                ("JPEG", "*.jpg")
            ]
        )

        if not ruta:
            return

        cv2.imwrite(
            ruta,
            self.imagen_resultado,
            [cv2.IMWRITE_JPEG_QUALITY, 100]
        )

        messagebox.showinfo(
            "Ready",
            "Imagen saved correctly."
        )


if __name__ == "__main__":

    root = tk.Tk()
    app = RomboPuzzle(root)
    root.mainloop()