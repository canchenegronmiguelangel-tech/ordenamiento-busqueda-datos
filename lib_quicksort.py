"""Librería: Ordenamiento QUICKSORT (interno).

Versión iterativa (pila explícita) con pivote = mediana de tres y partición
de Hoare. Así no hay riesgo de pasar el límite de recursión de Python con
5000 datos (por ejemplo, listas ya ordenadas) y soporta muchos repetidos.
"""


def _antes(a, b, ascendente):
    """True si `a` debe ir antes que `b`."""
    return a < b if ascendente else a > b


def _mediana_de_tres(a, b, c, ascendente):
    if _antes(a, b, ascendente):
        if _antes(b, c, ascendente):
            return b
        return c if _antes(a, c, ascendente) else a
    if _antes(a, c, ascendente):
        return a
    return c if _antes(b, c, ascendente) else b


def quicksort(lista, ascendente=True):
    """Regresa una copia ordenada de `lista` con quicksort."""
    arr = list(lista)
    pila = [(0, len(arr) - 1)]
    while pila:
        bajo, alto = pila.pop()
        if bajo >= alto:
            continue
        pivote = _mediana_de_tres(arr[bajo], arr[(bajo + alto) // 2], arr[alto], ascendente)
        i, j = bajo, alto
        while i <= j:
            while _antes(arr[i], pivote, ascendente):
                i += 1
            while _antes(pivote, arr[j], ascendente):
                j -= 1
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1
        pila.append((bajo, j))
        pila.append((i, alto))
    return arr


ordenar = quicksort