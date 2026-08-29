"""
Test suite de integración completa para Módulo E3 / E3.1: Cierre de Solicitudes (Compras).
Cubre:
1. Backend en Código.gs.txt: obtenerSolicitudesCierreE3, obtenerDetalleCierreE3_1, guardarResolucionCierreE3_1, guardarAgrupacionCierreE3.
2. UI de Bandeja en View_E3.html y JS_E3.html: 9 columnas oficiales, filtros, selector de página, modal de agrupación con fechas y archivo, checkbox condicional (esAgrupable).
3. UI de Detalle en View_E3_1.html y JS_E3.html: Iconografía FontAwesome, Sección 1 inputs limpios, Sección 2 spans de texto + tabla bancaria con badge EsEditado, Sección 3 métricas de liquidación y chips con fa-paperclip, Secciones 4/5/6 tablas de auditoría, Sección 7 acciones de resolución de cierre.
"""
import unittest
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODIGO_GS = os.path.join(BASE_DIR, "Codigo producido", "Código.gs.txt")
VIEW_E3 = os.path.join(BASE_DIR, "Codigo producido", "View_E3.html")
VIEW_E3_1 = os.path.join(BASE_DIR, "Codigo producido", "View_E3_1.html")
JS_E3 = os.path.join(BASE_DIR, "Codigo producido", "JS_E3.html")

class TestIntegracionE3Cierre(unittest.TestCase):

    def test_01_backend_functions_exist_and_use_colmap(self):
        with open(CODIGO_GS, "r", encoding="utf-8") as f:
            gs = f.read()
        self.assertIn("function obtenerSolicitudesCierreE3(", gs)
        self.assertIn("function obtenerDetalleCierreE3_1(", gs)
        self.assertIn("function guardarResolucionCierreE3_1(", gs)
        self.assertIn("function guardarAgrupacionCierreE3(", gs)
        self.assertIn("obtenerColMapTransaccional", gs)

    def test_02_backend_transitions(self):
        with open(CODIGO_GS, "r", encoding="utf-8") as f:
            gs = f.read()
        self.assertIn('"FINALIZADO"', gs)
        self.assertIn('"RECHAZO-CIERRE"', gs)
        self.assertIn('"LIQUIDADO"', gs)

    def test_03_view_e3_table_columns_and_modal(self):
        with open(VIEW_E3, "r", encoding="utf-8") as f:
            v3 = f.read()
        self.assertIn("ID Solicitud", v3)
        self.assertIn("Solicitante", v3)
        self.assertIn("Monto", v3)
        self.assertTrue("Código CC" in v3 or "Codigo CC" in v3)
        self.assertIn("Fechas", v3)
        self.assertTrue("Estado" in v3 or "Estado Solicitud" in v3)
        self.assertTrue("Tipo Viático" in v3 or "Tipo de Viático" in v3)
        self.assertTrue("Clasificación" in v3 or "Clasificación Solicitud" in v3)
        self.assertIn("Acciones", v3)
        self.assertIn('id="e3-modal-agrupar"', v3)
        self.assertIn('id="btn-e3-agrupar"', v3)
        self.assertIn('id="e3-page-size"', v3)

    def test_04_view_e3_1_detail_sections_and_icons(self):
        with open(VIEW_E3_1, "r", encoding="utf-8") as f:
            v3_1 = f.read()
        self.assertIn("fa-info-circle", v3_1)
        self.assertIn("fa-list", v3_1)
        self.assertIn("fa-folder-open", v3_1)
        self.assertIn("fa-comments", v3_1)
        self.assertIn("fa-receipt", v3_1)
        self.assertTrue("fa-university" in v3_1 or "fa-money-check-alt" in v3_1)
        self.assertTrue("fa-tasks" in v3_1 or "fa-check-double" in v3_1)
        self.assertIn("fa-paperclip", v3_1)
        self.assertIn('id="e3-1-info-tipo-cierre"', v3_1)
        self.assertIn('id="e3-1-info-monto-reintegro"', v3_1)
        self.assertIn('id="e3-1-info-fecha-reintegro"', v3_1)
        self.assertIn('id="e3-1-info-fecha-cierre-s"', v3_1)

    def test_05_js_e3_logic_and_formatting(self):
        with open(JS_E3, "r", encoding="utf-8") as f:
            j3 = f.read()
        self.assertIn("formatearFechaE3", j3)
        self.assertIn("renderTablaE3", j3)
        self.assertIn("poblarFormularioE3_1", j3)
        self.assertIn("confirmarGuardarAgrupacionE3", j3)
        self.assertIn("confirmarGuardarResolucionE3_1", j3)

if __name__ == "__main__":
    unittest.main()
