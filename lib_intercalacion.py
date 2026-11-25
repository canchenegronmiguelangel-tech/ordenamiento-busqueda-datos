"""Librería: INTERCALACIÓN (externo, 2 vías).

Toma dos secuencias YA ordenadas y las mezcla en una sola en una pasada
secuencial. Hay versión para listas y versión para archivos de texto
(un número por línea).
"""


def intercalacion(lista_a, lista_b, ascendente=True):
    """Intercala dos listas ya ordenadas (en el mismo sentido) y regresa una nueva."""
    resultado = []
    i, j = 0, 0
    while i < len(lista_a) and j < len(lista_b):
        toma_a = lista_a[i] <= lista_b[j] if ascendente else lista_a[i] >= lista_b[j]
        if toma_a:
            resultado.append(lista_a[i])
            i += 1
        else:
            resultado.append(lista_b[j])
            j += 1
    resultado.extend(lista_a[i:])     # remanentes
    resultado.extend(lista_b[j:])
    return resultado


def _siguiente(f):
    linea = f.readline()
    return int(linea) if linea.strip() else None


def intercalar_archivos(ruta_a, ruta_b, ruta_salida, ascendente=True):
    """Intercala dos archivos ordenados (un entero por línea) hacia `ruta_salida`.

    Lee un número a la vez, sin cargar los archivos completos en memoria.
    Regresa la cantidad de registros escritos.
    """
    escritos = 0
    with open(ruta_a) as fa, open(ruta_b) as fb, open(ruta_salida, "w") as out:
        a, b = _siguiente(fa), _siguiente(fb)
        while a is not None and b is not None:
            if (a <= b) if ascendente else (a >= b):
                out.write(f"{a}\n")
                a = _siguiente(fa)
            else:
                out.write(f"{b}\n")
                b = _siguiente(fb)
            escritos += 1
        while a is not None:
            out.write(f"{a}\n")
            a = _siguiente(fa)
            escritos += 1
        while b is not None:
            out.write(f"{b}\n")
            b = _siguiente(fb)
            escritos += 1
    return escritos


ordenar = intercalacion