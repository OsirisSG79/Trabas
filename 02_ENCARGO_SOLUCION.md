# Qué debe entregar la propuesta

Implementar, no sólo explicar: conectar lector P42 -> candidatos -> consolidar_caso -> dudas -> Trazabilidad -> Versuchsmatrix/Rangos. Identidad inequívoca con proyecto/caso/etapa; ante duplicados ambiguos detener publicación. No emparejar ciegamente por número.

Reutilizar consenso por valor completo y separación de clases del P42. Ejecutar búsqueda ampliada ante duda; contabilizar rutas relativas completas de fotos presentes, examinadas, descartadas con motivo, error y pendientes. Una foto no examinada no es «sin dato». No reutilizar JSON antiguo. Cada candidato debe mantener foto, recorte, texto/payload, valor original, clase/origen, regla, confianza, votos y conflicto/estado/motivo. Respetar autoridad manual, no publicar inferencias como confirmaciones y no sobrescribir celdas ocupadas.

Windows Server / Python 3.12 / .venv_ocr existente / rutas con espacios / sin PyPI ni red. Directorio único por corrida configurable mediante tempfile; opción explícita conservar/limpiar artefactos. Libro original intacto y salida nueva. No escribir datos del Book corregido: sólo evaluar contra él.

Entregar diff unificado o commits, archivos modificados, aplicación y reversión con copia previa y verificación de hash, manifiesto SHA256, simulación sintética y lanzador .bat local. Comando completo desde C:\Programas Base\OCR-Validacion-Excel-ocr-gpu-produccion. Informe local con archivos examinados y pendientes y verificación automática del libro.

## Pruebas obligatorias
- Sin fotos; foto sin ancla; OCR ausente/error.
- Fecha de módulo/proveedor separada del sticker del tablero; fechas del tablero contradictorias.
- Segunda pasada encuentra imagen omitida (regresión de 232564 sin hardcodear fecha de referencia).
- Consenso nunca fabrica una fecha inexistente; votos independientes, no giros de una foto contados como fotos distintas.
- Pendientes visibles en trazabilidad y dudas; no publicados.
- Duplicados entre etapas, nombres de foto repetidos VOR/NACH, parciales de corrida vieja, rutas con espacios.
- Preservación de valores humanos, originales, imágenes, comentarios y cabeceras institucionales.
- Guarda EDAG separada; entradas sin perfil, sin fecha, contradictorias y corroboradas.
- Ruta normal completa con OCR simulado inyectado y exportación real. Distinguirla de prueba real con fotos privadas.
- Suite completa Python y Node: registrar resultados exactos; los 63 fallos históricos no cuentan como corregidos por ser antiguos.

Enviar la propuesta como ZIP o diff contra este código, con pruebas, hipótesis y límites. Se evaluará aplicándola en una copia limpia, reproduciendo errores y verificando que no rellene datos por copia de referencia. No cambiar vídeo salvo dependencia imprescindible demostrada.
