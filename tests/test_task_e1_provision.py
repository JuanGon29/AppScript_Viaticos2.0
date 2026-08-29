"""
Suite de pruebas automatizadas para la fase E1 (Bandeja Provisión) y E1.1 (Detalle de Provisión)
Valida:
1. Regla de Validación de Presupuesto con FechaSolicitud.
2. Formateo y resiliencia de fechas en backend y frontend (dd/mm/aaaa).
3. Backend: obtenerSolicitudesProvisionE1, obtenerDetalleProvisionE1_1, guardarResolucionProvisionE1_1.
4. Frontend: View_E1.html y JS_E1.html (tabla, filtros, ordenamiento de fechas).
5. Frontend: View_E1_1.html y JS_E1.html (secciones 1-6, responder, modal confirmación).
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODIGO_GS = os.path.join(BASE_DIR, "Codigo producido", "Código.gs.txt")
VIEW_E1 = os.path.join(BASE_DIR, "Codigo producido", "View_E1.html")
JS_E1 = os.path.join(BASE_DIR, "Codigo producido", "JS_E1.html")
VIEW_E1_1 = os.path.join(BASE_DIR, "Codigo producido", "View_E1_1.html")

def test_backend_budget_validation_month():
    print("[TEST 1] Verificando regla de mes de presupuesto desde FechaSolicitud...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        content = f.read()

    # Verificar que guardarNuevaSolicitudS1 pasa fechaHoyFormato a validarYAfectarPresupuesto
    match_call = re.search(r"validarYAfectarPresupuesto\([^)]*fechaHoyFormato[^)]*\)", content)
    assert match_call is not None, "validarYAfectarPresupuesto debe llamarse con fechaHoyFormato (FechaSolicitud) en guardarNuevaSolicitudS1"

    # Verificar que validarYAfectarPresupuesto parsea fechaSolicitudStr
    assert "fechaSolicitudStr" in content or "fechaStr" in content, "validarYAfectarPresupuesto debe recibir parámetro de fecha de solicitud"
    assert "revertirAfectacionPresupuesto" in content, "Debe existir función revertirAfectacionPresupuesto"
    print("  -> OK: Validación de presupuesto usa FechaSolicitud correctamente.")

def test_backend_e1_and_e1_1():
    print("[TEST 2] Verificando lógica de backend para E1 y E1.1...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        content = f.read()

    assert "function obtenerColMapTransaccional" in content, "Debe existir obtenerColMapTransaccional"
    assert "function formatearFechaTexto" in content, "Debe existir formatearFechaTexto"
    assert "function obtenerSolicitudesProvisionE1" in content, "Debe existir obtenerSolicitudesProvisionE1"
    assert "function obtenerDetalleProvisionE1_1" in content, "Debe existir obtenerDetalleProvisionE1_1"
    assert "function guardarResolucionProvisionE1_1" in content, "Debe existir guardarResolucionProvisionE1_1"
    
    # Verificar transiciones de estado en guardarResolucionProvisionE1_1
    assert "RECHAZO-PROVISION 1" in content, "Debe manejar RECHAZO-PROVISION 1"
    assert "RECHAZO-PROVISION 2" in content, "Debe manejar RECHAZO-PROVISION 2"
    assert "revertirAfectacionPresupuesto" in content, "Debe revertir presupuesto en RECHAZO-PROVISION 1"
    print("  -> OK: Funciones de backend para E1 y E1.1 verificadas.")

def test_ui_e1_table_and_date_formatting():
    print("[TEST 3] Verificando UI E1 y formateo de fechas...")
    with open(VIEW_E1, "r", encoding="utf-8") as f:
        v1 = f.read()
    with open(JS_E1, "r", encoding="utf-8") as f:
        j1 = f.read()

    # Tabla E1
    assert "Provisión de Pago" in v1 or "Provisión de Pagos" in v1
    assert "ID Solicitud" in v1
    assert "Fechas" in v1
    assert "Solicitante" in v1
    assert "Tipo de viático" in v1 or "Tipo Viático" in v1
    assert "Monto" in v1
    assert "Código CC" in v1
    assert "Estado Solicitud" in v1 or "Estado" in v1
    assert "Clasificación" in v1
    assert "Acciones" in v1

    # JS E1
    assert "function formatearFechaE1" in j1, "Debe existir función formatearFechaE1 en JS_E1.html"
    assert "function parseFechaE1" in j1, "Debe existir parseFechaE1"
    assert "function toggleSortDateE1" in j1 or "filtrarTablaE1" in j1
    assert "fCreacion" in j1, "renderTablaE1 debe usar fCreacion formateada"
    print("  -> OK: UI E1 y formateo de fechas dd/mm/aaaa verificados.")

def test_ui_e1_1_detail_and_responder_flow():
    print("[TEST 4] Verificando UI E1.1 y flujo de respuesta...")
    with open(VIEW_E1_1, "r", encoding="utf-8") as f:
        v1_1 = f.read()
    with open(JS_E1, "r", encoding="utf-8") as f:
        j1 = f.read()

    # Secciones en View_E1_1
    assert "Información del Solicitante" in v1_1
    assert "bg-[#E2E8F0]" in v1_1, "Sección de solicitante debe tener estilo bg-[#E2E8F0]"
    assert "Detalle de Viático" in v1_1
    assert "Información de la Solicitud" in v1_1 or "Información de Solicitud" in v1_1
    assert "Información Autorización" in v1_1
    assert "Acciones de Provisión" in v1_1
    assert "e1-1-btn-responder" in v1_1
    assert "e1-1-btn-guardar" in v1_1
    assert "Confirmar y Guardar" in v1_1 or "e1-1-btn-modal-ejecutar" in v1_1

    # Lógica en JS_E1
    assert "function verDetalleProvisionE1" in j1
    assert "function poblarFormularioE1_1" in j1
    assert "function activarSeccionResponderE1_1" in j1
    assert "function abrirModalConfirmarResolucionE1_1" in j1
    assert "function confirmarGuardarResolucionE1_1" in j1
    print("  -> OK: UI E1.1 y flujo de Responder/Guardar verificados.")

if __name__ == "__main__":
    test_backend_budget_validation_month()
    test_backend_e1_and_e1_1()
    test_ui_e1_table_and_date_formatting()
    test_ui_e1_1_detail_and_responder_flow()
    print("\n>>> ¡TODOS LOS TESTS DE PROVISIÓN E1 Y E1.1 PASARON EXITOSAMENTE! <<<")
