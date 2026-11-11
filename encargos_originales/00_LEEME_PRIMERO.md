# 00 · LEEME PRIMERO

Paquete de contexto para un análisis externo del problema del **libro V16.0.52** del
proyecto *OCR-Validacion-Excel-ocr-gpu-produccion*.

Se ha preparado para que **Astra** pueda analizar el código y el resultado real, buscar la
causa y proponer un arreglo. El trabajo posterior (verificar la propuesta, implementarla,
probarla y empaquetarla) lo hace quien mantiene el proyecto.

---

## Qué se pide exactamente

1. **Auditar el árbol de código** buscando todo lo que pueda *borrar o dejar en blanco* datos
   que ya estaban escritos en el libro, y devolver una lista con `archivo:línea` y nivel de
   riesgo. El punto ya localizado está en `02_DIAGNOSTICO_ACTUAL.md`; lo que interesa es si
   hay **más** sitios como ése.
2. **Opinar sobre la corrección ya propuesta** (`corregir_borrado_libro.py`): si es
   suficiente, si rompe algo, y en qué casos límite fallaría.
3. **Explicar dos cosas que siguen abiertas** y proponer por dónde atacar: (a) el paso del
   *tablero* no produce ni una fila de evidencia en la corrida real; (b) las columnas
   Semana / Motivo / Fecha / Lugar no se rellenan nunca.
4. **Entregar una propuesta concreta**: parche en formato diff, con las pruebas que la
   respaldan. Cuanto más específica (archivo, función, líneas), mejor.

## Cómo está organizado

```
PROMPT_PARA_ASTRA.md      ← el texto que acompaña al zip; es el encargo, en una página
00_LEEME_PRIMERO.md        ← esto
01_EL_PROBLEMA.md          ← el síntoma, medido, y por qué importa
02_DIAGNOSTICO_ACTUAL.md   ← el código culpable, la prueba A/B y lo que sigue abierto
03_ENCARGO_Y_PREGUNTAS.md  ← el encargo detallado, con las restricciones del proyecto
04_REPRODUCIR.md           ← comandos exactos para repetir cada medición
codigo/                    ← el árbol del proyecto y las versiones del motor
libros/                    ← los .xlsx como evidencia (antes, durante y después)
evidencia/                 ← CSV de las celdas perdidas, hojas de trazabilidad, notas de cierre
herramientas/              ← los scripts de medición y de corrección, listos para correr
```

## Orden de lectura recomendado

0. `PROMPT_PARA_ASTRA.md` — el encargo tal como llega.
1. `01_EL_PROBLEMA.md` — qué se observa.
2. `02_DIAGNOSTICO_ACTUAL.md` — dónde está y cómo se demuestra.
3. `03_ENCARGO_Y_PREGUNTAS.md` — qué se espera de la respuesta.
4. El código, empezando por `codigo/arbol_proyecto/reporte_bmg.py`.

## Lo que NO va en el paquete

- **Fotos y vídeos originales del laboratorio** (varios GB, material del cliente). Por eso el
  pipeline completo no se puede reejecutar aquí; todas las mediciones se hacen sobre los
  libros ya generados, que sí van incluidos.
- Credenciales, rutas de red y datos personales.

## Estado

Todo lo que se afirma en estos documentos está medido sobre los archivos incluidos y se puede
repetir con los comandos de `04_REPRODUCIR.md`. Cuando algo es una hipótesis y no una
medición, se dice expresamente.
