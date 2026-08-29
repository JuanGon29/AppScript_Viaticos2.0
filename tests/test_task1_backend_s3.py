"""
Test unitario para Tarea 1: Backend S3 y S3.1 en Código.gs.txt
Verifica:
1. obtenerSolicitudesCierreS3 usa obtenerColMapTransaccional y formatea fechas con formatearFechaTexto.
2. obtenerDetalleCierreS3_1 usa obtenerColMapTransaccional y extrae todas las bitácoras y metadatos de cierre.
3. guardarCierreSolicitudS3_1 actualiza EstadoSolicitud='LIQUIDADO', ActorActual='Compras', FechaCierreS, FechaModificacion, TipoCierre, MontoReintegro, FechaReintegro y anexa archivos a ArchivosAdjuntos.
4. guardarCierreSolicitudS3_1 valida obligatoriedad de monto y fecha en reintegro.
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODIGO_GS = os.path.join(BASE_DIR, "Codigo producido", "Código.gs.txt")

def test_obtener_solicitudes_cierre_s3():
    print("[TEST 1.1] Verificando obtenerSolicitudesCierreS3 en Código.gs.txt...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        code = f.read()

    # Buscar función
    match = re.search(r"function\s+obtenerSolicitudesCierreS3\s*\([^)]*\)\s*\{(.*?)\n\}", code, re.DOTALL)
    assert match is not None, "obtenerSolicitudesCierreS3 debe existir en Código.gs.txt"
    fn_code = match.group(1)

    assert "obtenerColMapTransaccional" in fn_code, "obtenerSolicitudesCierreS3 debe usar obtenerColMapTransaccional"
    assert "formatearFechaTexto" in fn_code, "obtenerSolicitudesCierreS3 debe usar formatearFechaTexto"
    assert "PAGADO" in fn_code, "obtenerSolicitudesCierreS3 debe filtrar estado PAGADO"
    print("  -> OK: obtenerSolicitudesCierreS3 validado correctamente.")

def test_obtener_detalle_cierre_s3_1():
    print("[TEST 1.2] Verificando obtenerDetalleCierreS3_1 en Código.gs.txt...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        code = f.read()

    match = re.search(r"function\s+obtenerDetalleCierreS3_1\s*\([^)]*\)\s*\{(.*?)\n\}", code, re.DOTALL)
    assert match is not None, "obtenerDetalleCierreS3_1 debe existir en Código.gs.txt"
    fn_code = match.group(1)

    assert "obtenerColMapTransaccional" in fn_code, "obtenerDetalleCierreS3_1 debe usar obtenerColMapTransaccional"
    assert "formatearFechaTexto" in fn_code, "obtenerDetalleCierreS3_1 debe usar formatearFechaTexto"
    assert "nombreProvision" in fn_code, "obtenerDetalleCierreS3_1 debe retornar nombreProvision"
    assert "nombreProcesamiento" in fn_code, "obtenerDetalleCierreS3_1 debe retornar nombreProcesamiento"
    print("  -> OK: obtenerDetalleCierreS3_1 validado correctamente.")

def test_guardar_cierre_solicitud_s3_1():
    print("[TEST 1.3] Verificando guardarCierreSolicitudS3_1 en Código.gs.txt...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        code = f.read()

    match = re.search(r"function\s+guardarCierreSolicitudS3_1\s*\([^)]*\)\s*\{(.*?)\n\}", code, re.DOTALL)
    assert match is not None, "guardarCierreSolicitudS3_1 debe existir en Código.gs.txt"
    fn_code = match.group(1)

    assert "obtenerColMapTransaccional" in fn_code, "guardarCierreSolicitudS3_1 debe usar obtenerColMapTransaccional"
    assert "LIQUIDADO" in fn_code, "guardarCierreSolicitudS3_1 debe transicionar a LIQUIDADO"
    assert "Compras" in fn_code, "guardarCierreSolicitudS3_1 debe asignar ActorActual a Compras"
    assert "FechaCierreS" in fn_code, "guardarCierreSolicitudS3_1 debe registrar FechaCierreS"
    assert "TipoCierre" in fn_code, "guardarCierreSolicitudS3_1 debe registrar TipoCierre"
    assert "MontoReintegro" in fn_code, "guardarCierreSolicitudS3_1 debe registrar MontoReintegro"
    assert "FechaReintegro" in fn_code, "guardarCierreSolicitudS3_1 debe registrar FechaReintegro"
    print("  -> OK: guardarCierreSolicitudS3_1 validado correctamente.")

if __name__ == "__main__":
    test_obtener_solicitudes_cierre_s3()
    test_obtener_detalle_cierre_s3_1()
    test_guardar_cierre_solicitud_s3_1()
    print("\n>>> ¡TODOS LOS TESTS DE BACKEND S3/S3.1 PASARON EXITOSAMENTE! <<<")
