# Tareas del Proyecto - Portal de Viáticos V3 MVP

## Fase: Módulo E2 y E2.1 (Procesamiento de Pagos - Tesorería) [COMPLETADA]
- [x] **Tarea 1 (Backend E2/E2.1 en `Código.gs.txt`)**: Completada con `obtenerColMapTransaccional(headers)`.
- [x] **Tarea 2 (UI & Lógica de Bandeja E2 en `View_E2.html` y `JS_E2.html`)**: Completada con 9 columnas oficiales.
- [x] **Tarea 3 (UI & Lógica de Detalle E2.1 en `View_E2_1.html` y `JS_E2.html`)**: Completada con spans de texto e iconografía FontAwesome.
- [x] **Tarea 4 (Alineación Visual de E1.1 con FontAwesome)**: Completada.
- [x] **Tarea 5 (Suite de Pruebas & Compilación SPA)**: Completada.

## Fase: Módulo S3 y S3.1 (Cierre y Liquidación de Solicitudes - Solicitante) [COMPLETADA]
- [x] **Tarea 1 (Backend S3/S3.1 en `Código.gs.txt`)**: Completada.
- [x] **Tarea 2 (UI & Lógica de Bandeja S3 en `View_S3.html` y `JS_S3.html`)**: Completada con 8 columnas oficiales.
- [x] **Tarea 3 (UI & Lógica de Detalle S3.1 en `View_S3_1.html` y `JS_S3.html`)**: Completada con spans de texto, tablas de auditoría y acciones de cierre.
- [x] **Tarea 4 (Suite de Pruebas Integrada S3/S3.1 & Compilación SPA)**: Completada.

## Fase: Corrección Global de Scrolling y Módulo E3 / E3.1 (Cierre de Solicitudes - Compras) [COMPLETADA]
- [x] **Tarea 0 (Corrección Global de Scrolling en Vistas de Detalle)**: Completada.
- [x] **Tarea 1 (Backend E3 y E3.1 en `Código.gs.txt`)**: Completada.
- [x] **Tarea 2 (UI & Lógica de Bandeja E3 en `View_E3.html` y `JS_E3.html`)**: Completada con 9 columnas oficiales y modal de agrupación contable.
- [x] **Tarea 3 (UI & Lógica de Detalle E3.1 en `View_E3_1.html` y `JS_E3.html`)**: Completada con 7 secciones e iconografía FontAwesome.
- [x] **Tarea 4 (Suite de Pruebas Integrada E3/E3.1 & Compilación SPA)**: Completada (30/30 tests pasando).

## Fase: Módulo S2 y S2.1 (Solicitudes Rechazadas y Multi-Resolución) & Corrección de DatosAutorizacion
- [x] **Tarea 1 (Corrección de Reglas de `DatosAutorizacion` y Backend Apps Script para S2 y S2.1 en `Código.gs.txt`)**: Asegurar que `DatosAutorizacion` sea exclusivo de autorizadores (nivel 0 reservado a Jefe Regional de Agencias, array inicial `[]` sin registro del solicitante), refactorizar `obtenerSolicitudesRechazadas`, `obtenerDetalleSolicitudRechazada` y `resolverRechazoS2_1` con los 5 flujos operativos de rechazo.
- [x] **Tarea 2 (UI & Lógica de Bandeja S2 en `View_S2.html` y `JS_S2.html`)**: Implementar 8 columnas oficiales, eliminar columna y filtro redundante de Solicitante, barra de 5 filtros reactivos, botón `Limpiar filtros`, paginación (10, 20, 30) y badges de estado con FontAwesome.
- [x] **Tarea 3 (UI & Lógica de Detalle y Multi-Resolución S2.1 en `View_S2_1.html` y `JS_S2.html`)**: Estructura visual con FontAwesome, Sección 1 inputs limpios `#E2E8F0`, Sección 2 adaptable (readonly para `RECHAZO-PRESUPUESTO` / `RECHAZO-CIERRE`; editable precargado para `RECHAZO-PROVISION 1/2` y `RECHAZO-PAGO 1`), tablas informativas de retroalimentación de Compras/Tesorería, Sección 4 con justificación obligatoria o acciones de cierre, y modales de confirmación.
- [x] **Tarea 4 (Test Suite Integrado S2/S2.1, Regresión Total y Compilación SPA `preview_local.html`)**: Crear suite `test_task_s2_rechazadas.py`, ejecutar regresión completa del MVP (16/16 tests pasando) y compilar `preview_local.html`.

## Incidencia: Corrección de Guardado de ArchivosAdjuntos en S1 [COMPLETADA]
- [x] **Diagnóstico de Causa Raíz**:
  1. Sobrescritura de función por declaración duplicada de `guardarArchivosEnDrive` en `Código.gs.txt` (Sección 6 vs Sección 13).
  2. Incompatibilidad de nomenclatura de propiedades (`contenidoBase64` en camelCase vs `ContenidoBase64` en PascalCase).
  3. Discrepancia en parámetros de ID de carpeta en Google Drive (`ID_CARPETA_ADJUNTOS`, `ID_CARPETA_COMPROBANTES`, `ID_CARPETA_ARCHIVOS`, `ID_CARPETA_DRIVE`).
- [x] **Corrección Backend & Frontend**: Unificación de `guardarArchivosEnDrive` en Sección 6 con soporte universal de keys, eliminación de duplicado en Sección 13, normalización de payload en `JS_NuevaSolicitud.html` y re-compilación de `preview_local.html`.
- [x] **Validación y Suite de Regresión**: Creado `test_task_s1_archivos_adjuntos.py` (5/5 tests pasando, 42/42 tests globales OK).

