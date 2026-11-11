# 03 · ENCARGO Y PREGUNTAS

## Restricciones del proyecto (no negociables)

1. **Nunca inventar un dato.** Si no hay evidencia, la celda se queda vacía o se abre una duda
   para que la revise una persona. Está escrito en el diccionario del propio libro.
2. **Nunca pisar un valor existente** salvo que una persona lo pida explícitamente. Regla del
   proyecto desde P08.
3. **La red del cliente bloquea PyPI.** Cualquier propuesta que necesite descargar paquetes no
   sirve tal cual.
4. **Windows + Python 3.12 dentro de un `.venv_ocr`.** Nada de rutas con supuestos de Linux.
5. **El libro es de la empresa**: no se reescribe la fila de encabezados ni se cambia el
   formato institucional desde el motor (otra herramienta aparte sí ajusta anchos, con permiso).
6. El trabajo se entrega como código que se pueda **verificar y revertir**, con copia previa.

## Preguntas, por orden de importancia

### P1 · ¿Hay más sitios que borren?

Auditar `codigo/arbol_proyecto/` completo buscando todo lo que pueda dejar en blanco un dato
ya escrito: asignaciones de `None`/`""` sobre celdas, `delete_rows`, recreación de hojas,
`Workbook()` sobre plantillas, limpiezas por rango. Devolver una tabla:

| archivo:línea | qué hace | ¿borra datos del usuario? | riesgo |

El punto conocido es `reporte_bmg.py:_poblar_lista` (limpieza A:BC filas 8-107) y
`_limpiar_bloques_historicos_matriz` (D:J filas 7-16 y 33-42). Lo que interesa es el resto.

### P2 · ¿La corrección propuesta es suficiente o rompe algo?

Revisar `herramientas/corregir_borrado_libro.py` contra `reporte_bmg.py`. En particular:

- ¿Es correcto emparejar por número de prueba? ¿Qué pasa con dos filas del mismo número
  (1ST/2ST, filas 8-57 y 58+)?
- ¿Puede la conservación "resucitar" un dato que el flujo borró **a propósito**? ¿Existe ese
  caso hoy?
- ¿Se pierden filas históricas que no aparecen en la corrida? ¿Debería conservarlas?
- ¿La interacción con `_copiar_estilo_fila` (que copia estilos de las filas 8/58) deja celdas
  con formato incoherente al reutilizar una fila?
- ¿Afecta a `Rangos` (hoja espejo) de forma distinta que a `Versuchsmatrix`?

### P3 · El tablero no deja evidencia

`Trazabilidad` no tiene ni una fila de campos `dashboard_*` en la corrida real, y el libro de
referencia sí. Seguir el rastro de llamadas desde el orquestador hasta
`utilidades/tablero_pipeline.py`, `evidencia_tablero.py` y `utilidades/tablero_anclas.py`, y
decir **en qué condición** ese paso no produce nada. Si hace falta, proponer qué mirar en el
equipo del cliente (¿qué tiene que haber en la carpeta para que se dispare?).

### P4 · Semana / Motivo / Fecha / Lugar

Con las reglas del diccionario del libro (ver `02_DIAGNOSTICO_ACTUAL.md`, apartado b),
proponer:

- ¿Debe el pipeline derivar `week` del número de prueba (WWYYNN) cuando la fecha lo corrobora?
  ¿Con qué guardas?
- Para `test_reason` y `test_place`, ¿la respuesta correcta es abrir duda
  (`utilidades/cola_dudas.py`, `dudas_y_opciones.py`) en vez de dejar la celda vacía en
  silencio?
- ¿Dónde se pierde hoy esa información entre la carpeta de fotos y el libro?

### P5 · La propuesta

Entregar el arreglo como **diff unificado** (o archivos completos si el diff es confuso), con:

- qué archivo y qué función toca;
- qué pruebas lo respaldan (idealmente ejecutables sin fotos: sobre libros sintéticos, como
  hace `herramientas/corregir_borrado_libro.py`);
- qué riesgo tiene y cómo se revierte;
- qué NO arregla.

## Cómo se va a verificar la propuesta

Con las mismas tres mediciones que ya están en el paquete:

1. `herramientas/cierre_libro.py` contra `libros/Book-10-Examples_CORREGIDO.xlsx`
   (debe dar ≥ 198/200 con la evidencia parcial simulada).
2. La prueba de conservación (`corregir_borrado_libro.py --probar`).
3. Que los libros de entrada queden intactos y que el resultado conserve las 11 imágenes y
   comentarios internos del `.xlsx`.

Todo eso se puede repetir aquí: ver `04_REPRODUCIR.md`.

## Formato de la respuesta esperada

1. **Diagnóstico**: qué borra, dónde, y por qué ocurre aunque "no esté escrito en ningún sitio".
2. **Auditoría**: tabla de P1.
3. **Propuesta**: diff + pruebas.
4. **Riesgos y límites**: qué no cubre.
5. **Siguiente paso concreto**: qué haría falta para cerrar el tablero (P3).
