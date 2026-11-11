# 04 · REPRODUCIR

Todos los comandos se ejecutan **desde la raíz del paquete**. Sólo hace falta Python 3.10+ y
`openpyxl`. No hace falta OCR, ni fotos, ni red.

```
pip install openpyxl
```

---

## A · Medir un libro contra la referencia

```
python3 herramientas/cierre_libro.py \
    --libro libros/versionV16_0_52_real.xlsx \
    --referencia libros/Book-10-Examples_CORREGIDO.xlsx
```

Resultado esperado:

```
  coincide        48   (24.0 %)
  hueco          141
  discrepancia     1
  cerradas (coincide + sin dato) ... 58/200 = 29.0 %
```

Es el número del libro del cliente. Cambiando `--libro` se ve la evolución completa:

| `--libro` | cerradas |
|---|---|
| `versionV16_0_51.xlsx` (antes de la corrida) | 198/200 = 99,0 % |
| `versionV16_0_52_real.xlsx` (corrida real) | 58/200 = 29,0 % |
| `versionV16_0_52_real_v2.xlsx` | 58/200 = 29,0 % |
| `versionV16_0_52_corrida_3.xlsx` | 58/200 = 29,0 % |
| `versionV16_0_52_reparado.xlsx` (recuperado a mano) | 198/200 = 99,0 % |

---

## B · Ver que las tres corridas son idénticas

```
python3 - <<'PY'
import openpyxl
libros = ["versionV16_0_52_real.xlsx", "versionV16_0_52_real_v2.xlsx", "versionV16_0_52_corrida_3.xlsx"]
base = openpyxl.load_workbook("libros/" + libros[0])
for otro in libros[1:]:
    b = openpyxl.load_workbook("libros/" + otro)
    dif = sum(1 for h in ("Rangos", "Versuchsmatrix") for f in range(8, 18) for c in range(1, 21)
              if (base[h].cell(f, c).value or None) != (b[h].cell(f, c).value or None))
    print(f"{libros[0]} vs {otro}: {dif} celdas distintas")
PY
```

Esperado: `0 celdas distintas` las dos veces.

---

## C · La prueba A/B del borrado (la importante)

**1. Motor tal como está** (el que produjo el libro del cliente):

```
python3 herramientas/simular_borrado.py \
    --motor codigo/arbol_proyecto \
    --libro libros/versionV16_0_51.xlsx \
    --evidencia libros/versionV16_0_52_real.xlsx \
    --salida /tmp/sim_sin.xlsx

python3 herramientas/cierre_libro.py --libro /tmp/sim_sin.xlsx \
    --referencia libros/Book-10-Examples_CORREGIDO.xlsx
```

Esperado: `58/200 = 29.0 %` — el mismo número que el libro real.

**2. Motor con la corrección:**

```
cp -r codigo/arbol_proyecto /tmp/motor_corregido
python3 herramientas/corregir_borrado_libro.py --arbol /tmp/motor_corregido

python3 herramientas/simular_borrado.py \
    --motor /tmp/motor_corregido \
    --libro libros/versionV16_0_51.xlsx \
    --evidencia libros/versionV16_0_52_real.xlsx \
    --salida /tmp/sim_con.xlsx

python3 herramientas/cierre_libro.py --libro /tmp/sim_con.xlsx \
    --referencia libros/Book-10-Examples_CORREGIDO.xlsx
```

Esperado: `198/200 = 99.0 %` y `ULTIMA_CONSERVACION: {'Versuchsmatrix': 143}`.

`simular_borrado.py` construye la evidencia leyendo del libro real **sólo las columnas que la
corrida sí leyó** (C, F, G, H, I, M), llama a `_poblar_lista` —la misma función que usa
producción— y guarda el libro resultante. Nada más.

---

## D · Ver el código culpable en su contexto

```
sed -n '535,565p' codigo/arbol_proyecto/reporte_bmg.py      # _poblar_lista
sed -n '487,520p' codigo/arbol_proyecto/reporte_bmg.py      # _escribir_fila
grep -n "value=None\|value = None\|delete_rows\|Workbook(" codigo/arbol_proyecto/*.py
```

La última orden es el punto de partida de la auditoría pedida en P1.

---

## E · La corrección, paso a paso

```
python3 herramientas/corregir_borrado_libro.py --arbol codigo/arbol_proyecto --simular
```

Enseña exactamente las tres líneas que insertaría, sin escribir. Con `--probar` aplica y
ejecuta la prueba de conservación; con `--revertir` repone `reporte_bmg.py.bak`.

---

## F · Formato del libro (problema distinto, ya resuelto)

```
python3 herramientas/ordenar_libro.py --libro libros/versionV16_0_52_real.xlsx --simular
```

Ajusta anchos, parte el encabezado en líneas y saca el contador `SUBTOTAL` de `A6`. Nunca
cambia un dato; con `--recuperar <libro anterior>` devuelve las celdas vaciadas, y con
`--preguntar` pregunta celda a celda mostrando el rastro de origen de cada valor. Es la
herramienta de socorro, no la solución: la solución es que el motor no borre.
