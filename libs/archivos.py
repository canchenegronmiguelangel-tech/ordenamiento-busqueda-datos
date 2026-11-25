import os

try:
    import pandas as pd
except ImportError:
    pd = None


def convertir_lista(valores):
    """Si todos los valores son enteros, los regresa como int.
    Si alguno no lo es, regresa todos como texto."""
    try:
        return [int(v) for v in valores]
    except ValueError:
        return [str(v) for v in valores]


def leer_txt(ruta):
    """Lee un TXT (un dato por línea). Regresa lista de int o de str."""
    valores = []
    with open(ruta, encoding="utf-8-sig") as f:
        for linea in f:
            linea = linea.strip()
            if linea != "":
                valores.append(linea)
    return convertir_lista(valores)


def leer_xlsx(ruta):
    """Lee la primera columna de un XLSX (asume encabezado en la fila 1)."""
    if pd is None:
        raise ImportError("Falta pandas. Instala con: pip install -r requirements.txt")
    tabla = pd.read_excel(ruta)
    valores = []
    for v in tabla.iloc[:, 0].tolist():
        if pd.isna(v):
            continue
        texto = str(v).strip()
        if texto.endswith(".0") and texto[:-2].lstrip("-").isdigit():
            texto = texto[:-2]
        if texto != "":
            valores.append(texto)
    return convertir_lista(valores)


def cargar_archivo(ruta):
    """Elige el lector según la extensión."""
    if not os.path.exists(ruta):
        raise FileNotFoundError("No se encontró el archivo: " + ruta)
    extension = os.path.splitext(ruta)[1].lower()
    if extension == ".txt":
        return leer_txt(ruta)
    elif extension == ".xlsx":
        return leer_xlsx(ruta)
    else:
        raise ValueError("Formato no válido. Usa .txt o .xlsx")


def exportar(datos, algoritmo, tiempo, nombre="resultado"):
    """Guarda en salida/ (dentro del proyecto) el ordenado y un resumen."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    carpeta = os.path.join(base, "salida")
    os.makedirs(carpeta, exist_ok=True)

    ruta_datos = os.path.join(carpeta, nombre + "_ordenado.txt")
    with open(ruta_datos, "w", encoding="utf-8") as f:
        for d in datos:
            f.write(str(d) + "\n")

    ruta_resumen = os.path.join(carpeta, nombre + "_resumen.txt")
    with open(ruta_resumen, "w", encoding="utf-8") as f:
        f.write("Algoritmo utilizado: " + algoritmo + "\n")
        f.write("Tiempo de ejecución: " + str(tiempo) + " segundos\n")
        f.write("Total de registros: " + str(len(datos)) + "\n")

    return ruta_datos, ruta_resumen