# 05 · INVENTARIO DEL PAQUETE

Qué hay, para qué sirve y qué se ha dejado fuera.

## Documentos

| Archivo | Para qué |
|---|---|
| `PROMPT_PARA_ASTRA.md` | **el encargo completo**, para pegar en el chat |
| `00_LEEME_PRIMERO.md` | qué es el paquete y qué se pide |
| `01_EL_PROBLEMA.md` | el síntoma medido, columnas afectadas y cronología |
| `02_DIAGNOSTICO_ACTUAL.md` | el código culpable, la prueba A/B y lo que sigue abierto |
| `03_ENCARGO_Y_PREGUNTAS.md` | el encargo (P1-P5) y las restricciones del proyecto |
| `04_REPRODUCIR.md` | comandos para repetir cada medición |
| `05_INVENTARIO.md` | esto |
| `06_VERIFICACION_DEL_PAQUETE.md` | la salida real de las comprobaciones de control |

## `codigo/`

| Carpeta | Contenido |
|---|---|
| `arbol_proyecto/` | el árbol del proyecto (232 archivos `.py`): `reporte_bmg.py` (el motor del libro), `pipeline.py`, `flujo_empresarial.py`, `generar_excel.py`, `utilidades/` (28 módulos), `pruebas/`, `dashboard/`, `config.yaml` |
| `parche_p42/` | los módulos que se instalan sobre ese árbol con el super parche V16.0.52 |
| `versiones/` | tres versiones del motor del libro, para comparar la evolución del borrado: `reporte_bmg_p49.py`, `reporte_bmg_v16_0_21.py` y el del árbol |

Lo que se ha quitado del árbol para que el paquete sea manejable: `.git`, `.cache_ocr`,
`__pycache__`, la presentación `.pptx`, `inventario_proyecto.json` (3 MB de caché de escaneo)
y las imágenes pesadas de `datos_prueba/` (sólo se han borrado las de más de 100 KB: son fotos
de ejemplo para las pruebas unitarias, no código, y las pruebas que las usan no se pueden
correr aquí sin el OCR completo).

## `libros/`

| Archivo | Qué es | Nota de cierre |
|---|---|---|
| `Book-10-Examples.xlsx` | plantilla institucional, rellenada a mano (10 casos) | — |
| `Book-10-Examples_CORREGIDO.xlsx` | **referencia** contra la que se mide | — |
| `versionV16_0_51.xlsx` | libro antes de la corrida (lleno) | 198/200 |
| `versionV16_0_52_real.xlsx` | **la corrida que falla** | 58/200 |
| `versionV16_0_52_real_v2.xlsx` | segunda corrida (idéntica) | 58/200 |
| `versionV16_0_52_corrida_3.xlsx` | tercera corrida (idéntica) | 58/200 |
| `versionV16_0_52_reparado.xlsx` | recuperado a mano con `ordenar_libro.py --recuperar` | 198/200 |
| `versionV16_0_52.xlsx` | muestra que trae el parche, hecha a mano | 199/200 |

Todas las hojas de todos ellos están en `evidencia/hojas_y_dimensiones.txt`. Los libros
conservan sus 11 imágenes y comentarios internos: son parte del archivo de la empresa y se
puede comprobar que no se han perdido.

## `evidencia/`

| Archivo | Contenido |
|---|---|
| `celdas_perdidas.csv` | **282 filas** = 141 celdas × 2 hojas: hoja, celda, caso, campo, valor en V16.0.51 y (vacío) en la corrida real |
| `trazabilidad_v51.csv` | hoja `Trazabilidad` del libro anterior: 550 filas con regla y fuente de cada valor |
| `trazabilidad_real.csv` | la misma hoja en la corrida real: 526 filas |
| `cierre_*.txt` | salida completa de `cierre_libro.py` para cada libro |
| `hojas_y_dimensiones.txt` | hojas, dimensiones y filas con contenido de los cuatro libros principales |

La comparación de los dos CSV de trazabilidad es la pista más directa para P3: en el libro
anterior hay filas con regla `tablero` y `corregido_por_codigo`; en la corrida real no existe
ninguna de las dos.

## `herramientas/`

| Archivo | Para qué |
|---|---|
| `cierre_libro.py` | mide un libro contra la referencia (las notas de este documento) |
| `simular_borrado.py` | **la prueba A/B**: aplica `_poblar_lista` con evidencia parcial sobre un libro lleno |
| `corregir_borrado_libro.py` | la corrección propuesta, con prueba de conservación y `--revertir` |
| `ordenar_libro.py` | formato y recuperación de celdas vaciadas, con `--preguntar` (socorro, no solución) |

Todos funcionan con `python3` y `openpyxl`, sin OCR ni red.
