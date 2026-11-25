"""Librería: Ordenamiento por SELECCIÓN (interno)."""


def seleccion(lista, ascendente=True):
    """Regresa una copia ordenada de `lista` con selección."""
    arr = list(lista)
    n = len(arr)
    for i in range(n - 1):
        pos = i  # posición del menor (o mayor si es descendente)
        for j in range(i + 1, n):
            if (arr[j] < arr[pos]) if ascendente else (arr[j] > arr[pos]):
                pos = j
        if pos != i:
            arr[i], arr[pos] = arr[pos], arr[i]
    return arr


ordenar = seleccion