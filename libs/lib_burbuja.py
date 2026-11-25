"""Librería: Ordenamiento BURBUJA (interno)."""


def burbuja(lista, ascendente=True):
    """Regresa una copia ordenada de `lista` con burbuja.

    ascendente=True  -> de menor a mayor
    ascendente=False -> de mayor a menor
    """
    arr = list(lista)
    n = len(arr)
    for i in range(n - 1):
        hubo_cambio = False
        for j in range(n - 1 - i):
            fuera_de_orden = arr[j] > arr[j + 1] if ascendente else arr[j] < arr[j + 1]
            if fuera_de_orden:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                hubo_cambio = True
        if not hubo_cambio:
            break
    return arr


ordenar = burbuja  # nombre común para el programa principal