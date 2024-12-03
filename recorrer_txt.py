import tkinter as tk
from tkinter import filedialog, messagebox

def mostrar_modal(mensaje):
    modal = tk.Toplevel()
    modal.title("Errores detectados")
    modal.transient(root)
    modal.grab_set()

    ancho = 400
    alto = 300

    ancho_pantalla = modal.winfo_screenwidth()
    alto_pantalla = modal.winfo_screenheight()

    pos_x = (ancho_pantalla // 2) - (ancho // 2)
    pos_y = (alto_pantalla // 2) - (alto // 2)

    modal.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")

    tk.Label(modal, text="Resultado del procesamiento:").pack(pady=10)
    text_area = tk.Text(modal, wrap=tk.WORD, height=10, width=50)
    text_area.pack(pady=5, padx=10)
    text_area.insert(tk.END, mensaje)
    text_area.configure(state='disabled')

    tk.Button(modal, text="Cerrar", command=modal.destroy).pack(pady=10)


def seleccionar_archivo(propiedades_requeridas):
    ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if ruta:
        procesar_archivo(ruta, propiedades_requeridas)
    else:
        mostrar_modal("No se seleccionó ningún archivo.")

def procesar_archivo(ruta, propiedades_requeridas):
    codificaciones = ['utf-8', 'latin-1']  
    errores = []
    for codificacion in codificaciones:
        try:
            with open(ruta, 'r', encoding=codificacion) as file:
                for linea in file:
                    propiedades = linea.strip().split('|')
                    if len(propiedades) != propiedades_requeridas:
                        if propiedades_requeridas == 8:
                            errores.append(propiedades[2])
                        else:
                            errores.append(propiedades[1])

            
        
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            mostrar_modal(f"Se produjo un error al procesar el archivo: {e}")
            return

    if errores:
        mensaje = "Códigos de artículo con errores:\n" + "\n".join(errores)
        mostrar_modal(mensaje)
    else:
        mostrar_modal("No se encontraron errores.")

def main():
    global root
    root = tk.Tk()
    root.title("Procesador de Archivos")
    root.geometry("400x220")
    root.eval('tk::PlaceWindow . center')

    tk.Label(root, text="Tipo de archivo a procesar").pack(pady=20)

    tk.Button(root, text="CodiProd (8 Prop)", command=lambda: seleccionar_archivo(8)).pack(pady=5)
    tk.Button(root, text="DbPrecio (22 Prop)", command=lambda: seleccionar_archivo(22)).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
