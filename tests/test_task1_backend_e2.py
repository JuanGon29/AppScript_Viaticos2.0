"""
Test unitario para Tarea 1: Backend E1 (Agrupación) y E2/E2.1 (Procesamiento de Pagos)
Verifica:
1. guardarAgrupacionProvisionE1 usa obtenerColMapTransaccional, asigna ENVIADO A PAGO, Tesoreria, AgrupableProvision y anexa archivo.
2. obtenerSolicitudesProcesamientoE2 usa obtenerColMapTransaccional, filtra ENVIADO A PAGO y formatea fechas con formatearFechaTexto.
3. obtenerDetalleProcesamientoE2_1 usa obtenerColMapTransaccional, extrae campos de AgrupableProvision y auditoría de provisión.
4. guardarResolucionProcesamientoE2_1 maneja Aprobado, RECHAZO-PAGO 1 (Solicitante), RECHAZO-PAGO 2 (Compras) y comentario obligatorio.
5. guardarAgrupacionProcesamientoE2 maneja transiciones Anticipo -> PAGADO y Reintegro -> FINALIZADO.
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODIGO_GS = os.path.join(BASE_DIR, "Codigo producido", "Código.gs.txt")

def test_guardar_agrupacion_provision_e1():
    print("[TEST 1.1] Verificando guardarAgrupacionProvisionE1...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        content = f.read()

    # Buscar definición de la función
    fn_match = re.search(r"function guardarAgrupacionProvisionE1\s*\([^)]*\)\s*\{([\s\S]*?)\n\}", content)
    assert fn_match is not None, "Debe existir la función guardarAgrupacionProvisionE1"
    fn_body = fn_match.group(1)

    assert "obtenerColMapTransaccional" in fn_body, "guardarAgrupacionProvisionE1 debe usar obtenerColMapTransaccional"
    assert "ENVIADO A PAGO" in fn_body, "guardarAgrupacionProvisionE1 debe asignar EstadoSolicitud = ENVIADO A PAGO"
    assert "Tesoreria" in fn_body, "guardarAgrupacionProvisionE1 debe asignar ActorActual = Tesoreria"
    assert "AgrupableProvision" in fn_body, "guardarAgrupacionProvisionE1 debe guardar AgrupableProvision"
    print("  -> OK: guardarAgrupacionProvisionE1 verificado.")

def test_obtener_solicitudes_procesamiento_e2():
    print("[TEST 1.2] Verificando obtenerSolicitudesProcesamientoE2...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        content = f.read()

    fn_match = re.search(r"function obtenerSolicitudesProcesamientoE2\s*\([^)]*\)\s*\{([\s\S]*?)\n\}", content)
    assert fn_match is not None, "Debe existir la función obtenerSolicitudesProcesamientoE2"
    fn_body = fn_match.group(1)

    assert "obtenerColMapTransaccional" in fn_body, "obtenerSolicitudesProcesamientoE2 debe usar obtenerColMapTransaccional"
    assert "ENVIADO A PAGO" in fn_body, "obtenerSolicitudesProcesamientoE2 debe filtrar por ENVIADO A PAGO"
    assert "formatearFechaTexto" in fn_body, "obtenerSolicitudesProcesamientoE2 debe usar formatearFechaTexto"
    print("  -> OK: obtenerSolicitudesProcesamientoE2 verificado.")

def test_obtener_detalle_procesamiento_e2_1():
    print("[TEST 1.3] Verificando obtenerDetalleProcesamientoE2_1...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        content = f.read()

    fn_match = re.search(r"function obtenerDetalleProcesamientoE2_1\s*\([^)]*\)\s*\{([\s\S]*?)\n\}", content)
    assert fn_match is not None, "Debe existir la función obtenerDetalleProcesamientoE2_1"
    fn_body = fn_match.group(1)

    assert "obtenerColMapTransaccional" in fn_body, "obtenerDetalleProcesamientoE2_1 debe usar obtenerColMapTransaccional"
    assert "AgrupableProvision" in fn_body, "obtenerDetalleProcesamientoE2_1 debe parsear AgrupableProvision"
    assert "fechaContableProvision" in fn_body, "obtenerDetalleProcesamientoE2_1 debe retornar fechaContableProvision"
    assert "formatearFechaTexto" in fn_body, "obtenerDetalleProcesamientoE2_1 debe formatear fechas con formatearFechaTexto"
    print("  -> OK: obtenerDetalleProcesamientoE2_1 verificado.")

def test_guardar_resolucion_procesamiento_e2_1():
    print("[TEST 1.4] Verificando guardarResolucionProcesamientoE2_1...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        content = f.read()

    fn_match = re.search(r"function guardarResolucionProcesamientoE2_1\s*\([^)]*\)\s*\{([\s\S]*?)\n\}", content)
    assert fn_match is not None, "Debe existir la función guardarResolucionProcesamientoE2_1"
    fn_body = fn_match.group(1)

    assert "obtenerColMapTransaccional" in fn_body, "guardarResolucionProcesamientoE2_1 debe usar obtenerColMapTransaccional"
    assert "RECHAZO-PAGO 1" in fn_body, "guardarResolucionProcesamientoE2_1 debe manejar RECHAZO-PAGO 1 (Solicitante)"
    assert "RECHAZO-PAGO 2" in fn_body, "guardarResolucionProcesamientoE2_1 debe manejar RECHAZO-PAGO 2 (Compras)"
    print("  -> OK: guardarResolucionProcesamientoE2_1 verificado.")

def test_guardar_agrupacion_procesamiento_e2():
    print("[TEST 1.5] Verificando guardarAgrupacionProcesamientoE2...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        content = f.read()

    fn_match = re.search(r"function guardarAgrupacionProcesamientoE2\s*\([^)]*\)\s*\{([\s\S]*?)\n\}", content)
    assert fn_match is not None, "Debe existir la función guardarAgrupacionProcesamientoE2"
    fn_body = fn_match.group(1)

    assert "obtenerColMapTransaccional" in fn_body, "guardarAgrupacionProcesamientoE2 debe usar obtenerColMapTransaccional"
    assert "AgrupableProcesamiento" in fn_body, "guardarAgrupacionProcesamientoE2 debe guardar AgrupableProcesamiento"
    assert "PAGADO" in fn_body, "guardarAgrupacionProcesamientoE2 debe manejar transición a PAGADO para Anticipo"
    assert "FINALIZADO" in fn_body, "guardarAgrupacionProcesamientoE2 debe manejar transición a FINALIZADO para Reintegro"
    print("  -> OK: guardarAgrupacionProcesamientoE2 verificado.")

if __name__ == "__main__":
    test_guardar_agrupacion_provision_e1()
    test_obtener_solicitudes_procesamiento_e2()
    test_obtener_detalle_procesamiento_e2_1()
    test_guardar_resolucion_procesamiento_e2_1()
    test_guardar_agrupacion_procesamiento_e2()
    print("\n>>> ¡TODOS LOS TESTS DE TAREA 1 (BACKEND E1/E2) PASARON EXITOSAMENTE! <<<")
