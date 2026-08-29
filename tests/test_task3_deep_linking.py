import os
import re
import unittest

class TestTask3DeepLinking(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Codigo producido', 'Código.gs.txt'), 'r', encoding='utf-8') as f:
            self.gs_code = f.read()
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Codigo producido', 'JS_Logic.html'), 'r', encoding='utf-8') as f:
            self.js_logic = f.read()
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Codigo producido', 'JS_A1.html'), 'r', encoding='utf-8') as f:
            self.js_a1 = f.read()

    def test_email_card_contains_revisar_solicitud_button_with_a1_1_link(self):
        # Email card link must point to view=a1_1&id=...
        self.assertIn('view=a1_1&id=', self.gs_code, "generarHtmlCardEmail must include 'view=a1_1&id=' in review link.")
        self.assertIn('Revisar Solicitud', self.gs_code, "generarHtmlCardEmail must include button 'Revisar Solicitud'.")

    def test_js_a1_exposes_both_ver_and_cargar_detalle_a1_1(self):
        # Both function names must be available
        self.assertIn('function verDetalleAutorizacionA1_1', self.js_a1)
        self.assertTrue(
            'cargarDetalleAutorizacionA1_1' in self.js_a1,
            "JS_A1.html must define or alias cargarDetalleAutorizacionA1_1 for compatibility with JS_Logic router."
        )

    def test_js_logic_deep_link_navigation_calls_a1_1_loader(self):
        # JS_Logic must map a1_1 to view-a1-1-detalle and invoke the loader function
        self.assertIn("'a1_1': 'view-a1-1-detalle'", self.js_logic)
        self.assertTrue(
            'verDetalleAutorizacionA1_1' in self.js_logic or 'cargarDetalleAutorizacionA1_1' in self.js_logic,
            "ejecutarNavegacionDeepLink must trigger A1.1 detail loading function."
        )

if __name__ == '__main__':
    unittest.main()
