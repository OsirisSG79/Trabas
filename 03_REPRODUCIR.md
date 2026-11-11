# Reproducción (no instala paquetes)

Extraer el ZIP en una carpeta de análisis. Usar Python del .venv_ocr existente con openpyxl; pytest/Node sólo si ya están disponibles. Los comandos siguientes parten de la raíz CONTEXTO_V_MATRIX_P42.

```bat
"C:\Programas Base\OCR-Validacion-Excel-ocr-gpu-produccion\.venv_ocr\Scripts\python.exe" verificar_paquete.py
"C:\Programas Base\OCR-Validacion-Excel-ocr-gpu-produccion\.venv_ocr\Scripts\python.exe" codigo\cierre_libro.py --libro libros\versionV16_0_52_V16_0_52_FE.z.xlsx --referencia libros\Book-10-Examples_CORREGIDO.xlsx
mkdir salida_prueba
"C:\Programas Base\OCR-Validacion-Excel-ocr-gpu-produccion\.venv_ocr\Scripts\python.exe" herramientas\simular_borrado.py --motor codigo --libro libros\versionV16_0_51.xlsx --evidencia libros\versionV16_0_52_real.xlsx --salida salida_prueba\simulacion.xlsx
"C:\Programas Base\OCR-Validacion-Excel-ocr-gpu-produccion\.venv_ocr\Scripts\python.exe" codigo\cierre_libro.py --libro salida_prueba\simulacion.xlsx --referencia libros\Book-10-Examples_CORREGIDO.xlsx
```

Resultado esperado: FE.z 52/200; simulación 198/200. Crear una carpeta salida_prueba nueva en cada ejecución. La simulación llama _poblar_lista y no ejecuta OCR ni el pipeline completo.

Desde codigo, en entorno QA preparado:
```bat
"C:\Programas Base\OCR-Validacion-Excel-ocr-gpu-produccion\.venv_ocr\Scripts\python.exe" -m pytest pruebas/
node --test pruebas/*.cjs
```

No afirmar que estos comandos se ejecutaron exitosamente en Windows: son instrucciones de reproducción. Las mediciones_actuales se ejecutaron en el entorno de análisis con Python/openpyxl. El expediente no incluye instalador, entorno OCR ni modelos. La integración local que ejecutará el lector dentro de la corrida normal es precisamente el código que debe aportar la propuesta.
