import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import platform
import shutil

def buscar_y_abrir_archivo(termino_busqueda, directorio_busqueda):
    try:
        for carpeta_raiz, carpetas, archivos in os.walk(directorio_busqueda):
            for archivo in archivos:
                if termino_busqueda.lower() in archivo.lower():
                    ruta_completa = os.path.join(carpeta_raiz, archivo)
                    abrir_archivo(ruta_completa)
                    return True  # Abre el primer archivo encontrado
        messagebox.showinfo("Resultados", "No se encontró ningún archivo que coincida con la búsqueda.")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"Error al buscar archivos: {e}")
        return False

def abrir_archivo(ruta):
    try:
        if platform.system() == "Windows":
            os.startfile(ruta)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", ruta])
        else:  # Linux y otros sistemas
            subprocess.run(["xdg-open", ruta])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

def realizar_busqueda():
    termino_busqueda = entrada_busqueda.get().strip()
    if not termino_busqueda:
        messagebox.showwarning("Advertencia", "Por favor, introduce un término de búsqueda.")
        return

    directorio_busqueda = entrada_directorio.get().strip()
    if not os.path.isdir(directorio_busqueda):
        messagebox.showwarning("Advertencia", "El directorio proporcionado no es válido.")
        return

    encontrado = buscar_y_abrir_archivo(termino_busqueda, directorio_busqueda)
    if encontrado:
        messagebox.showinfo("Éxito", f"Se abrió el archivo correspondiente a: {termino_busqueda}")

def seleccionar_directorio():
    directorio = filedialog.askdirectory()
    if directorio:
        entrada_directorio.delete(0, tk.END)
        entrada_directorio.insert(0, directorio)
        mostrar_contenido_directorio(directorio)

def mostrar_contenido_directorio(directorio):
    try:
        lista_archivos.delete(0, tk.END)  # Limpiar lista
        for archivo in os.listdir(directorio):
            lista_archivos.insert(tk.END, archivo)
    except Exception as e:
        messagebox.showerror("Error", f"Error al mostrar el contenido del directorio: {e}")

def mover_archivo():
    archivo_seleccionado = lista_archivos.curselection()
    if not archivo_seleccionado:
        messagebox.showwarning("Advertencia", "Selecciona un archivo para mover.")
        return

    archivo = lista_archivos.get(archivo_seleccionado)
    origen = os.path.join(entrada_directorio.get(), archivo)
    destino = filedialog.askdirectory()
    
    if destino:
        try:
            shutil.move(origen, destino)
            mostrar_contenido_directorio(entrada_directorio.get())  # Actualizar la lista
            messagebox.showinfo("Éxito", f"Archivo movido a {destino}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mover el archivo: {e}")

def renombrar_archivo():
    archivo_seleccionado = lista_archivos.curselection()
    if not archivo_seleccionado:
        messagebox.showwarning("Advertencia", "Selecciona un archivo para renombrar.")
        return

    archivo = lista_archivos.get(archivo_seleccionado)
    nuevo_nombre = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=archivo)
    
    if nuevo_nombre:
        try:
            os.rename(os.path.join(entrada_directorio.get(), archivo), nuevo_nombre)
            mostrar_contenido_directorio(entrada_directorio.get())  # Actualizar la lista
            messagebox.showinfo("Éxito", f"Archivo renombrado a {nuevo_nombre}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo renombrar el archivo: {e}")

def eliminar_archivo():
    archivo_seleccionado = lista_archivos.curselection()
    if not archivo_seleccionado:
        messagebox.showwarning("Advertencia", "Selecciona un archivo para eliminar.")
        return

    archivo = lista_archivos.get(archivo_seleccionado)
    archivo_a_eliminar = os.path.join(entrada_directorio.get(), archivo)
    
    try:
        os.remove(archivo_a_eliminar)
        mostrar_contenido_directorio(entrada_directorio.get())  # Actualizar la lista
        messagebox.showinfo("Éxito", f"Archivo {archivo} eliminado.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el archivo: {e}")

def realizar_copia_seguridad():
    # Abre un cuadro de diálogo para seleccionar la carpeta de destino
    carpeta_destino = filedialog.askdirectory(title="Selecciona una carpeta de destino para la copia de seguridad")
    
    if carpeta_destino:
        try:
            # Copiar archivos desde el directorio de búsqueda a la carpeta de destino
            for archivo in os.listdir(entrada_directorio.get()):
                origen = os.path.join(entrada_directorio.get(), archivo)
                if os.path.isfile(origen):  # Solo copiar archivos, no directorios
                    shutil.copy(origen, carpeta_destino)
            messagebox.showinfo("Éxito", "La copia de seguridad se ha realizado con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la copia de seguridad: {e}")
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó ninguna carpeta para la copia de seguridad.")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Organizador de Archivos")
ventana.geometry("600x400")

# Campo de entrada para el término de búsqueda
frame_busqueda = ttk.LabelFrame(ventana, text="Búsqueda de Archivos", padding=10)
frame_busqueda.pack(fill="x", padx=10, pady=10)

ttk.Label(frame_busqueda, text="Término de búsqueda:").pack(side="left", padx=5)
entrada_busqueda = ttk.Entry(frame_busqueda, width=40)
entrada_busqueda.pack(side="left", padx=5)

# Campo para seleccionar el directorio de búsqueda
ttk.Label(frame_busqueda, text="Directorio de búsqueda:").pack(side="left", padx=5)
entrada_directorio = ttk.Entry(frame_busqueda, width=30)
entrada_directorio.pack(side="left", padx=5)

btn_buscar = ttk.Button(frame_busqueda, text="Buscar y abrir", command=realizar_busqueda)
btn_buscar.pack(side="left", padx=5)

btn_directorio = ttk.Button(frame_busqueda, text="Seleccionar directorio", command=seleccionar_directorio)
btn_directorio.pack(side="left", padx=5)

# Botón para realizar la copia de seguridad
btn_copia_seguridad = ttk.Button(ventana, text="Realizar copia de seguridad", command=realizar_copia_seguridad)
btn_copia_seguridad.pack(pady=10)

# Lista de archivos en el directorio
frame_archivos = ttk.LabelFrame(ventana, text="Archivos en el directorio", padding=10)
frame_archivos.pack(fill="both", padx=10, pady=10)

lista_archivos = tk.Listbox(frame_archivos, height=10, width=50)
lista_archivos.pack(side="left", fill="y")

# Botones de acciones de archivos
btn_mover = ttk.Button(ventana, text="Mover archivo", command=mover_archivo)
btn_mover.pack(side="left", padx=10)

btn_renombrar = ttk.Button(ventana, text="Renombrar archivo", command=renombrar_archivo)
btn_renombrar.pack(side="left", padx=10)

btn_eliminar = ttk.Button(ventana, text="Eliminar archivo", command=eliminar_archivo)
btn_eliminar.pack(side="left", padx=10)

# Ejecutar la ventana
ventana.mainloop()

