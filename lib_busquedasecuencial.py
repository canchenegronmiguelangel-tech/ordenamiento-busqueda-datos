"""Librería: BÚSQUEDA SECUENCIAL (solo buscar, no ordena).

Revisa los elementos uno por uno desde el primero. No necesita orden.
También permite llamar a la binaria (que vive en ejercicio_11_binario.py)
desde este mismo archivo con `buscar(..., metodo="binaria")`.
"""
from libs import lib_busquedabinaria as _binario

busqueda_binaria = _binario.busqueda_binaria   # se mantiene disponible aquí


def busqueda_secuencial(lista, objetivo):
    """Regresa (indice, comparaciones). indice = -1 si no existe."""
    comparaciones = 0
    for indice, valor in enumerate(lista):
        comparaciones += 1
        if valor == objetivo:
            return indice, comparaciones
    return -1, comparaciones


def buscar(lista, objetivo, metodo="secuencial", ascendente=True):
    """Opción de búsqueda para el programa principal.

    metodo: "secuencial" (por defecto) o "binaria".
    Regresa {"metodo", "encontrado", "indice", "comparaciones"}.
    """
    metodo = metodo.lower()
    if metodo == "secuencial":
        indice, comparaciones = busqueda_secuencial(lista, objetivo)
        return {"metodo": "secuencial", "encontrado": indice != -1,
                "indice": indice, "comparaciones": comparaciones}
    if metodo == "binaria":
        return _binario.buscar(lista, objetivo, ascendente)
    raise ValueError("Método no válido: usa 'secuencial' o 'binaria'.")