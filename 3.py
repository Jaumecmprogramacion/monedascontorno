import tkinter as tk
from tkinter import filedialog
import random
import cv2
import numpy as np

def subir_imagen():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg *.gif *.bmp")])
    if ruta_archivo:
        etiqueta_archivo.config(text=f"Archivo seleccionado: {ruta_archivo}")
        boton_contar.config(state=tk.NORMAL)

def contar_monedas():
    # conteo de monedas
        valorGauss=3
        valorKernel=3
        original=cv2.imread(subir_imagen)
        gris=cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
        gauss=cv2.GaussianBlur(gris,(valorGauss,valorGauss), 0)
        canny=cv2.Canny(gauss, 60,100)

        kernel=np.ones((valorKernel,valorKernel),np.uint8)
        cierre=cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)

        contornos, jerarquia=cv2.findContours(cierre.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print("monedas encontradas: {}".format(len(contornos)))
        cv2.drawContours(original, contornos, -1, (0,0,255),2)
        #MOSTRAR RESULTADO
        cv2.imshow("Grises",gris)
        cv2.imshow("gauss",gauss)
        cv2.imshow("canny",canny)
        cv2.imshow("resultado",original)
        cv2.waitKey(0)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Contador de Monedas Simple")
ventana.geometry("400x300")

# Crear y colocar widgets
titulo = tk.Label(ventana, text="Contador de Monedas", font=("Arial", 16))
titulo.pack(pady=20)

boton_subir = tk.Button(ventana, text="Subir Imagen", command=subir_imagen)
boton_subir.pack(pady=10)

etiqueta_archivo = tk.Label(ventana, text="No se ha seleccionado ningún archivo")
etiqueta_archivo.pack(pady=10)

boton_contar = tk.Button(ventana, text="Contar Monedas", command=contar_monedas, state=tk.DISABLED)
boton_contar.pack(pady=10)

etiqueta_resultado = tk.Label(ventana, text="")
etiqueta_resultado.pack(pady=20)

# Iniciar el bucle de eventos
ventana.mainloop()