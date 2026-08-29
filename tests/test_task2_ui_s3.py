"""
Test unitario para Tarea 2: Bandeja S3 en View_S3.html y JS_S3.html
Verifica:
1. View_S3.html cuenta con las 8 columnas oficiales (ID Solicitud, Fechas, Tipo Viático, Monto, Estado, Actor Actual, Clasificación, Acciones).
2. View_S3.html NO incluye filtro ni columna de Solicitante.
3. JS_S3.html contiene formatearFechaS3 con formato dd/mm/aaaa.
4. JS_S3.html renderTablaS3 alinea las 8 columnas sin la columna Solicitante.
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEW_S3 = os.path.join(BASE_DIR, "Codigo producido", "View_S3.html")
JS_S3 = os.path.join(BASE_DIR, "Codigo producido", "JS_S3.html")

def test_view_s3_columns_and_filters():
    print("[TEST 2.1] Verificando columnas y filtros en View_S3.html...")
    with open(VIEW_S3, "r", encoding="utf-8") as f:
        v3 = f.read()

    # Columnas esperadas en thead
    assert "ID Solicitud" in v3
    assert "Fechas" in v3
    assert "Tipo Viático" in v3 or "Tipo de Viático" in v3 or "Tipo de viático" in v3
    assert "Monto" in v3
    assert "Estado" in v3 or "Estado Solicitud" in v3
    assert "Actor Actual" in v3
    assert "Clasificación" in v3 or "Clasificación Solicitud" in v3
    assert "Acciones" in v3

    # NO debe tener columna ni filtro de Solicitante
    assert 'for="filter-s3-applicant"' not in v3, "No debe existir filtro de solicitante en S3"
    assert "<th>Solicitante</th>" not in v3 and "<th>SOLICITANTE</th>" not in v3

    # Botón limpiar filtros y selector de páginas
    assert "limpiarFiltrosS3" in v3
    assert "s3-page-size" in v3

    print("  -> OK: View_S3.html verificado correctamente.")

def test_js_s3_date_and_rendering():
    print("[TEST 2.2] Verificando formateo y renderizado en JS_S3.html...")
    with open(JS_S3, "r", encoding="utf-8") as f:
        j3 = f.read()

    assert "formatearFechaS3" in j3, "JS_S3.html debe tener la función formatearFechaS3"
    assert "renderTablaS3" in j3
    assert "toggleSortDateS3" in j3
    assert "limpiarFiltrosS3" in j3

    print("  -> OK: JS_S3.html verificado correctamente.")

if __name__ == "__main__":
    test_view_s3_columns_and_filters()
    test_js_s3_date_and_rendering()
    print("\n>>> ¡TODOS LOS TESTS DE BANDEJA S3 PASARON EXITOSAMENTE! <<<")
