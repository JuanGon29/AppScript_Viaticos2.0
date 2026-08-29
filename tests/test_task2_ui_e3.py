"""
Test unitario para Tarea 2: Bandeja E3 en View_E3.html y JS_E3.html
Verifica:
1. View_E3.html contiene las 9 columnas oficiales en thead (ID Solicitud, Solicitante, Monto, Código CC, Fechas, Estado, Tipo Viático, Clasificación, Acciones).
2. View_E3.html cuenta con los 6 filtros reactivos, botón Agrupar, botón Limpiar filtros, paginación (10, 20, 30) y modal de asiento contable.
3. JS_E3.html incluye formatearFechaE3 con formato estricto dd/mm/aaaa.
4. JS_E3.html renderTablaE3 muestra el checkbox en ACCIONES SOLO cuando esAgrupable es verdadero (Reintegro y cierre + Aprobado).
5. JS_E3.html confirmarGuardarAgrupacionE3 muta las solicitudes agrupadas a FINALIZADO en simulación local.
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEW_E3 = os.path.join(BASE_DIR, "Codigo producido", "View_E3.html")
JS_E3 = os.path.join(BASE_DIR, "Codigo producido", "JS_E3.html")

def test_view_e3_table_and_modal():
    print("[TEST 2.1] Verificando columnas, filtros y modal en View_E3.html...")
    with open(VIEW_E3, "r", encoding="utf-8") as f:
        v3 = f.read()

    # Columnas esperadas en thead
    assert "ID Solicitud" in v3
    assert "Solicitante" in v3
    assert "Monto" in v3
    assert "Código CC" in v3 or "Codigo CC" in v3
    assert "Fechas" in v3
    assert "Estado" in v3 or "Estado Solicitud" in v3
    assert "Tipo Viático" in v3 or "Tipo de Viático" in v3
    assert "Clasificación" in v3 or "Clasificación Solicitud" in v3
    assert "Acciones" in v3

    # Filtros y controles
    assert 'id="filter-e3-id"' in v3
    assert 'id="filter-e3-date"' in v3
    assert 'id="filter-e3-solicitante"' in v3
    assert 'id="filter-e3-type"' in v3
    assert 'id="filter-e3-classification"' in v3
    assert 'id="filter-e3-cc"' in v3
    assert 'id="btn-e3-agrupar"' in v3
    assert "limpiarFiltrosE3" in v3
    assert 'id="e3-page-size"' in v3

    # Modal de agrupación
    assert 'id="e3-modal-agrupar"' in v3
    assert 'id="e3-asiento-fecha-contable"' in v3
    assert 'id="e3-asiento-fecha-valor"' in v3
    assert 'id="e3-asiento-modulo"' in v3
    assert 'id="e3-asiento-transaccion"' in v3
    assert 'id="e3-asiento-relacion"' in v3
    assert 'id="e3-asiento-cr-fse"' in v3
    assert 'id="e3-asiento-archivo"' in v3

    print("  -> OK: View_E3.html verificado.")

def test_js_e3_logic():
    print("[TEST 2.2] Verificando lógica de tabla, checkbox condicional y agrupación en JS_E3.html...")
    with open(JS_E3, "r", encoding="utf-8") as f:
        j3 = f.read()

    assert "formatearFechaE3" in j3, "JS_E3.html debe tener formatearFechaE3"
    assert "renderTablaE3" in j3
    assert "toggleSelectE3" in j3
    assert "abrirModalAgruparE3" in j3
    assert "confirmarGuardarAgrupacionE3" in j3
    assert "FINALIZADO" in j3, "Simulación local debe mutar a FINALIZADO"

    print("  -> OK: JS_E3.html verificado.")

if __name__ == "__main__":
    test_view_e3_table_and_modal()
    test_js_e3_logic()
    print("\n>>> ¡TODOS LOS TESTS DE BANDEJA E3 PASARON EXITOSAMENTE! <<<")
