import time
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from libs.archivos import cargar_archivo, exportar
from libs import (lib_burbuja, lib_insercion, lib_seleccion, lib_shellsort,
                  lib_quicksort, lib_heapsort, lib_radixsort,
                  lib_mezcladirecta, lib_mezclaequilibrada,
                  lib_busquedasecuencial, lib_busquedabinaria, lib_busquedahash, lib_intercalacion)

# ---------- Colores ----------
BG = "#13131f"
PANEL = "#1f1f33"
CAMPO = "#2b2b45"
TEXTO = "#e5e7eb"
GRIS = "#9ca3af"
MORADO = "#7c5cff"
CIAN = "#22d3ee"
VERDE = "#22c55e"
NARANJA = "#f59e0b"
ROSA = "#ec4899"
ROJO = "#ef4444"

# ---------- Catálogos ----------
ALGORITMOS = {
    "Burbuja (interno)": lib_burbuja.ordenar,
    "Inserción (interno)": lib_insercion.ordenar,
    "Selección (interno)": lib_seleccion.ordenar,
    "ShellSort (interno)": lib_shellsort.ordenar,
    "QuickSort (interno)": lib_quicksort.ordenar,
    "HeapSort (interno)": lib_heapsort.ordenar,
    "Radix Sort (interno)": lib_radixsort.ordenar,
    "Mezcla Directa (externo)": lib_mezcladirecta.ordenar,
    "Mezcla Equilibrada (externo)": lib_mezclaequilibrada.ordenar,
}
SOLO_NUMEROS = ["Radix Sort (interno)", "Mezcla Directa (externo)",
                "Mezcla Equilibrada (externo)"]

# ---------- Estado compartido ----------
datos = []
datos_ordenados = []
algoritmo_usado = ""
tiempo = 0.0
orden_asc = True
nombre_base = "resultado"


def es_numerica(lista):
    return len(lista) > 0 and isinstance(lista[0], int)


# ---------- Ayudas de texto ----------
def limpiar():
    texto.delete("1.0", tk.END)


def escribir(contenido, etiqueta=None):
    if etiqueta:
        texto.insert(tk.END, contenido, etiqueta)
    else:
        texto.insert(tk.END, contenido)


def mostrar(lista, titulo):
    """Primeros 20, últimos 20 y total."""
    limpiar()
    escribir(titulo + "\n", "titulo")
    escribir("Total de registros: ", "etiqueta")
    escribir(str(len(lista)) + "\n\n", "dato")
    escribir("Primeros 20\n", "etiqueta")
    escribir(str(lista[:20]) + "\n\n", "dato")
    escribir("Últimos 20\n", "etiqueta")
    escribir(str(lista[-20:]) + "\n", "dato")


# ---------- Acciones ----------
def cargar():
    global datos, datos_ordenados, algoritmo_usado, tiempo, nombre_base
    ruta = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Archivos de datos", "*.txt *.xlsx")])
    if ruta == "":
        return
    try:
        datos = cargar_archivo(ruta)
    except Exception as e:
        messagebox.showerror("Error al cargar", str(e))
        return
    datos_ordenados = []
    algoritmo_usado = ""
    tiempo = 0.0
    nombre_base = os.path.splitext(os.path.basename(ruta))[0]
    tipo = "números" if es_numerica(datos) else "texto"
    etiqueta_archivo.config(text=os.path.basename(ruta) + "  |  " +
                            str(len(datos)) + " registros (" + tipo + ")",
                            fg=VERDE)
    etiqueta_estado.config(text="")
    mostrar(datos, "Datos originales")


def ordenar():
    global datos_ordenados, algoritmo_usado, tiempo, orden_asc
    if not datos:
        messagebox.showwarning("Aviso", "Primero carga un archivo.")
        return
    nombre = combo_alg.get()
    if nombre in SOLO_NUMEROS and not es_numerica(datos):
        messagebox.showwarning(
            "Aviso", nombre + " solo funciona con números. "
                     "Elige otro algoritmo para texto.")
        return
    asc = combo_orden.get() == "Ascendente"
    etiqueta_estado.config(text="Ordenando...", fg=NARANJA)
    ventana.update_idletasks()
    try:
        inicio = time.perf_counter()
        resultado = ALGORITMOS[nombre](datos, asc)
        fin = time.perf_counter()
    except Exception as e:
        messagebox.showerror("Error al ordenar", str(e))
        etiqueta_estado.config(text="")
        return
    datos_ordenados = resultado
    algoritmo_usado = nombre
    tiempo = fin - inicio
    orden_asc = asc
    etiqueta_estado.config(
        text=nombre + " | " + combo_orden.get() + " | " +
        format(tiempo, ".6f") + " s", fg=CIAN)
    mostrar(datos_ordenados, "Datos ordenados con " + nombre)


def buscar():
    if not datos:
        messagebox.showwarning("Aviso", "Primero carga un archivo.")
        return
    valor = entrada_busqueda.get().strip()
    if valor == "":
        messagebox.showwarning("Aviso", "Escribe un valor a buscar.")
        return
    if es_numerica(datos):
        try:
            objetivo = int(valor)
        except ValueError:
            messagebox.showwarning("Aviso", "Los datos son números; escribe un entero.")
            return
    else:
        objetivo = valor

    metodo = combo_busqueda.get()
    if metodo == "Binaria" and not datos_ordenados:
        messagebox.showwarning("Aviso", "La búsqueda binaria necesita datos ordenados. "
                                        "Primero usa Ordenar.")
        return
    if metodo == "Hash" and not es_numerica(datos):
        messagebox.showwarning("Aviso", "La búsqueda hash solo funciona con números.")
        return

    lista = datos_ordenados if datos_ordenados else datos
    try:
        inicio = time.perf_counter()
        if metodo == "Secuencial":
            r = lib_busquedasecuencial.buscar(lista, objetivo)
        elif metodo == "Binaria":
            r = lib_busquedabinaria.buscar(lista, objetivo, orden_asc)
        else:
            r = lib_busquedahash.buscar(lista, objetivo)
        t_busqueda = time.perf_counter() - inicio
    except Exception as e:
        messagebox.showerror("Error en la búsqueda", str(e))
        return

    posiciones = [i for i, v in enumerate(lista) if v == objetivo]

    limpiar()
    escribir("Búsqueda " + metodo + " del valor " + str(objetivo) + "\n\n", "titulo")
    if r["encontrado"]:
        escribir("ENCONTRADO\n", "ok")
        escribir("Primera posición hallada: " + str(r["indice"]) + "\n", "dato")
        escribir("Coincidencias totales: " + str(len(posiciones)) + "\n", "dato")
        escribir("Posiciones (máx. 20): " + str(posiciones[:20]) + "\n", "dato")
    else:
        escribir("NO se encontró el valor\n", "error")
    escribir("\nComparaciones del algoritmo: " + str(r["comparaciones"]) + "\n", "etiqueta")
    escribir("Tiempo: " + format(t_busqueda, ".6f") + " s\n", "etiqueta")


def exportar_resultados():
    if not datos_ordenados:
        messagebox.showwarning("Aviso", "Primero ordena los datos.")
        return
    try:
        ruta_datos, ruta_resumen = exportar(datos_ordenados, algoritmo_usado,
                                            tiempo, nombre_base)
    except Exception as e:
        messagebox.showerror("Error al exportar", str(e))
        return
    mostrar(datos_ordenados, "Exportado con " + algoritmo_usado +
            " (" + format(tiempo, ".6f") + " s)")
    messagebox.showinfo("Exportado", "Archivos guardados:\n" + ruta_datos +
                        "\n" + ruta_resumen)
    
# ---------- Intercalación (ventana emergente) ----------
def abrir_intercalacion():
    rutas = {"A": "", "B": ""}
    resultado = {"datos": [], "tiempo": 0.0}

    top = tk.Toplevel(ventana)
    top.title("Intercalación de dos archivos ordenados")
    top.geometry("560x340")
    top.configure(bg=BG)
    top.transient(ventana)
    top.grab_set()

    tk.Label(top, text="Intercalación (mezcla de 2 archivos ya ordenados)",
             bg=BG, fg=MORADO, font=("Segoe UI", 12, "bold")).pack(pady=(12, 6))

    marco = tk.Frame(top, bg=PANEL, highlightbackground=MORADO,
                     highlightthickness=1)
    marco.pack(fill="x", padx=14, pady=6)

    def elegir(clave, etiqueta):
        ruta = filedialog.askopenfilename(
            parent=top, title="Selecciona el archivo " + clave,
            filetypes=[("Archivos de datos", "*.txt *.xlsx")])
        if ruta == "":
            return
        rutas[clave] = ruta
        etiqueta.config(text=os.path.basename(ruta), fg=VERDE)

    for clave in ("A", "B"):
        fila = tk.Frame(marco, bg=PANEL)
        fila.pack(fill="x", padx=10, pady=6)
        etiqueta = tk.Label(fila, text="Sin archivo", bg=PANEL, fg=GRIS,
                            font=("Segoe UI", 10))
        boton(fila, "Archivo " + clave, lambda c=clave, e=etiqueta: elegir(c, e),
              CIAN).pack(side="left")
        etiqueta.pack(side="left", padx=12)

    fila_orden = tk.Frame(marco, bg=PANEL)
    fila_orden.pack(fill="x", padx=10, pady=6)
    tk.Label(fila_orden, text="Sentido de ambos archivos:", bg=PANEL, fg=TEXTO,
             font=("Segoe UI", 10)).pack(side="left")
    combo_ord = ttk.Combobox(fila_orden, values=["Ascendente", "Descendente"],
                             state="readonly", width=14)
    combo_ord.current(0)
    combo_ord.pack(side="left", padx=8)

    estado = tk.Label(top, text="", bg=BG, fg=CIAN, font=("Segoe UI", 10, "bold"))
    estado.pack(pady=4)

    def intercalar():
        if rutas["A"] == "" or rutas["B"] == "":
            messagebox.showwarning("Aviso", "Elige los dos archivos.", parent=top)
            return
        asc = combo_ord.get() == "Ascendente"
        try:
            a = cargar_archivo(rutas["A"])
            b = cargar_archivo(rutas["B"])
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e), parent=top)
            return
        if not a or not b:
            messagebox.showwarning("Aviso", "Alguno de los archivos está vacío.",
                                   parent=top)
            return
        if es_numerica(a) != es_numerica(b):
            messagebox.showwarning("Aviso", "Un archivo tiene números y el otro texto. "
                                            "Deben ser del mismo tipo.", parent=top)
            return
        for nombre, lista in (("A", a), ("B", b)):
            if not lib_busquedabinaria.esta_ordenada(lista, asc):
                messagebox.showwarning(
                    "Aviso", "El archivo " + nombre + " no está ordenado en sentido " +
                             combo_ord.get().lower() + ". La intercalación necesita "
                             "archivos ya ordenados (ordénalo y expórtalo primero).",
                    parent=top)
                return
        try:
            inicio = time.perf_counter()
            r = lib_intercalacion.intercalacion(a, b, asc)
            t = time.perf_counter() - inicio
        except Exception as e:
            messagebox.showerror("Error al intercalar", str(e), parent=top)
            return
        resultado["datos"] = r
        resultado["tiempo"] = t
        resultado["nombre"] = ("intercalado_" +
                               os.path.splitext(os.path.basename(rutas["A"]))[0] + "_" +
                               os.path.splitext(os.path.basename(rutas["B"]))[0])
        estado.config(text=str(len(a)) + " + " + str(len(b)) + " = " + str(len(r)) +
                      " registros | " + format(t, ".6f") + " s", fg=CIAN)
        mostrar(r, "Intercalación de " + os.path.basename(rutas["A"]) + " y " +
                   os.path.basename(rutas["B"]) + " (" + format(t, ".6f") + " s)")

    def exportar_intercalado():
        if not resultado["datos"]:
            messagebox.showwarning("Aviso", "Primero intercala los archivos.",
                                   parent=top)
            return
        try:
            ruta_datos, ruta_resumen = exportar(resultado["datos"], "Intercalación",
                                                resultado["tiempo"], resultado["nombre"])
        except Exception as e:
            messagebox.showerror("Error al exportar", str(e), parent=top)
            return
        messagebox.showinfo("Exportado", "Archivos guardados:\n" + ruta_datos +
                            "\n" + ruta_resumen, parent=top)

    botones = tk.Frame(top, bg=BG)
    botones.pack(pady=8)
    boton(botones, "Intercalar", intercalar, VERDE).pack(side="left", padx=4)
    boton(botones, "Exportar", exportar_intercalado, ROSA).pack(side="left", padx=4)
    boton(botones, "Cerrar", top.destroy, GRIS).pack(side="left", padx=4)

# ---------- Componentes con estilo ----------
def aclarar(color, cantidad=30):
    """Devuelve un color un poco más claro (para el efecto hover)."""
    r = min(255, int(color[1:3], 16) + cantidad)
    g = min(255, int(color[3:5], 16) + cantidad)
    b = min(255, int(color[5:7], 16) + cantidad)
    return "#%02x%02x%02x" % (r, g, b)


def boton(padre, titulo, comando, color):
    b = tk.Button(padre, text=titulo, command=comando, bg=color, fg="white",
                  activebackground=aclarar(color), activeforeground="white",
                  font=("Segoe UI", 10, "bold"), relief="flat", bd=0,
                  padx=14, pady=6, cursor="hand2")
    b.bind("<Enter>", lambda e: b.config(bg=aclarar(color)))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b


def panel(titulo, color):
    marco = tk.Frame(ventana, bg=PANEL, highlightbackground=color,
                     highlightthickness=1)
    marco.pack(fill="x", padx=14, pady=5)
    tk.Label(marco, text=titulo, bg=PANEL, fg=color,
             font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(6, 0))
    fila = tk.Frame(marco, bg=PANEL)
    fila.pack(fill="x", padx=10, pady=8)
    return fila


# ---------- Ventana ----------
ventana = tk.Tk()
ventana.title("Sistema de Procesamiento y Ordenamiento Masivo de Datos")
ventana.geometry("900x700")
ventana.configure(bg=BG)

estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure("TCombobox", fieldbackground=CAMPO, background=MORADO,
                 foreground=TEXTO, arrowcolor=TEXTO, bordercolor=MORADO,
                 lightcolor=CAMPO, darkcolor=CAMPO, padding=4)
estilo.map("TCombobox", fieldbackground=[("readonly", CAMPO)],
           foreground=[("readonly", TEXTO)],
           selectbackground=[("readonly", CAMPO)],
           selectforeground=[("readonly", TEXTO)])
estilo.configure("Vertical.TScrollbar", background=MORADO, troughcolor=PANEL,
                 bordercolor=PANEL, arrowcolor=TEXTO)
ventana.option_add("*TCombobox*Listbox.background", CAMPO)
ventana.option_add("*TCombobox*Listbox.foreground", TEXTO)
ventana.option_add("*TCombobox*Listbox.selectBackground", MORADO)
ventana.option_add("*TCombobox*Listbox.font", ("Segoe UI", 10))

# Encabezado
encabezado = tk.Frame(ventana, bg=MORADO)
encabezado.pack(fill="x")
tk.Label(encabezado, text="Procesamiento y Ordenamiento Masivo de Datos",
         bg=MORADO, fg="white", font=("Segoe UI", 16, "bold")).pack(pady=(10, 0))
tk.Label(encabezado, text="Ordenar  •  Buscar  •  Exportar",
         bg=MORADO, fg="#e0d8ff", font=("Segoe UI", 10)).pack(pady=(0, 10))

# 1. Archivo
fila1 = panel("1  ARCHIVO", CIAN)
boton(fila1, "Cargar archivo", cargar, CIAN).pack(side="left")
etiqueta_archivo = tk.Label(fila1, text="Sin archivo", bg=PANEL, fg=GRIS,
                            font=("Segoe UI", 10))
etiqueta_archivo.pack(side="left", padx=12)

# 2. Ordenar
fila2 = panel("2  ORDENAR", VERDE)
combo_alg = ttk.Combobox(fila2, values=list(ALGORITMOS.keys()),
                         state="readonly", width=28)
combo_alg.current(0)
combo_alg.pack(side="left")
combo_orden = ttk.Combobox(fila2, values=["Ascendente", "Descendente"],
                           state="readonly", width=14)
combo_orden.current(0)
combo_orden.pack(side="left", padx=8)
boton(fila2, "Ordenar", ordenar, VERDE).pack(side="left")
etiqueta_estado = tk.Label(fila2, text="", bg=PANEL, fg=CIAN,
                           font=("Segoe UI", 10, "bold"))
etiqueta_estado.pack(side="left", padx=12)

# 3. Buscar
fila3 = panel("3  BUSCAR", NARANJA)
entrada_busqueda = tk.Entry(fila3, width=18, bg=CAMPO, fg=TEXTO,
                            insertbackground=TEXTO, relief="flat",
                            font=("Segoe UI", 11))
entrada_busqueda.pack(side="left", ipady=4)
combo_busqueda = ttk.Combobox(fila3, values=["Secuencial", "Binaria", "Hash"],
                              state="readonly", width=12)
combo_busqueda.current(0)
combo_busqueda.pack(side="left", padx=8)
boton(fila3, "Buscar", buscar, NARANJA).pack(side="left")

# 4. Exportar
fila4 = panel("4  EXPORTAR", ROSA)
boton(fila4, "Exportar resultados", exportar_resultados, ROSA).pack(side="left")
# 5. Intercalar
fila5 = panel("5  INTERCALAR", MORADO)
boton(fila5, "Intercalar 2 archivos", abrir_intercalacion, MORADO).pack(side="left")

# Resultados
marco5 = tk.Frame(ventana, bg=PANEL, highlightbackground=MORADO,
                  highlightthickness=1)
marco5.pack(fill="both", expand=True, padx=14, pady=(5, 14))
tk.Label(marco5, text="RESULTADOS", bg=PANEL, fg=MORADO,
         font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(6, 0))
cuerpo = tk.Frame(marco5, bg=PANEL)
cuerpo.pack(fill="both", expand=True, padx=10, pady=8)
scroll = ttk.Scrollbar(cuerpo)
scroll.pack(side="right", fill="y")
texto = tk.Text(cuerpo, wrap="word", yscrollcommand=scroll.set, bg="#0d0d17",
                fg=TEXTO, insertbackground=TEXTO, relief="flat", padx=10,
                pady=8, font=("Consolas", 11))
texto.pack(fill="both", expand=True)
scroll.config(command=texto.yview)


texto.tag_configure("titulo", foreground=MORADO, font=("Segoe UI", 13, "bold"))
texto.tag_configure("etiqueta", foreground=GRIS)
texto.tag_configure("dato", foreground=CIAN)
texto.tag_configure("ok", foreground=VERDE, font=("Segoe UI", 12, "bold"))
texto.tag_configure("error", foreground=ROJO, font=("Segoe UI", 12, "bold"))

ventana.mainloop()