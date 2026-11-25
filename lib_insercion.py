"""Librería: Ordenamiento por INSERCIÓN (interno)."""


def insercion(lista, ascendente=True):
    """Regresa una copia ordenada de `lista` con inserción."""
    arr = list(lista)
    for i in range(1, len(arr)):
        actual = arr[i]
        j = i - 1
        while j >= 0 and (arr[j] > actual if ascendente else arr[j] < actual):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = actual
    return arr


ordenar = insercion