"""Librería: MEZCLA DIRECTA (externo) con archivos temporales reales.

Cada pasada reparte bloques de tamaño 1, 2, 4, 8... alternadamente en dos
archivos auxiliares (F1 y F2) y los intercala de regreso al archivo principal.
"""
import os
import shutil
import tempfile


def _leer(f):
    linea = f.readline()
    return int(linea) if linea.strip() else None


def mezcla_directa(lista, ascendente=True):
    """Regresa una copia ordenada de `lista` con Mezcla Directa (vía archivos)."""
    n = len(lista)
    if n < 2:
        return list(lista)

    carpeta = tempfile.mkdtemp(prefix="mezcla_directa_")
    principal = os.path.join(carpeta, "principal.txt")
    ruta_f1 = os.path.join(carpeta, "F1.txt")
    ruta_f2 = os.path.join(carpeta, "F2.txt")
    try:
        with open(principal, "w") as f:
            f.writelines(f"{x}\n" for x in lista)

        bloque = 1
        while bloque < n:
            # 1) Distribución: bloques alternados hacia F1 y F2
            cant1 = cant2 = 0
            with open(principal) as src, open(ruta_f1, "w") as f1, open(ruta_f2, "w") as f2:
                destino, contados = f1, 0
                for linea in src:
                    destino.write(linea)
                    contados += 1
                    if destino is f1:
                        cant1 += 1
                    else:
                        cant2 += 1
                    if contados == bloque:
                        destino = f2 if destino is f1 else f1
                        contados = 0

            # 2) Fusión: se mezcla un bloque de F1 con uno de F2 a la vez
            with open(ruta_f1) as f1, open(ruta_f2) as f2, open(principal, "w") as out:
                r1, r2 = cant1, cant2          # registros que faltan por leer
                while r1 > 0 or r2 > 0:
                    c1, c2 = min(bloque, r1), min(bloque, r2)
                    r1 -= c1
                    r2 -= c2
                    v1 = _leer(f1) if c1 > 0 else None
                    v2 = _leer(f2) if c2 > 0 else None
                    while c1 > 0 and c2 > 0:
                        if (v1 <= v2) if ascendente else (v1 >= v2):
                            out.write(f"{v1}\n")
                            c1 -= 1
                            v1 = _leer(f1) if c1 > 0 else None
                        else:
                            out.write(f"{v2}\n")
                            c2 -= 1
                            v2 = _leer(f2) if c2 > 0 else None
                    while c1 > 0:
                        out.write(f"{v1}\n")
                        c1 -= 1
                        v1 = _leer(f1) if c1 > 0 else None
                    while c2 > 0:
                        out.write(f"{v2}\n")
                        c2 -= 1
                        v2 = _leer(f2) if c2 > 0 else None
            bloque *= 2

        with open(principal) as f:
            return [int(l) for l in f if l.strip()]
    finally:
        shutil.rmtree(carpeta, ignore_errors=True)


ordenar = mezcla_directa