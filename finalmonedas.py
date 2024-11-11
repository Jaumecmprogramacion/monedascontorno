import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

# Definir variable global para la ruta del archivo
ruta_archivo = ""

def subir_imagen():
    global ruta_archivo
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg *.gif *.bmp")])
    if ruta_archivo:
        etiqueta_archivo.config(text=f"Archivo seleccionado: {ruta_archivo}", fg="green")
        boton_contar.config(state=tk.NORMAL)

def contar_monedas():
    global ruta_archivo
    
    if ruta_archivo:  # Asegurarse de que se ha seleccionado una imagen
        valorGauss = 3
        valorKernel = 3
        
        # Leer la imagen
        original = cv2.imread(ruta_archivo)
        
        if original is None:
            etiqueta_resultado.config(text="Error al cargar la imagen.", fg="red")
            return

        # Procesar la imagen
        gris = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        gauss = cv2.GaussianBlur(gris, (valorGauss, valorGauss), 0)
        canny = cv2.Canny(gauss, 60, 100)

        kernel = np.ones((valorKernel, valorKernel), np.uint8)
        cierre = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)

        contornos, jerarquia = cv2.findContours(cierre.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Mostrar el número de monedas encontradas
        num_monedas = len(contornos)
        etiqueta_resultado.config(text=f"Monedas encontradas: {num_monedas}", fg="blue")
        
        # Dibujar los contornos en la imagen original
        cv2.drawContours(original, contornos, -1, (0, 0, 255), 2)

        # Mostrar ventanas de OpenCV con resultados
        # cv2.imshow("Grises", gris)
        # cv2.imshow("Gauss", gauss)
        # cv2.imshow("Canny", canny)
        cv2.imshow("Resultado", original)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Contador de Monedas Simple")
ventana.geometry("400x400")
ventana.configure(bg="#f0f0f0")  # Fondo de color claro

# Crear y colocar widgets con diseño mejorado
titulo = tk.Label(ventana, text="Contador de Monedas", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333333")
titulo.pack(pady=20)

boton_subir = tk.Button(ventana, text="Subir Imagen", command=subir_imagen, font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049", padx=10, pady=5)
boton_subir.pack(pady=10)

etiqueta_archivo = tk.Label(ventana, text="No se ha seleccionado ningún archivo", font=("Helvetica", 10), bg="#f0f0f0", fg="#666666")
etiqueta_archivo.pack(pady=10)

boton_contar = tk.Button(ventana, text="Contar Monedas", command=contar_monedas, state=tk.DISABLED, font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049", padx=10, pady=5)
boton_contar.pack(pady=10)

# Etiqueta para mostrar el resultado
etiqueta_resultado = tk.Label(ventana, text="", font=("Helvetica", 12), bg="#f0f0f0", fg="white")
etiqueta_resultado.pack(pady=20)

# Iniciar el bucle de eventos
ventana.mainloop()

