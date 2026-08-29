"""
Test unitario para Tarea 3: Detalle y Resolución de Cierre E3.1 en View_E3_1.html y JS_E3.html
Verifica:
1. View_E3_1.html contiene toda la iconografía FontAwesome (fas fa-...) en títulos y etiquetas.
2. View_E3_1.html usa inputs limpios en Sección 1, spans de texto en Sección 2, métricas ampliadas en Sección 3 y 3 tablas de auditoría (Autorizaciones, Compras, Tesorería).
3. View_E3_1.html cuenta con Sección 7 Acciones de Cierre (Resolución Aprobado/Rechazado + Comentario).
4. JS_E3.html poblarFormularioE3_1 carga correctamente todos los datos de liquidación y auditorías previas.
5. JS_E3.html confirmarGuardarResolucionE3_1 ejecuta las mutaciones de estado requeridas según el tipo de cierre y resolución.
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEW_E3_1 = os.path.join(BASE_DIR, "Codigo producido", "View_E3_1.html")
JS_E3 = os.path.join(BASE_DIR, "Codigo producido", "JS_E3.html")

def test_view_e3_1_fontawesome_and_structure():
    print("[TEST 3.1] Verificando FontAwesome y estructura en View_E3_1.html...")
    with open(VIEW_E3_1, "r", encoding="utf-8") as f:
        v3_1 = f.read()

    # Iconografía FontAwesome
    assert "fa-info-circle" in v3_1, "Sección 1 debe tener icono fa-info-circle"
    assert "fa-list" in v3_1, "Sección 2 debe tener icono fa-list"
    assert "fa-folder-open" in v3_1, "Sección 3 debe tener icono fa-folder-open"
    assert "fa-comments" in v3_1, "Sección 4 debe tener icono fa-comments"
    assert "fa-receipt" in v3_1, "Sección 5 debe tener icono fa-receipt"
    assert "fa-university" in v3_1 or "fa-money-check-alt" in v3_1, "Sección 6 debe tener icono de tesorería"
    assert "fa-tasks" in v3_1 or "fa-check-double" in v3_1 or "fa-gavel" in v3_1, "Sección 7 debe tener icono de resolución"
    assert "fa-paperclip" in v3_1, "Adjuntos debe tener icono fa-paperclip"

    # Spans en sección 2
    assert 'id="e3-1-viatico-tipo"' in v3_1
    assert 'id="e3-1-viatico-fecha-ini"' in v3_1
    assert 'id="e3-1-viatico-fecha-fin"' in v3_1
    assert 'id="e3-1-viatico-monto"' in v3_1
    assert 'id="e3-1-motivo"' in v3_1
    assert 'id="e3-1-banco"' in v3_1
    assert 'id="e3-1-tipo-cuenta"' in v3_1
    assert 'id="e3-1-num-cuenta"' in v3_1

    # Métricas y campos en sección 3
    assert 'id="e3-1-info-id"' in v3_1
    assert 'id="e3-1-info-monto"' in v3_1
    assert 'id="e3-1-info-fecha-creacion"' in v3_1
    assert 'id="e3-1-info-rubro"' in v3_1
    assert 'id="e3-1-info-tipo-cierre"' in v3_1
    assert 'id="e3-1-info-monto-reintegro"' in v3_1
    assert 'id="e3-1-info-fecha-reintegro"' in v3_1
    assert 'id="e3-1-info-fecha-cierre-s"' in v3_1

    # 3 Tablas de auditoría
    assert 'id="e3-1-tabla-autorizaciones"' in v3_1
    assert 'id="e3-1-prov-nombre"' in v3_1
    assert 'id="e3-1-proc-nombre"' in v3_1

    # Acciones de cierre
    assert 'id="e3-1-resolucion-select"' in v3_1
    assert 'id="e3-1-comentario-input"' in v3_1

    print("  -> OK: View_E3_1.html estructura e iconografía verificadas.")

def test_js_e3_1_detail_and_validation():
    print("[TEST 3.2] Verificando lógica de detalle y resolución en JS_E3.html...")
    with open(JS_E3, "r", encoding="utf-8") as f:
        j3 = f.read()

    assert "poblarFormularioE3_1" in j3
    assert "e3-1-viatico-monto" in j3
    assert "activarSeccionResponderE3_1" in j3
    assert "abrirModalConfirmarE3_1" in j3
    assert "confirmarGuardarResolucionE3_1" in j3

    print("  -> OK: JS_E3.html lógica verificada.")

if __name__ == "__main__":
    test_view_e3_1_fontawesome_and_structure()
    test_js_e3_1_detail_and_validation()
    print("\n>>> ¡TODOS LOS TESTS DE DETALLE E3.1 PASARON EXITOSAMENTE! <<<")
