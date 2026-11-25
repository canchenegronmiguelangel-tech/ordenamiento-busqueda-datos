"""Librería: BÚSQUEDA HASH para enteros (solo buscar, no ordena).

Función hash: valor % tamaño. Las colisiones se manejan con encadenamiento:
cada cubeta es una lista de [valor, [posiciones]], así también se guardan
los números repetidos. No necesita que los datos estén ordenados.
"""


class TablaHash:
    def __init__(self, tamano=1009):
        self.tamano = tamano
        self.cubetas = [[] for _ in range(tamano)]

    def _hash(self, valor):
        return valor % self.tamano          # funciona también con negativos

    def insertar(self, valor, posicion):
        cubeta = self.cubetas[self._hash(valor)]
        for par in cubeta:
            if par[0] == valor:
                par[1].append(posicion)
                return
        cubeta.append([valor, [posicion]])

    def buscar(self, valor):
        """Regresa (indice_cubeta, posiciones o None, comparaciones)."""
        indice = self._hash(valor)
        comparaciones = 0
        for clave, posiciones in self.cubetas[indice]:
            comparaciones += 1
            if clave == valor:
                return indice, posiciones, comparaciones
        return indice, None, comparaciones


def construir_tabla(lista, tamano=None):
    """Crea y llena una TablaHash con los valores de `lista`."""
    if tamano is None:
        tamano = max(11, len(lista) // 2) | 1      # tamaño impar, ~2 elementos por cubeta
    tabla = TablaHash(tamano)
    for posicion, valor in enumerate(lista):
        tabla.insertar(valor, posicion)
    return tabla


def busqueda_hash(tabla, objetivo):
    """Regresa (indice_primera_posicion, comparaciones); -1 si no existe."""
    _, posiciones, comparaciones = tabla.buscar(objetivo)
    return (posiciones[0] if posiciones else -1), comparaciones


def buscar(lista, objetivo, tabla=None):
    """Opción de búsqueda HASH para el programa principal.

    Si no se pasa `tabla`, se construye a partir de `lista`. Para varias
    búsquedas sobre los mismos datos conviene construirla una sola vez con
    construir_tabla() y pasarla.
    Regresa {"metodo", "encontrado", "indice", "comparaciones",
             "cubeta", "posiciones"}.
    """
    if tabla is None:
        tabla = construir_tabla(lista)
    cubeta, posiciones, comparaciones = tabla.buscar(objetivo)
    return {"metodo": "hash", "encontrado": posiciones is not None,
            "indice": posiciones[0] if posiciones else -1,
            "comparaciones": comparaciones, "cubeta": cubeta,
            "posiciones": posiciones or []}