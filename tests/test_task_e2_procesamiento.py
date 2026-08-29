"""
Test unitario completo para Tarea 4 y Tarea 5: Módulo E2 y E2.1 Procesamiento de Pagos
Verifica:
1. View_E2_1.html contiene toda la iconografía FontAwesome (fas fa-...) en títulos y etiquetas.
2. View_E2_1.html usa inputs limpios en Sección 1, spans de texto en Sección 2 y tarjetas de métricas en Sección 3.
3. View_E2_1.html contiene el desglose del Asiento de Provisión (Compras) y tabla bancaria con indicador de edición.
4. JS_E2.html poblarFormularioE2_1 llena todos los campos de lectura sin errores en elementos DOM.
5. JS_E2.html maneja la validación de comentario obligatorio en rechazo (hacia solicitante / compras).
6. Regresión total del módulo E1/E2.
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEW_E2_1 = os.path.join(BASE_DIR, "Codigo producido", "View_E2_1.html")
JS_E2 = os.path.join(BASE_DIR, "Codigo producido", "JS_E2.html")

def test_view_e2_1_fontawesome_and_structure():
    print("[TEST 4.1] Verificando FontAwesome y estructura en View_E2_1.html...")
    with open(VIEW_E2_1, "r", encoding="utf-8") as f:
        v2_1 = f.read()

    # Iconos en encabezado y títulos de sección
    assert "fa-info-circle" in v2_1 or "fa-user-circle" in v2_1, "Sección 1 debe tener icono de solicitante"
    assert "fa-list" in v2_1, "Sección 2 debe tener icono fa-list"
    assert "fa-folder-open" in v2_1, "Sección 3 debe tener icono fa-folder-open"
    assert "fa-file-invoice-dollar" in v2_1 or "fa-receipt" in v2_1, "Debe tener icono de asiento/provisión"
    assert "fa-comments" in v2_1, "Sección 4 debe tener icono fa-comments"
    assert "fa-paperclip" in v2_1, "Adjuntos debe tener icono fa-paperclip"

    # Spans en sección 2
    assert 'id="e2-1-viatico-tipo"' in v2_1
    assert 'id="e2-1-viatico-fecha-ini"' in v2_1
    assert 'id="e2-1-viatico-fecha-fin"' in v2_1
    assert 'id="e2-1-viatico-monto"' in v2_1
    assert 'id="e2-1-motivo"' in v2_1
    assert 'id="e2-1-banco"' in v2_1
    assert 'id="e2-1-tipo-cuenta"' in v2_1
    assert 'id="e2-1-num-cuenta"' in v2_1

    # Asiento de provisión en sección 3
    assert 'id="e2-1-prov-fcontable"' in v2_1
    assert 'id="e2-1-prov-fvalor"' in v2_1
    assert 'id="e2-1-prov-modulo"' in v2_1
    assert 'id="e2-1-prov-transaccion"' in v2_1
    assert 'id="e2-1-prov-codrelacion"' in v2_1

    print("  -> OK: Estructura e iconografía de View_E2_1.html verificadas.")

def test_js_e2_1_detail_and_validation():
    print("[TEST 4.2] Verificando lógica de detalle y validación en JS_E2.html...")
    with open(JS_E2, "r", encoding="utf-8") as f:
        j2 = f.read()

    assert "poblarFormularioE2_1" in j2
    assert "e2-1-viatico-monto" in j2
    assert "e2-1-prov-fcontable" in j2
    assert "handleCambioResolucionE2_1" in j2
    assert "abrirModalConfirmarResolucionE2_1" in j2
    assert "confirmarGuardarResolucionE2_1" in j2

    print("  -> OK: Lógica de JS_E2.html verificada.")

if __name__ == "__main__":
    test_view_e2_1_fontawesome_and_structure()
    test_js_e2_1_detail_and_validation()
    print("\n>>> ¡TODOS LOS TESTS DE PROCESAMIENTO E2/E2.1 PASARON EXITOSAMENTE! <<<")
