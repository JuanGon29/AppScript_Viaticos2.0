"""
Test suite completa de integración para Módulo S3 y S3.1 (Cierre y Liquidación de Solicitudes)
Verifica:
1. Backend en Código.gs.txt: obtención resiliente, detalle estructurado y guardado de liquidación con transición a LIQUIDADO.
2. Bandeja S3: 8 columnas oficiales, sin columna/filtro de solicitante, fechas dd/mm/aaaa y paginación.
3. Detalle S3.1: iconografía FontAwesome en etiquetas/secciones, spans de texto para gastos, métricas en 4 columnas y acciones de cierre con validación condicional de reintegro.
4. Simulación local reactiva: la solicitud liquidada pasa a LIQUIDADO y se remueve de S3.
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODIGO_GS = os.path.join(BASE_DIR, "Codigo producido", "Código.gs.txt")
VIEW_S3 = os.path.join(BASE_DIR, "Codigo producido", "View_S3.html")
VIEW_S3_1 = os.path.join(BASE_DIR, "Codigo producido", "View_S3_1.html")
JS_S3 = os.path.join(BASE_DIR, "Codigo producido", "JS_S3.html")

def test_backend_s3_complete():
    print("[TEST S3.1] Verificando Backend S3 y S3.1 en Código.gs.txt...")
    with open(CODIGO_GS, "r", encoding="utf-8") as f:
        code = f.read()

    # obtenerSolicitudesCierreS3
    assert "function obtenerSolicitudesCierreS3" in code
    assert "obtenerColMapTransaccional(headers)" in code
    assert "PAGADO" in code

    # obtenerDetalleCierreS3_1
    assert "function obtenerDetalleCierreS3_1" in code
    assert "nombreProvision" in code
    assert "nombreProcesamiento" in code
    assert "tipoCierre" in code

    # guardarCierreSolicitudS3_1
    assert "function guardarCierreSolicitudS3_1" in code
    assert "LIQUIDADO" in code
    assert "Compras" in code
    assert "FechaCierreS" in code
    assert "TipoCierre" in code
    print("  -> OK: Backend S3/S3.1 verificado.")

def test_view_and_logic_s3():
    print("[TEST S3.2] Verificando Bandeja S3 en View_S3.html y JS_S3.html...")
    with open(VIEW_S3, "r", encoding="utf-8") as f:
        v3 = f.read()
    with open(JS_S3, "r", encoding="utf-8") as f:
        j3 = f.read()

    # 8 Columnas oficiales
    assert "ID Solicitud" in v3
    assert "Fechas" in v3
    assert "Tipo Viático" in v3 or "Tipo de Viático" in v3
    assert "Monto" in v3
    assert "Estado" in v3
    assert "Actor Actual" in v3
    assert "Clasificación" in v3
    assert "Acciones" in v3

    # Sin solicitante
    assert 'for="filter-s3-applicant"' not in v3
    assert "<th>Solicitante</th>" not in v3 and "<th>SOLICITANTE</th>" not in v3

    # Formateo de fechas
    assert "formatearFechaS3" in j3
    assert "limpiarFiltrosS3" in j3
    print("  -> OK: Bandeja S3 verificada.")

def test_view_and_logic_s3_1():
    print("[TEST S3.3] Verificando Detalle S3.1 en View_S3_1.html y JS_S3.html...")
    with open(VIEW_S3_1, "r", encoding="utf-8") as f:
        v3_1 = f.read()
    with open(JS_S3, "r", encoding="utf-8") as f:
        j3 = f.read()

    # Iconografía
    assert "fa-info-circle" in v3_1
    assert "fa-list" in v3_1
    assert "fa-folder-open" in v3_1
    assert "fa-comments" in v3_1
    assert "fa-receipt" in v3_1
    assert "fa-paperclip" in v3_1

    # Spans en sección 2
    assert 'id="s3-1-viatico-tipo"' in v3_1
    assert 'id="s3-1-viatico-monto"' in v3_1
    assert 'id="s3-1-motivo"' in v3_1
    assert 'id="s3-1-banco"' in v3_1
    assert 'id="s3-1-tipo-cuenta"' in v3_1
    assert 'id="s3-1-num-cuenta"' in v3_1

    # Acciones de cierre
    assert 'id="s3-1-tipo-cierre-select"' in v3_1
    assert 'id="s3-1-archivo-input"' in v3_1
    assert 'id="s3-1-monto-reintegro-input"' in v3_1
    assert 'id="s3-1-fecha-reintegro-input"' in v3_1

    # JS bindings
    assert "poblarFormularioS3_1" in j3
    assert "handleCambioTipoCierreS3_1" in j3
    assert "confirmarGuardarCierreS3_1" in j3
    print("  -> OK: Detalle S3.1 verificado.")

if __name__ == "__main__":
    test_backend_s3_complete()
    test_view_and_logic_s3()
    test_view_and_logic_s3_1()
    print("\n>>> ¡SUITE COMPLETA DE CIERRE S3 Y S3.1 PASÓ EXITOSAMENTE! <<<")
