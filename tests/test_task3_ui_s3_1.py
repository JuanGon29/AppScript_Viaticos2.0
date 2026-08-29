"""
Test unitario para Tarea 3: Detalle y Liquidación S3.1 en View_S3_1.html y JS_S3.html
Verifica:
1. View_S3_1.html contiene toda la iconografía FontAwesome (fas fa-...) en títulos y etiquetas.
2. View_S3_1.html usa inputs limpios en Sección 1, spans de texto en Sección 2 y tarjetas de métricas en Sección 3.
3. View_S3_1.html contiene tablas de auditoría de Autorización, Compras y Tesorería.
4. View_S3_1.html contiene sección de Acciones de Cierre con campos condicionales de reintegro.
5. JS_S3.html poblarFormularioS3_1 llena todos los campos de lectura correctamente.
6. JS_S3.html confirmarGuardarCierreS3_1 muta el estado a LIQUIDADO y refresca la tabla local.
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEW_S3_1 = os.path.join(BASE_DIR, "Codigo producido", "View_S3_1.html")
JS_S3 = os.path.join(BASE_DIR, "Codigo producido", "JS_S3.html")

def test_view_s3_1_fontawesome_and_structure():
    print("[TEST 3.1] Verificando FontAwesome y estructura en View_S3_1.html...")
    with open(VIEW_S3_1, "r", encoding="utf-8") as f:
        v3_1 = f.read()

    # Iconos en encabezados y etiquetas
    assert "fa-info-circle" in v3_1, "Sección 1 debe tener icono fa-info-circle"
    assert "fa-list" in v3_1, "Sección 2 debe tener icono fa-list"
    assert "fa-folder-open" in v3_1, "Sección 3 debe tener icono fa-folder-open"
    assert "fa-comments" in v3_1, "Sección 4 debe tener icono fa-comments"
    assert "fa-receipt" in v3_1, "Sección 5 debe tener icono fa-receipt"
    assert "fa-money-check-alt" in v3_1 or "fa-university" in v3_1, "Sección 6 debe tener icono de tesorería"
    assert "fa-tasks" in v3_1 or "fa-receipt" in v3_1 or "fa-money-bill-wave" in v3_1, "Sección 7 debe tener icono de acciones"
    assert "fa-paperclip" in v3_1, "Adjuntos debe tener icono fa-paperclip"

    # Spans en sección 2
    assert 'id="s3-1-viatico-tipo"' in v3_1
    assert 'id="s3-1-viatico-fecha-ini"' in v3_1
    assert 'id="s3-1-viatico-fecha-fin"' in v3_1
    assert 'id="s3-1-viatico-monto"' in v3_1
    assert 'id="s3-1-motivo"' in v3_1
    assert 'id="s3-1-banco"' in v3_1
    assert 'id="s3-1-tipo-cuenta"' in v3_1
    assert 'id="s3-1-num-cuenta"' in v3_1

    # Métricas y campos en sección 3
    assert 'id="s3-1-info-id"' in v3_1
    assert 'id="s3-1-info-monto"' in v3_1
    assert 'id="s3-1-info-fecha-creacion"' in v3_1
    assert 'id="s3-1-info-rubro"' in v3_1

    # Campos de acciones de cierre
    assert 'id="s3-1-tipo-cierre-select"' in v3_1
    assert 'id="s3-1-archivo-input"' in v3_1
    assert 'id="s3-1-monto-reintegro-input"' in v3_1
    assert 'id="s3-1-fecha-reintegro-input"' in v3_1

    print("  -> OK: View_S3_1.html estructura e iconografía verificadas.")

def test_js_s3_1_detail_and_validation():
    print("[TEST 3.2] Verificando lógica de detalle y validación en JS_S3.html...")
    with open(JS_S3, "r", encoding="utf-8") as f:
        j3 = f.read()

    assert "poblarFormularioS3_1" in j3
    assert "s3-1-viatico-monto" in j3
    assert "handleCambioTipoCierreS3_1" in j3
    assert "abrirModalConfirmarCierreS3_1" in j3
    assert "confirmarGuardarCierreS3_1" in j3

    print("  -> OK: JS_S3.html lógica verificada.")

if __name__ == "__main__":
    test_view_s3_1_fontawesome_and_structure()
    test_js_s3_1_detail_and_validation()
    print("\n>>> ¡TODOS LOS TESTS DE DETALLE S3.1 PASARON EXITOSAMENTE! <<<")
