import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import traceback

class ContadorMonedas:
    def __init__(self, master):
        self.master = master
        self.master.title("Contador de Monedas Avanzado")
        self.master.geometry("500x600")
        self.master.configure(bg="#f0f0f0")

        self.ruta_archivo = ""
        self.imagen_original = None
        self.crear_widgets()

    def crear_widgets(self):
        # Título
        titulo = tk.Label(self.master, text="Contador de Monedas Avanzado", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#333333")
        titulo.pack(pady=20)

        # Frame para los botones
        frame_botones = tk.Frame(self.master, bg="#f0f0f0")
        frame_botones.pack(pady=10)

        # Botón para subir imagen
        self.boton_subir = tk.Button(frame_botones, text="Subir Imagen", command=self.subir_imagen, font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049", padx=10, pady=5)
        self.boton_subir.pack(side=tk.LEFT, padx=5)

        # Botón para contar monedas
        self.boton_contar = tk.Button(frame_botones, text="Contar Monedas", command=self.contar_monedas, state=tk.DISABLED, font=("Helvetica", 12), bg="#4CAF50", fg="white", activebackground="#45a049", padx=10, pady=5)
        self.boton_contar.pack(side=tk.LEFT, padx=5)

        # Etiqueta para mostrar el archivo seleccionado
        self.etiqueta_archivo = tk.Label(self.master, text="No se ha seleccionado ningún archivo", font=("Helvetica", 10), bg="#f0f0f0", fg="#666666", wraplength=450)
        self.etiqueta_archivo.pack(pady=10)

        # Frame para los parámetro
        frame_parametros = tk.Frame(self.master, bg="#f0f0f0")
        frame_parametros.pack(pady=10)

        # Parámetros ajustables
        self.crear_parametro(frame_parametros, "Valor Gauss:", 3, 21, 3)
        self.crear_parametro(frame_parametros, "Valor Kernel:", 3, 21, 3)
        self.crear_parametro(frame_parametros, "Canny Bajo:", 0, 255, 50)
        self.crear_parametro(frame_parametros, "Canny Alto:", 0, 255, 150)

        # Etiqueta para mostrar el resultado.
        self.etiqueta_resultado = tk.Label(self.master, text="", font=("Helvetica", 14), bg="#f0f0f0", fg="#333333")
        self.etiqueta_resultado.pack(pady=20)

        # Canvas para mostrar la imagen
        self.canvas = tk.Canvas(self.master, width=400, height=300, bg="white", highlightthickness=1, highlightbackground="#999999")
        self.canvas.pack(pady=10)

    def crear_parametro(self, parent, texto, desde, hasta, valor_inicial):
        frame = tk.Frame(parent, bg="#f0f0f0")
        frame.pack(pady=5)
        
        label = tk.Label(frame, text=texto, font=("Helvetica", 10), bg="#f0f0f0", fg="#333333", width=12, anchor="w")
        label.pack(side=tk.LEFT, padx=5)
        
        var = tk.IntVar(value=valor_inicial)
        escala = tk.Scale(frame, from_=desde, to=hasta, orient=tk.HORIZONTAL, variable=var, length=200, bg="#f0f0f0", highlightthickness=0)
        escala.pack(side=tk.LEFT, padx=5)
        
        setattr(self, texto.lower().replace(" ", "_").replace(":", ""), var)

    def subir_imagen(self):
        self.ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if self.ruta_archivo:
            self.etiqueta_archivo.config(text=f"Archivo seleccionado: {self.ruta_archivo}", fg="green")
            self.boton_contar.config(state=tk.NORMAL)
            self.cargar_imagen()

    def cargar_imagen(self):
        try:
            self.imagen_original = cv2.imread(self.ruta_archivo)
            if self.imagen_original is None:
                raise ValueError("No se pudo cargar la imagen.")
            self.mostrar_imagen(self.imagen_original)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la imagen: {str(e)}")

    def contar_monedas(self):
        if self.imagen_original is None:
            messagebox.showerror("Error", "No se ha cargado ninguna imagen.")
            return

        try:
            valor_gauss = self.valor_gauss.get()
            valor_kernel = self.valor_kernel.get()
            canny_bajo = self.canny_bajo.get()
            canny_alto = self.canny_alto.get()

            # Asegurarse de que los valores sean impares y mayores que 1
            valor_gauss = max(3, valor_gauss + 1 if valor_gauss % 2 == 0 else valor_gauss)
            valor_kernel = max(3, valor_kernel + 1 if valor_kernel % 2 == 0 else valor_kernel)

            gris = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2GRAY)
            gauss = cv2.GaussianBlur(gris, (valor_gauss, valor_gauss), 0)
            canny = cv2.Canny(gauss, canny_bajo, canny_alto)

            kernel = np.ones((valor_kernel, valor_kernel), np.uint8)
            cierre = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)

            contornos, _ = cv2.findContours(cierre.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filtrar contornos por área
            area_min = 100  # Ajusta este valor según el tamaño de tus monedas
            contornos_filtrados = [cnt for cnt in contornos if cv2.contourArea(cnt) > area_min]

            imagen_resultado = self.imagen_original.copy()
            cv2.drawContours(imagen_resultado, contornos_filtrados, -1, (0, 255, 0), 2)

            num_monedas = len(contornos_filtrados)
            self.etiqueta_resultado.config(text=f"Monedas encontradas: {num_monedas}", fg="blue")

            self.mostrar_imagen(imagen_resultado)

        except cv2.error as e:
            messagebox.showerror("Error de OpenCV", f"Error al procesar la imagen: {str(e)}\n\nDetalles:\n{traceback.format_exc()}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}\n\nDetalles:\n{traceback.format_exc()}")

    def mostrar_imagen(self, imagen):
        try:
            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            imagen_tk = self.redimensionar_imagen(imagen_rgb, (400, 300))
            self.imagen_tk = tk.PhotoImage(data=cv2.imencode('.png', imagen_tk)[1].tobytes())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imagen_tk)
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar la imagen: {str(e)}\n\nDetalles:\n{traceback.format_exc()}")

    def redimensionar_imagen(self, imagen, tamaño):
        altura, ancho = imagen.shape[:2]
        relacion = min(tamaño[0]/ancho, tamaño[1]/altura)
        nuevo_tamaño = (int(ancho * relacion), int(altura * relacion))
        return cv2.resize(imagen, nuevo_tamaño, interpolation=cv2.INTER_AREA)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContadorMonedas(root)
    root.mainloop()

