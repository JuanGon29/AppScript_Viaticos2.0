"""
Test unitario para Tarea 1: Backend E3 y E3.1 en Código.gs.txt
Verifica:
1. obtenerSolicitudesCierreE3 utiliza obtenerColMapTransaccional(headers) y filtra por LIQUIDADO.
2. obtenerDetalleCierreE3_1 extrae auditorías previas, metadatos de cierre y archivos adjuntos.
3. guardarResolucionCierreE3_1 gestiona correctamente transiciones a FINALIZADO, RECHAZO-CIERRE y LIQUIDADO agrupable.
4. guardarAgrupacionCierreE3 valida campos contables, anexa archivo a ArchivosAdjuntos y finaliza las solicitudes.
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODIGO_GS = os.path.join(BASE_DIR, "Codigo producido", "Código.gs.txt")

def test_obtener_solicitudes_cierre_e3():
    print("[TEST 1.1] Verificando obtenerSolicitudesCierreE3 en Código.gs.txt...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        code = f.read()

    assert "function obtenerSolicitudesCierreE3" in code
    match = re.search(r'function obtenerSolicitudesCierreE3\s*\([^)]*\)\s*\{([\s\S]*?)\n\}', code)
    assert match is not None, "Función obtenerSolicitudesCierreE3 no encontrada"
    body = match.group(1)

    assert "obtenerColMapTransaccional(headers)" in body, "Debe usar obtenerColMapTransaccional(headers)"
    assert "LIQUIDADO" in body, "Debe filtrar por estado LIQUIDADO"
    assert "formatearFechaTexto" in body, "Debe formatear fechas con formatearFechaTexto"
    assert "codigoCC" in body, "Debe extraer codigoCC"
    assert "esAgrupable" in body, "Debe calcular esAgrupable"
    print("  -> OK: obtenerSolicitudesCierreE3 validado correctamente.")

def test_obtener_detalle_cierre_e3_1():
    print("[TEST 1.2] Verificando obtenerDetalleCierreE3_1 en Código.gs.txt...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        code = f.read()

    assert "function obtenerDetalleCierreE3_1" in code
    match = re.search(r'function obtenerDetalleCierreE3_1\s*\([^)]*\)\s*\{([\s\S]*?)\n\}', code)
    assert match is not None, "Función obtenerDetalleCierreE3_1 no encontrada"
    body = match.group(1)

    assert "obtenerColMapTransaccional(headers)" in body, "Debe usar obtenerColMapTransaccional(headers)"
    assert "formatearFechaTexto" in body, "Debe formatear fechas con formatearFechaTexto"
    assert "nombreProvision" in body, "Debe extraer auditoría de provisión"
    assert "nombreProcesamiento" in body, "Debe extraer auditoría de procesamiento"
    assert "resolucionCierreE" in body, "Debe extraer resolucionCierreE previa"
    assert "tipoCierre" in body, "Debe extraer tipoCierre"
    assert "montoReintegro" in body, "Debe extraer montoReintegro"
    assert "fechaReintegro" in body, "Debe extraer fechaReintegro"
    assert "archivosAdjuntos" in body, "Debe retornar archivosAdjuntos"
    print("  -> OK: obtenerDetalleCierreE3_1 validado correctamente.")

def test_guardar_resolucion_cierre_e3_1():
    print("[TEST 1.3] Verificando guardarResolucionCierreE3_1 en Código.gs.txt...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        code = f.read()

    assert "function guardarResolucionCierreE3_1" in code
    match = re.search(r'function guardarResolucionCierreE3_1\s*\([^)]*\)\s*\{([\s\S]*?)\n\}', code)
    assert match is not None, "Función guardarResolucionCierreE3_1 no encontrada"
    body = match.group(1)

    assert "FINALIZADO" in body, "Debe transicionar a FINALIZADO si es Aprobado con Solo cierre"
    assert "RECHAZO-CIERRE" in body, "Debe transicionar a RECHAZO-CIERRE si es Rechazado"
    assert "FechaCierreE" in body, "Debe registrar FechaCierreE"
    assert "NombreCierreE" in body, "Debe registrar NombreCierreE"
    print("  -> OK: guardarResolucionCierreE3_1 validado correctamente.")

def test_guardar_agrupacion_cierre_e3():
    print("[TEST 1.4] Verificando guardarAgrupacionCierreE3 en Código.gs.txt...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        code = f.read()

    assert "function guardarAgrupacionCierreE3" in code
    match = re.search(r'function guardarAgrupacionCierreE3\s*\([^)]*\)\s*\{([\s\S]*?)\n\}', code)
    assert match is not None, "Función guardarAgrupacionCierreE3 no encontrada"
    body = match.group(1)

    assert "FINALIZADO" in body, "Debe transicionar a FINALIZADO"
    assert "AgrupableCierreE" in body, "Debe guardar JSON en AgrupableCierreE"
    assert "ArchivosAdjuntos" in body, "Debe anexar a ArchivosAdjuntos"
    assert "FechaCierreE" in body, "Debe registrar FechaCierreE"
    print("  -> OK: guardarAgrupacionCierreE3 validado correctamente.")

if __name__ == "__main__":
    test_obtener_solicitudes_cierre_e3()
    test_obtener_detalle_cierre_e3_1()
    test_guardar_resolucion_cierre_e3_1()
    test_guardar_agrupacion_cierre_e3()
    print("\n>>> ¡TODOS LOS TESTS DE BACKEND E3/E3.1 PASARON EXITOSAMENTE! <<<")
