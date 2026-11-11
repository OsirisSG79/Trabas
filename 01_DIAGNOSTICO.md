# Qué falla y qué está demostrado

## Resultado más reciente
FE.z produce 42 coincidencias, 148 huecos, 0 discrepancias, 0 sobrantes y 10 sin dato: 52/200 cerradas, 26 %. El porcentaje incluye diez celdas sin dato en ambos libros; no son diez extracciones correctas. Se mide Versuchsmatrix A:T para los diez casos de la referencia, NO todo el libro.

La Trazabilidad de FE.z tiene 513 filas de evidencia y ninguna dashboard_*. Hay 83 _fecha_ambigua, 41 _nivel_por_identificar, 9 _fecha_por_identificar y 8 _serial_por_identificar. Esto acredita falta de candidatos especializados en esta salida, no prueba por sí solo qué configuración ejecutó el cliente ni que cada hueco sea culpa del escritor Excel.

## Dos problemas distintos
1. Conservación: _poblar_lista anteriormente limpiaba y reescribía rangos. La revisión usa escritura aditiva, conserva filas históricas y rechaza números ambiguos. La simulación V51 + seis campos de la corrida real mantiene 198/200 (188 coincidencias + 10 sin dato). Conservó las 11 imágenes y comentarios en Versuchsmatrix/Rangos. NO es extracción desde fotos.
2. Extracción e integración: la corrida normal no incorpora la salida especializada P42 antes de consolidar cada caso. Mantener datos previos no llena una plantilla vacía. La integración no se ha implementado todavía.

## Mapa para investigar
| Archivo / función | Papel y punto a resolver |
|---|---|
| pipeline.py | Orquesta validar_lote_empresarial y generar_excel; integrar aislamiento de corrida y salida nueva. |
| validacion.py / validar_lote_empresarial | Recoge OCR genérico, barra y QR alrededor de línea 785; consolidar_caso alrededor de 932. Falta incorporar candidatos especializados antes de consolidar. |
| flujo_empresarial.py / consolidar_caso | Contrato de candidatos, corroboración, autoridad manual, campos pendientes. No saltarse filtros para lograr más celdas. |
| evidencia_tablero.py | Reutilizar _solo_clase, filtrar_fechas, consensuar_completo, cerrar. No reinventar consenso. |
| buscar_mas.py | Segunda pasada: fechas_de_una_foto y clase_de_pegatina; debe conectar lecturas frescas al cierre. |
| leer_tablero_lote.py | Usa /tmp y parcial compartido; requiere aislamiento portable y tratamiento de errores. |
| auditar_cobertura.py | miradas infiere examen desde lecturas y usa nombres sin carpeta; no distingue examen sin lectura ni colisiones VOR/NACH. Adaptar productores y consumidores conjuntamente. |
| utilidades/tablero_pipeline.py y tablero_anclas.py | Ruta de anclas/propuestas; no asumir que equivale por sí sola al flujo P42 ampliado. |
| reporte_bmg.py | _poblar_lista preserva datos; _crear_trazabilidad usa candidatos. Otras funciones recrean hojas derivadas: sigue habiendo riesgo para anotaciones humanas allí. |
| rellenar_tablero_p42.py | Herramienta aparte, no conecta automáticamente la corrida normal; revisar identidad por número y metadatos fijos antes de reutilizarla. |
| utilidades/cola_dudas.py y dudas_y_opciones.py | Exponer estados y opciones sin publicar dudas como hechos. |

## 232564: corrección importante del usuario
El conflicto ya se trabajó en P42. NACH/IMG_4408.JPG contiene el sticker localizado por la búsqueda ampliada, si está presente localmente. El JSON incluido puede preceder a esa corrección: muestra 2025-05-17 con duda y fuente antigua 2025-04-11. No usarlo para negar la corrección ni alimentar una nueva corrida. Refrescar lecturas, clase, consenso y cobertura con las fotos locales. Nunca copiar 2025-05-17 desde la referencia.

## 222504: asunto independiente
V51 contiene module_serial_number = '671 ZRZ0539983E'; la referencia '671ZRZ0539983E'. No cambiar automáticamente el dato ni contar comparación normalizada como coincidencia estricta.

## Semana / motivo / fecha / lugar
flujo_empresarial.py deriva semana ISO desde test_date sin exigir siempre el perfil EDAG. Revisar contra el contrato: perfil EDAG explícito, WWYYNN válido y corroboración de semana/año por fecha. Sin esas condiciones, pendiente. Motivo y lugar requieren evidencia explícita o confirmación; fabricante VW no equivale a laboratorio VW.

## Pruebas históricas
Última suite completa registrada: 1604 aprobadas, 63 fallidas, 79 omitidas; Node 54/54. main tuvo 68 fallos y los 63 son comunes. Eso NO los resuelve: 59 abarcan detector/consenso/FPS/publicación/paridad, 3 módulo APLICAR_PARCHE_V15_10 ausente, 1 permisos Mac. Ver nodos exactos en logs. La reejecución posterior no arrancó por ausencia de pytest; también faltaba cv2 en el entorno actual. No cambiar vídeo para este encargo ni esconder fallos.
