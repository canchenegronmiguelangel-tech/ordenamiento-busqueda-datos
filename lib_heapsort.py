"""Librería: Ordenamiento HEAPSORT (interno)."""


def _hundir(arr, n, i, ascendente):
    """Hunde el elemento i hasta cumplir la propiedad del montículo."""
    while True:
        mayor = i  # el que debe quedar más al final del orden pedido
        izq = 2 * i + 1
        der = 2 * i + 2
        if izq < n and (arr[izq] > arr[mayor] if ascendente else arr[izq] < arr[mayor]):
            mayor = izq
        if der < n and (arr[der] > arr[mayor] if ascendente else arr[der] < arr[mayor]):
            mayor = der
        if mayor == i:
            return
        arr[i], arr[mayor] = arr[mayor], arr[i]
        i = mayor


def heap_sort(lista, ascendente=True):
    """Regresa una copia ordenada de `lista` con Heapsort."""
    arr = list(lista)
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):      # 1) construir el montículo
        _hundir(arr, n, i, ascendente)
    for fin in range(n - 1, 0, -1):          # 2) extraer la raíz uno por uno
        arr[0], arr[fin] = arr[fin], arr[0]
        _hundir(arr, fin, 0, ascendente)
    return arr


ordenar = heap_sort