#!/usr/bin/env python3
"""Reproduce el borrado: misma evidencia, mismo libro de partida, dos motores.

    python3 herramientas/simular_borrado.py \
        --motor codigo/arbol_proyecto \
        --libro libros/versionV16_0_51.xlsx \
        --evidencia libros/versionV16_0_52_real.xlsx \
        --salida /tmp/sim_sin.xlsx

Qué hace
--------
1. Toma el libro de partida (`--libro`), que está LLENO.
2. Mira qué columnas sobrevivieron en la corrida real (`--evidencia`) y construye con eso
   unos `resultados` equivalentes a los de esa corrida: sólo número de prueba, temperatura,
   variante, número de parte, serie y tipo de generador.
3. Llama a `_poblar_lista` del motor indicado, que es exactamente la función que escribe la
   matriz en producción.
4. Guarda el resultado para poder medirlo contra la referencia con `cierre_libro.py`.

Con `--motor` apuntando a un árbol SIN corregir sale la nota de hoy (~34 %); apuntando a uno
corregido sale ~99 %. Eso es la prueba A/B.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import openpyxl

# columnas del libro que la corrida real sí supo leer (C, F, G, H, I, M)
COLUMNAS_EVIDENCIA = {3: "test_number", 6: "temperature_condition", 7: "module_part_number",
                      8: "module_version", 9: "module_serial_number", 13: "inflator_type"}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Simula una corrida con poca evidencia y guarda el libro.")
    p.add_argument("--motor", required=True, help="carpeta que contiene reporte_bmg.py")
    p.add_argument("--libro", required=True, help="libro de partida (lleno)")
    p.add_argument("--evidencia", required=True,
                   help="libro de la corrida real: de ahí se saca qué campos se leyeron")
    p.add_argument("--salida", required=True)
    p.add_argument("--hoja", default="Versuchsmatrix")
    args = p.parse_args(argv)

    motor = Path(args.motor).expanduser().resolve()
    sys.path.insert(0, str(motor))
    import reporte_bmg as R  # noqa: E402  (se importa después de fijar la ruta)

    libro = openpyxl.load_workbook(args.libro)
    hoja = libro[args.hoja]
    corrida = openpyxl.load_workbook(args.evidencia)[args.hoja]

    resultados = []
    for fila in range(8, 18):
        numero = corrida.cell(fila, 3).value
        if numero in (None, ""):
            continue
        campos = {}
        for columna, clave in COLUMNAS_EVIDENCIA.items():
            valor = corrida.cell(fila, columna).value
            if valor not in (None, ""):
                campos[clave] = {"valor": str(valor)}
        resultados.append({"case_key": f"caso|1st|{numero}", "tipo_st": "1ST", "campos": campos})

    print(f"motor:      {motor}")
    print(f"casos:      {len(resultados)}")
    print(f"campos por caso: {sorted({c for r in resultados for c in r['campos']})}")
    R._poblar_lista(hoja, resultados, "es")
    libro.save(args.salida)
    conservadas = getattr(R, "ULTIMA_CONSERVACION", {})
    print(f"ULTIMA_CONSERVACION: {conservadas or 'el motor no la define (sin corrección)'}")
    print(f"salida: {args.salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
