# 01 · EL PROBLEMA

## El sistema, en tres líneas

Pipeline en Python que lee etiquetas de módulos de airbag (fotos + vídeos), identifica campos
(número de prueba, número de parte, serie, nivel de ingeniería, fechas, generador, tablero…)
y vuelca el resultado en un libro Excel institucional de la empresa (hoja `Versuchsmatrix`,
con una hoja espejo llamada `Rangos`). El libro se compara contra una **referencia rellenada a
mano** para saber cuánto acierta el sistema: 10 casos × 20 campos = **200 celdas medidas**.

Ejecución típica del usuario:

```
cd /d "C:\Programas Base\OCR-Validacion-Excel-ocr-gpu-produccion"
".venv_ocr\Scripts\python.exe" <pipeline> <carpeta de fotos>
```

## El síntoma

**Cada corrida deja en blanco celdas que ya tenían dato.** No es que el sistema no sepa
rellenarlas: es que las borra.

Medición sobre el libro real (`libros/versionV16_0_52_real.xlsx`) contra el libro inmediatamente
anterior (`libros/versionV16_0_51.xlsx`), hoja `Versuchsmatrix`, filas 8-17, columnas A-T:

| | Celdas |
|---|---|
| Con dato en el libro anterior (V16.0.51) | 141 |
| Con dato en la corrida real (V16.0.52) | **0** |
| Celdas nuevas aportadas por la corrida en esas columnas | **0** |

Es decir: **se perdieron 141 celdas y no se ganó ninguna.**

### Qué columnas exactamente (una sola hoja; se repite igual en `Rangos`)

| Col. | Campo | Celdas perdidas |
|---|---|---|
| A | Semana | 10 |
| B | Motivo de prueba | 10 |
| D | Fecha de prueba | 10 |
| E | Lugar de prueba | 10 |
| G | PAB · Número de parte | 4 |
| I | PAB · Serie | 4 |
| J | PAB · Fecha fabricación | 10 |
| K | PAB · Nivel de ingeniería | 10 |
| L | Delay ms | 1 |
| M | Tipo de generador | 3 |
| N | Proveedor de generador | 10 |
| O | Tablero · Número de parte | 10 |
| P | Tablero · Serie | 10 |
| Q | Tablero · Fecha fabricación | 9 |
| R | Tablero · Nivel de ingeniería | 10 |
| S | Apertura láser | 10 |
| T | Proveedor de tablero | 10 |

Las que sobreviven son exactamente las que la corrida **sí** supo leer del OCR: número de
prueba (C), temperatura (F), variante (H) y parte de número de parte/serie/generador
(G, I, M). Detalle celda a celda en `evidencia/celdas_perdidas.csv`.

## Por qué importa

Medido con `herramientas/cierre_libro.py` contra la referencia
(`libros/Book-10-Examples_CORREGIDO.xlsx`):

| Libro | Coincide | Huecos | Nota final |
|---|---|---|---|
| `versionV16_0_51.xlsx` (antes de la corrida) | 188 | 1 | **198/200 = 99,0 %** |
| `versionV16_0_52_real.xlsx` (corrida real) | 48 | 141 | **58/200 = 29,0 %** |
| `versionV16_0_52.xlsx` (muestra del parche) | 189 | 0 | **199/200 = 99,5 %** |

El sistema **empeora el libro que ya tenía**. En producción eso significa que cada pasada
destruye trabajo manual previo, y que la nota del sistema no mide lo que acierta sino lo que
sobrevive.

## Cronología (tres corridas idénticas)

| Archivo | Cuándo | Celdas perdidas | ¿Corregido el formato? |
|---|---|---|---|
| `versionV16_0_52_real.xlsx` | primera corrida | 141 | no |
| `versionV16_0_52_real_v2.xlsx` | segunda corrida | 141 | no |
| `versionV16_0_52_V16_0_52_r2.z.xlsx` | tercera corrida | 141 | no |

Las tres son **idénticas celda a celda** en las filas 8-17, columnas A-T (0 diferencias). El
borrado es determinista, no un caso raro.

## Lo que NO es el problema (descartado con datos)

- **No es el formato del Excel.** Los tres libros conservan el ancho de columna original
  (A = 7,14) y el contador `SUBTOTAL` en `A6`: ninguna herramienta de formato se ejecutó
  sobre ellos. El formato es un problema aparte y ya está resuelto (`ordenar_libro.py`).
- **No es la instalación del parche.** Los tres libros salen con el mismo resultado antes y
  después de instalar el super parche: el parche no toca el motor que escribe el libro.
- **No es falta de evidencia del OCR en esos campos.** El libro anterior tenía esos datos y
  la corrida real no aportó ninguno nuevo: se limitó a borrarlos.

## Un dato aparte que apareció de paso

En una de las corridas (`real_v2`) el proyecto pasó de `Jetta_Gran_Turismo` a **`Ejemplo_VW`**
en `Rangos!A2`, `Übersicht!A1` y las 526 filas de `Trazabilidad`. No se sabe si fue
intencionado. Importa porque las reglas de derivación de Semana/Motivo/Lugar dependen del
perfil del proyecto.
