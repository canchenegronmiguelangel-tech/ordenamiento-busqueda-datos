"""Librería: BÚSQUEDA BINARIA (solo buscar, no ordena).

Necesita que los datos YA estén ordenados. En cada paso mira el elemento del
medio y descarta la mitad donde el valor no puede estar.
"""


def busqueda_binaria(lista_ordenada, objetivo, ascendente=True):
    """Regresa (indice, comparaciones). indice = -1 si no existe.
    La lista DEBE estar ordenada en el mismo sentido que `ascendente`."""
    izquierda, derecha = 0, len(lista_ordenada) - 1
    comparaciones = 0
    while izquierda <= derecha:
        comparaciones += 1
        medio = (izquierda + derecha) // 2
        valor = lista_ordenada[medio]
        if valor == objetivo:
            return medio, comparaciones
        if (valor < objetivo) == ascendente:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1, comparaciones


def esta_ordenada(lista, ascendente=True):
    """True si la lista está ordenada en el sentido indicado."""
    for i in range(len(lista) - 1):
        if (lista[i] > lista[i + 1]) if ascendente else (lista[i] < lista[i + 1]):
            return False
    return True


def buscar(lista, objetivo, ascendente=True):
    """Opción de búsqueda BINARIA para el programa principal.

    Regresa {"metodo", "encontrado", "indice", "comparaciones"}.
    Lanza ValueError si la lista no está ordenada.
    """
    if not esta_ordenada(lista, ascendente):
        raise ValueError("La búsqueda binaria requiere que los datos estén ordenados.")
    indice, comparaciones = busqueda_binaria(lista, objetivo, ascendente)
    return {"metodo": "binaria", "encontrado": indice != -1,
            "indice": indice, "comparaciones": comparaciones}