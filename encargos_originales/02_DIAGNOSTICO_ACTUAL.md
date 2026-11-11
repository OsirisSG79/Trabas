# 02 · DIAGNÓSTICO ACTUAL

## El punto exacto

`codigo/arbol_proyecto/reporte_bmg.py` → función `_poblar_lista()` (hacia las líneas 535-563).

Antes de escribir los casos de la corrida, **limpia toda la matriz**:

```python
    for fila in range(8, max(hoja.max_row, ultimo)+1):
        for col in range(1, 56):
            celda=hoja.cell(fila,col); celda.value=None; celda.hyperlink=None; celda.comment=None
```

Y después, al escribir cada caso, `_escribir_fila()` asigna el valor de todos los campos de la
plantilla, incluidos los que no tienen evidencia —con `None`—:

```python
    for indice, clave in enumerate(CLAVES_PLANTILLA, start=1):
        valor = _campo(resultado, clave)
        ...
        celda = hoja.cell(fila, indice)
        ...
        celda.value = valor        # None si esta corrida no leyó ese campo
```

Resultado mecánico: **lo que la corrida no vuelve a leer, se pierde**. No es una decisión
explícita del código en ningún sitio; es la combinación de "limpiar todo" + "escribir también
los vacíos".

La misma función se ejecuta dos veces por corrida: sobre `Versuchsmatrix` y sobre la hoja
espejo `Rangos` (`_copiar_lista_a_rangos`), de ahí que las 141 celdas sean 282 en el libro.

## La prueba A/B

Se simula una corrida con **poca evidencia** (sólo número de prueba, temperatura, número de
parte, variante, serie y tipo de generador — exactamente lo que la corrida real supo leer)
sobre un libro que ya está lleno (`libros/versionV16_0_51.xlsx`). Se aplica el motor sin la
corrección y con la corrección, y se mide contra la referencia con `herramientas/cierre_libro.py`:

| Motor | Coincide | Huecos | Nota |
|---|---|---|---|
| Sin corrección (el que está en el árbol) | 48 | 141 | **58/200 = 29,0 %** |
| Con corrección | 188 | 1 | **198/200 = 99,0 %** |

El número del motor sin corregir coincide **exactamente** con el de la corrida real del
cliente (58/200 = 29,0 %, 141 huecos): la simulación reproduce el fallo, no lo aproxima.

La única diferencia entre las dos ramas es que la corregida no borra.

Reproducible: `04_REPRODUCIR.md`, apartado C.

## La corrección ya propuesta

`herramientas/corregir_borrado_libro.py` (se instala en el árbol como
`corregir_borrado_libro.py`). Hace tres inserciones en `reporte_bmg.py`, sin reemplazar el
archivo:

1. Antes de limpiar: `previos=_previos_por_caso(hoja)` — guarda lo escrito **indexado por
   número de prueba** (no por fila, que cambia de sitio entre corridas).
2. Al escribir cada caso: `_conservar_previos(hoja, fila, resultado, previos, informe)` —
   devuelve a la fila lo que la corrida no escribió. **Nunca pisa** un valor nuevo: si la
   corrida trae dato, manda la corrida.
3. Al final: `ULTIMA_CONSERVACION[hoja.title]=...` — deja constancia de cuántas celdas se
   conservaron.

Se aplica buscando tres anclajes de texto exactos, cada uno debe aparecer **una sola vez**;
si el archivo del usuario es de otra versión, no toca nada y dice cuál falló. Verifica con
`ast.parse` y con una **prueba real**: importa el módulo corregido, monta un libro con datos
viejos, ejecuta `_poblar_lista` con un caso sin evidencia y comprueba que los datos siguen
ahí. Si la prueba falla, repone el original.

Medido: en la simulación conserva 143 celdas por hoja y deja el libro en 99 %.

## Lo que sigue abierto

### (a) El tablero no produce evidencia

En la corrida real, la hoja `Trazabilidad` **no tiene ni una fila** de
`dashboard_part_number`, `dashboard_serial_number`, `dashboard_date` ni
`dashboard_engineering_level`. En el libro de referencia que trae el parche sí las hay
(18 + 18 + 2 + 4 filas). Consecuencia: las columnas O, P, Q, R, S, T quedan vacías siempre, y
queda un hueco que ni la recuperación puede tapar (`232564 · dashboard_date`).

Hipótesis sin confirmar: el paso del tablero (`utilidades/tablero_pipeline.py`,
`evidencia_tablero.py`, `utilidades/tablero_anclas.py`) no se está invocando en la corrida
real, o se invoca sin fotos de tablero en la ruta. **No verificado**: no hay fotos en este
paquete.

### (b) Semana / Motivo / Fecha / Lugar nunca se rellenan

`week`, `test_reason`, `test_date` y `test_place` no aparecen en la `Trazabilidad` real. Las
fuentes previstas están en `utilidades/barra_estado.py` (barra de estado del vídeo),
`utilidades/pizarra.py` (pizarra escrita a mano) y la estructura de carpetas
(`ruta_carpeta`). El diccionario del propio libro (`hoja «Diccionario de datos»`) dice:

- `week`: «Sólo perfil EDAG: WW del número de prueba WWYYNN, corroborado con la fecha».
- `test_reason`: «Proyecto o pizarra explícitos o confirmación manual; **no inferir**».
- `test_place`: «EDAG Testlab explícito en overlay o laboratorio VW con prueba prefijada VW.
  El fabricante VW AG en una etiqueta no identifica el laboratorio».

O sea: hay una derivación reglada que **sí** sería legítima (la semana desde el número de
prueba) y otras dos que exigen evidencia y no deben inventarse. Queda por decidir si el
pipeline debe derivar la semana y abrir duda donde no haya evidencia, en vez de dejar la celda
muda.

### (c) Riesgo de la corrección que hay que revisar

`_conservar_previos` empareja por **número de prueba** (columna C, seis cifras). Casos límite
que conviene que alguien revise a fondo:

- dos filas con el mismo número de prueba (1ST y 2ST; las 2ST empiezan en la fila 58);
- un caso cuya numeración cambia entre corridas (corrección manual del número);
- filas históricas que ya no aparecen en la corrida (hoy se limpian y se pierden: ¿es lo
  deseado?);
- la interacción con `_copiar_estilo_fila`, con los `merge` de la banda de cabeceras y con
  `_poblar_matriz` (hoja `Übersicht`, que tiene su propia limpieza
  `_limpiar_bloques_historicos_matriz`).

## Versiones del motor que hay en el paquete

Para comparar evolución (las tres contienen la misma limpieza):

| Archivo | Origen |
|---|---|
| `codigo/arbol_proyecto/reporte_bmg.py` | árbol del proyecto (versión más reciente, 1 357 líneas) |
| `codigo/versiones/reporte_bmg_p49.py` | copia de otra rama del proyecto |
| `codigo/versiones/reporte_bmg_v16_0_21.py` | versión antigua (payload del instalador V16.0.21) |
