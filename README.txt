# Sistema de Procesamiento y Ordenamiento Masivo de Datos

**Alumno:** [Nombre completo]
**Matrícula:** [Matrícula]
**Materia:** Algoritmos de Ordenamiento y Búsqueda
**Fecha:** [Fecha de entrega]

## Descripción

Aplicación con interfaz gráfica (tkinter) que carga archivos de números enteros
(o de texto), los ordena con algoritmos propios, busca valores y exporta el
resultado con el algoritmo usado y el tiempo de ejecución.

No se usa `.sort()`, `sorted()` ni librerías automáticas de ordenamiento.
`pandas` se usa únicamente para leer archivos XLSX.

## Estructura del proyecto

```
estructura/
├── main.py                      # Interfaz gráfica; conecta botones con las librerías
├── libs/
│   ├── __init__.py
│   ├── archivos.py              # Lectura TXT/XLSX y exportación
│   ├── lib_burbuja.py           # Ordenamiento interno
│   ├── lib_insercion.py         # Ordenamiento interno
│   ├── lib_seleccion.py         # Ordenamiento interno
│   ├── lib_shellsort.py         # Ordenamiento interno
│   ├── lib_quicksort.py         # Ordenamiento interno
│   ├── lib_heapsort.py          # Ordenamiento interno
│   ├── lib_radixsort.py         # Ordenamiento interno
│   ├── lib_mezcladirecta.py     # Ordenamiento externo (archivos auxiliares)
│   ├── lib_mezclaequilibrada.py # Ordenamiento externo (archivos auxiliares)
│   ├── lib_intercalacion.py     # Intercalación de dos secuencias ordenadas
│   ├── lib_busquedasecuencial.py
│   ├── lib_busquedabinaria.py
│   └── lib_busquedahash.py
├── datos/                       # Archivos de prueba (1000 TXT y 5000 XLSX)
├── salida/                      # Resultados exportados
└── README.md
```

## Requisitos

- Python 3.10 o superior
- pandas y openpyxl

```
pip install pandas openpyxl
```

## Cómo ejecutarlo

1. Clona el repositorio:
   ```
   git clone [URL del repositorio]
   cd [carpeta del repositorio]
   ```
2. Instala las dependencias (ver arriba).
3. Ejecuta desde la carpeta raíz del proyecto:
   ```
   python main.py
   ```

## Uso

1. **Cargar archivo:** abre el explorador y permite elegir un `.txt` o `.xlsx`.
   Muestra el total de registros, los primeros 20 y los últimos 20.
2. **Ordenar:** elige el algoritmo y el orden (ascendente o descendente).
   Se muestra el tiempo medido con `time.perf_counter()`.
3. **Buscar:** escribe un valor y elige secuencial, binaria o hash.
   La binaria requiere haber ordenado antes.
4. **Exportar resultados:** guarda en `salida/` el archivo ordenado y un
   resumen con algoritmo, tiempo y total de registros.

## Formato de los archivos

- **TXT:** un dato por línea. Se ignoran líneas vacías y el BOM de UTF-8.
- **XLSX:** los datos están en la primera columna y la primera fila es el
  encabezado.
- Si todos los datos son enteros se tratan como números; si alguno no lo es,
  todos se tratan como texto.
- Radix Sort, las mezclas externas y la búsqueda hash solo funcionan con
  números. La interfaz avisa si se eligen con un archivo de texto.

## Algoritmos incluidos

| Tipo | Algoritmos |
|---|---|
| Ordenamiento interno | Burbuja, Inserción, Selección, ShellSort, QuickSort, HeapSort, Radix Sort |
| Ordenamiento externo | Mezcla Directa, Mezcla Equilibrada Natural |
| Búsqueda | Secuencial, Binaria, Hash (encadenamiento) |

## Comparación básica

| Escenario | Algoritmo recomendado | Motivo |
|---|---|---|
| Datos pequeños | Inserción | Simple y rápida con pocos datos |
| Datos masivos | QuickSort / HeapSort | O(n log n); HeapSort con peor caso garantizado |
| Archivos externos | Mezcla Directa / Equilibrada | Trabajan con archivos sin cargar todo en memoria |
| Datos parcialmente ordenados | Inserción / Mezcla Natural | Aprovechan el orden que ya existe |
| Búsquedas frecuentes | Hash (o binaria con datos ordenados) | Hash O(1) promedio; binaria O(log n) |

## Resultados de tiempo

Tiempos medidos con el programa (reemplaza con los tuyos):

| Algoritmo | 1000 datos (TXT) | 5000 datos (XLSX) |
|---|---|---|
| Burbuja | [ ] s | [ ] s |
| Inserción | [ ] s | [ ] s |
| Selección | [ ] s | [ ] s |
| ShellSort | [ ] s | [ ] s |
| QuickSort | [ ] s | [ ] s |
| HeapSort | [ ] s | [ ] s |
| Radix Sort | [ ] s | [ ] s |
| Mezcla Directa | [ ] s | [ ] s |
| Mezcla Equilibrada | [ ] s | [ ] s |

## Errores encontrados y corregidos

- **BOM en el TXT:** la primera línea traía un carácter invisible y `int()`
  fallaba. Se resolvió abriendo con `encoding="utf-8-sig"`.
- **Encabezado en el XLSX:** la celda A1 era texto y rompía la conversión a
  entero. Se lee con encabezado y la primera columna con `iloc[:, 0]`.
- **Indentación del `return`:** dentro del `for`, la función regresaba un solo
  dato. Se movió al nivel de la función.
- **Import roto en la búsqueda secuencial:** apuntaba a un módulo inexistente;
  se corrigió a `from libs import lib_busquedabinaria`.
- **Carpeta de exportación:** `salida/` se creaba según la carpeta de la
  terminal. Ahora se calcula desde la ubicación de `archivos.py`.

## Limitaciones

- Burbuja, Inserción y Selección tardan varios segundos con 5000 datos y la
  ventana se congela mientras trabajan.
- Las búsquedas son de valor exacto.
- Las mezclas externas usan archivos temporales (`tempfile`).
