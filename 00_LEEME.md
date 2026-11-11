# Contexto para proponer y probar una solución de V-Matrix P42

Fecha: 11 de noviembre de 2026. Este ZIP es un expediente de diagnóstico y código, NO una versión reparada ni un instalador. Leer 01_DIAGNOSTICO.md, 02_ENCARGO_SOLUCION.md y 03_REPRODUCIR.md antes de modificar código.

## Contenido y procedencia
- codigo/: fuentes activas, pruebas, scripts y contratos del checkout local 03ff75a49430f8ca86730b98eb92b9075977290e. Es un commit local de revisión; no confundirlo con un commit publicado.
- Rama remota consultada anteriormente: actualizacion-v16.0.52-p42-r3, head 14aba6a378c338457d4732c8321ad1c4742dacf8. main: 16f6b18f0c91c36540922598eee2bd6b3924f1d0. Repositorio: https://github.com/OsirisSG/OCR-Validacion-Excel
- libros/: cuatro originales sin editar: referencia CORREGIDO, estado anterior V51, corrida real anterior V52 y última corrida FE.z.
- mediciones_actuales/: comparación repetida al construir este paquete.
- encargos_originales/: MD del usuario; sus inventarios describen un paquete mayor y NO garantizan que todos esos archivos estén en este ZIP.
- evidencia_historica_NO_REUTILIZAR/: JSON antiguos, sólo para investigar. No tratarlos como resultados nuevos ni como autorización humana vigente.
- resultados_historicos/: registros de pruebas anteriores, no una certificación actual.
- auditoria_previa/: revisión anterior; afirmaciones sobre libros faltantes quedaron superadas al recibir los adjuntos.
- MANIFIESTO_SHA256.json y verificar_paquete.py: integridad de cada archivo incluido.

No se incluyen fotos privadas, videos, bases SQLite, cachés, entorno virtual, modelos OCR, credenciales ni el diagnóstico ZIP completo. El código incluye referencias a recursos externos a este expediente. Se necesita el entorno local existente para una corrida real; no instalar dependencias por red en el cliente. Los archivos señalados como implicados no están todos demostrados defectuosos.
