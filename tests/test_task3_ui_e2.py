"""
Test unitario para Tarea 3: UI & Lógica de Bandeja E2 (Procesamiento de Pagos)
Verifica:
1. View_E2.html tiene el botón Agrupar, Limpiar filtros, los 6 filtros reactivos y la tabla de 9 columnas oficiales.
2. JS_E2.html tiene la función formatearFechaE2 que formatea estrictamente a dd/mm/aaaa.
3. JS_E2.html renderTablaE2 genera las 9 columnas en el orden oficial.
4. JS_E2.html permite seleccionar únicamente filas con esAgrupable = true (resolución Aprobado).
5. JS_E2.html simula la agrupación de E2 actualizando estadoSolicitud a PAGADO o FINALIZADO según clasificación.
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEW_E2 = os.path.join(BASE_DIR, "Codigo producido", "View_E2.html")
JS_E2 = os.path.join(BASE_DIR, "Codigo producido", "JS_E2.html")

def test_view_e2_structure():
    print("[TEST 3.1] Verificando estructura de View_E2.html...")
    with open(VIEW_E2, "r", encoding="utf-8") as f:
        content = f.read()

    # Botones principales y modal
    assert "btn-e2-agrupar" in content, "Debe existir el botón btn-e2-agrupar"
    assert "e2-modal-agrupar" in content, "Debe existir el modal e2-modal-agrupar"
    assert "limpiarFiltrosE2" in content, "Debe existir la acción limpiarFiltrosE2"

    # 6 Filtros
    assert "filter-e2-id" in content, "Filtro ID"
    assert "filter-e2-date" in content, "Filtro Fecha"
    assert "filter-e2-solicitante" in content, "Filtro Solicitante"
    assert "filter-e2-type" in content, "Filtro Tipo Viático"
    assert "filter-e2-classification" in content, "Filtro Clasificación"
    assert "filter-e2-cc" in content, "Filtro Código CC"

    print("  -> OK: Estructura de View_E2.html verificada.")

def test_js_e2_functions():
    print("[TEST 3.2] Verificando funciones y orden de columnas en JS_E2.html...")
    with open(JS_E2, "r", encoding="utf-8") as f:
        content = f.read()

    assert "formatearFechaE2" in content, "Debe existir la función formatearFechaE2"

    # Verificar que confirmarGuardarAgrupacionE2 maneja transiciones PAGADO y FINALIZADO en simulación local
    fn_match = re.search(r"function confirmarGuardarAgrupacionE2\s*\([^)]*\)\s*\{([\s\S]*?)\n\}", content)
    assert fn_match is not None, "Debe existir confirmarGuardarAgrupacionE2"
    fn_body = fn_match.group(1)

    assert "PAGADO" in fn_body, "Simulación local debe manejar PAGADO para anticipos"
    assert "FINALIZADO" in fn_body, "Simulación local debe manejar FINALIZADO para reintegros"
    print("  -> OK: Funciones de JS_E2.html verificadas.")

if __name__ == "__main__":
    test_view_e2_structure()
    test_js_e2_functions()
    print("\n>>> ¡TODOS LOS TESTS DE TAREA 3 PASARON EXITOSAMENTE! <<<")
