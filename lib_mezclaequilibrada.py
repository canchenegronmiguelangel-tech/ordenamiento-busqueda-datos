"""Librería: MEZCLA EQUILIBRADA NATURAL (externo) con archivos temporales reales.

Detecta las corridas (secuencias ya ordenadas) del archivo, las reparte
alternadamente en F1 y F2 y las intercala hacia G1 y G2 (4 archivos en total,
equilibrado) hasta quedar una sola corrida. En los archivos, una línea en
blanco separa una corrida de la siguiente.
"""
import os
import shutil
import tempfile

_SEP = "SEP"   # fin de corrida
_EOF = "EOF"   # fin de archivo


class _Cinta:
    """Lector secuencial de un archivo con corridas separadas por línea en blanco."""

    def __init__(self, ruta):
        self.f = open(ruta)
        self.actual = None
        self.avanzar()

    def avanzar(self):
        linea = self.f.readline()
        if linea == "":
            self.actual = _EOF
        elif linea.strip() == "":
            self.actual = _SEP
        else:
            self.actual = int(linea)

    def hay_dato(self):
        return self.actual != _SEP and self.actual != _EOF

    def cerrar(self):
        self.f.close()


def _distribuir(lista, ruta_f1, ruta_f2, ascendente):
    """Reparte las corridas naturales de `lista` alternadamente. Regresa # de corridas."""
    corridas = 0
    with open(ruta_f1, "w") as f1, open(ruta_f2, "w") as f2:
        destino = f1
        anterior = None
        for x in lista:
            if anterior is not None:
                rompe = x < anterior if ascendente else x > anterior
                if rompe:                       # termina la corrida actual
                    destino.write("\n")
                    corridas += 1
                    destino = f2 if destino is f1 else f1
            destino.write(f"{x}\n")
            anterior = x
        if anterior is not None:
            destino.write("\n")
            corridas += 1
    return corridas


def _fusionar(ruta_a, ruta_b, ruta_g1, ruta_g2, ascendente):
    """Intercala corrida a corrida A y B hacia G1/G2 alternadamente. Regresa # de corridas."""
    a, b = _Cinta(ruta_a), _Cinta(ruta_b)
    corridas = 0
    with open(ruta_g1, "w") as g1, open(ruta_g2, "w") as g2:
        salida = g1
        while a.actual != _EOF or b.actual != _EOF:
            while a.hay_dato() and b.hay_dato():
                if (a.actual <= b.actual) if ascendente else (a.actual >= b.actual):
                    salida.write(f"{a.actual}\n")
                    a.avanzar()
                else:
                    salida.write(f"{b.actual}\n")
                    b.avanzar()
            while a.hay_dato():
                salida.write(f"{a.actual}\n")
                a.avanzar()
            while b.hay_dato():
                salida.write(f"{b.actual}\n")
                b.avanzar()
            salida.write("\n")
            corridas += 1
            salida = g2 if salida is g1 else g1
            if a.actual == _SEP:
                a.avanzar()
            if b.actual == _SEP:
                b.avanzar()
    a.cerrar()
    b.cerrar()
    return corridas


def mezcla_equilibrada(lista, ascendente=True):
    """Regresa una copia ordenada de `lista` con Mezcla Equilibrada Natural."""
    if len(lista) < 2:
        return list(lista)

    carpeta = tempfile.mkdtemp(prefix="mezcla_equilibrada_")
    r = {nombre: os.path.join(carpeta, nombre + ".txt") for nombre in ("F1", "F2", "G1", "G2")}
    try:
        corridas = _distribuir(lista, r["F1"], r["F2"], ascendente)
        entrada = (r["F1"], r["F2"])
        salida = (r["G1"], r["G2"])
        resultado = entrada[0]
        while corridas > 1:
            corridas = _fusionar(entrada[0], entrada[1], salida[0], salida[1], ascendente)
            entrada, salida = salida, entrada       # los de salida son ahora la entrada
            resultado = entrada[0]
        with open(resultado) as f:
            return [int(l) for l in f if l.strip()]
    finally:
        shutil.rmtree(carpeta, ignore_errors=True)


ordenar = mezcla_equilibrada