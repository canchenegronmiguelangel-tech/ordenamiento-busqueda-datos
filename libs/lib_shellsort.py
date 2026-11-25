"""Librería: Ordenamiento SHELLSORT (interno). Secuencia de Shell: n/2, n/4, ... 1."""


def shell_sort(lista, ascendente=True):
    """Regresa una copia ordenada de `lista` con ShellSort."""
    arr = list(lista)
    n = len(arr)
    salto = n // 2
    while salto > 0:
        for i in range(salto, n):
            temp = arr[i]
            j = i
            while j >= salto and (arr[j - salto] > temp if ascendente else arr[j - salto] < temp):
                arr[j] = arr[j - salto]
                j -= salto
            arr[j] = temp
        salto //= 2
    return arr


ordenar = shell_sort