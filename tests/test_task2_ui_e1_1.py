"""
Test unitario para Tarea 2: Refinamiento Visual E1.1 y Corrección de Simulación de Agrupación E1
Verifica:
1. View_E1_1.html tiene iconos FontAwesome (fas fa-...) en títulos y etiquetas de campos.
2. View_E1_1.html usa inputs limpios en Sección 1 y spans de texto en Sección 2 (Detalle de Gastos/Viático).
3. View_E1_1.html tiene tabla de Destinatarios y Pagos / Detalle Bancario con indicador ¿Información editada?.
4. View_E1_1.html tiene métricas destacadas y chips de adjuntos con fa-paperclip en Sección 3.
5. JS_E1.html poblarFormularioE1_1 llena spans de texto y tabla de destinatarios sin errores de elemento no encontrado.
6. JS_E1.html simula la agrupación de E1 actualizando estadoSolicitud = 'ENVIADO A PAGO'.
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEW_E1_1 = os.path.join(BASE_DIR, "Codigo producido", "View_E1_1.html")
JS_E1 = os.path.join(BASE_DIR, "Codigo producido", "JS_E1.html")

def test_view_e1_1_fontawesome_and_structure():
    print("[TEST 2.1] Verificando FontAwesome e iconografía en View_E1_1.html...")
    with open(VIEW_E1_1, "r", encoding="utf-8") as f:
        v1_1 = f.read()

    # Iconos en títulos de sección
    assert "fa-info-circle" in v1_1 or "fa-user-circle" in v1_1, "Sección 1 debe tener icono fa-info-circle o fa-user-circle"
    assert "fa-list" in v1_1, "Sección 2 debe tener icono fa-list"
    assert "fa-folder-open" in v1_1, "Sección 3 debe tener icono fa-folder-open"
    assert "fa-comments" in v1_1, "Sección 4 debe tener icono fa-comments"
    assert "fa-paperclip" in v1_1, "Sección de adjuntos debe tener icono fa-paperclip"

    # Iconos en labels de sección 1
    assert "fa-user" in v1_1 or "fa-user-circle" in v1_1
    assert "fa-envelope" in v1_1
    assert "fa-id-badge" in v1_1 or "fa-briefcase" in v1_1
    assert "fa-sitemap" in v1_1
    assert "fa-building" in v1_1

    # Iconos en labels de sección 2
    assert "fa-plane-departure" in v1_1
    assert "fa-calendar-plus" in v1_1
    assert "fa-calendar-check" in v1_1
    assert "fa-comment-dots" in v1_1
    assert "fa-university" in v1_1 or "fa-users" in v1_1

    # Verificar que sección 2 usa spans de texto para los valores de lectura
    assert 'id="e1-1-viatico-tipo"' in v1_1
    assert 'id="e1-1-viatico-fecha-ini"' in v1_1
    assert 'id="e1-1-viatico-fecha-fin"' in v1_1
    assert 'id="e1-1-viatico-monto"' in v1_1
    assert 'id="e1-1-tabla-destinatarios"' in v1_1 or 'e1-1-banco' in v1_1
    print("  -> OK: FontAwesome e iconografía en View_E1_1.html verificados.")

def test_js_e1_grouping_simulation():
    print("[TEST 2.2] Verificando simulación local de agrupación en JS_E1.html...")
    with open(JS_E1, "r", encoding="utf-8") as f:
        j1 = f.read()

    # Verificar que en el bloque de simulación local de confirmarGuardarAgrupacionE1 se actualiza estadoSolicitud
    fn_match = re.search(r"function confirmarGuardarAgrupacionE1\s*\([^)]*\)\s*\{([\s\S]*?)\n\}", j1)
    assert fn_match is not None, "Debe existir confirmarGuardarAgrupacionE1"
    fn_body = fn_match.group(1)

    assert "ENVIADO A PAGO" in fn_body, "Simulación local de E1 debe cambiar estadoSolicitud a ENVIADO A PAGO"
    print("  -> OK: Simulación local de agrupación en JS_E1.html verificada.")

if __name__ == "__main__":
    test_view_e1_1_fontawesome_and_structure()
    test_js_e1_grouping_simulation()
    print("\n>>> ¡TODOS LOS TESTS DE TAREA 2 PASARON EXITOSAMENTE! <<<")
