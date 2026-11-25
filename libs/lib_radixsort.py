"""Librería: Ordenamiento RADIX SORT (interno, enteros positivos y negativos)."""


def _counting_por_digito(arr, exp):
    """Counting sort estable según el dígito indicado por exp."""
    salida = [0] * len(arr)
    conteo = [0] * 10
    for num in arr:
        conteo[(num // exp) % 10] += 1
    for i in range(1, 10):
        conteo[i] += conteo[i - 1]
    for num in reversed(arr):
        d = (num // exp) % 10
        conteo[d] -= 1
        salida[conteo[d]] = num
    return salida


def _radix_positivos(arr):
    if not arr:
        return []
    maximo = max(arr)
    exp = 1
    while maximo // exp > 0:
        arr = _counting_por_digito(arr, exp)
        exp *= 10
    return arr


def radix_sort(lista, ascendente=True):
    """Regresa una copia ordenada de `lista` con Radix Sort LSD base 10."""
    negativos = _radix_positivos([-x for x in lista if x < 0])
    positivos = _radix_positivos([x for x in lista if x >= 0])
    resultado = [-x for x in reversed(negativos)] + positivos   # ascendente
    if not ascendente:
        resultado.reverse()
    return resultado


ordenar = radix_sort