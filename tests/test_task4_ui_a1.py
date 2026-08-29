import os
import unittest

class TestTask4UIA1(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Codigo producido', 'View_A1.html'), 'r', encoding='utf-8') as f:
            self.view_a1 = f.read()
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Codigo producido', 'JS_A1.html'), 'r', encoding='utf-8') as f:
            self.js_a1 = f.read()

    def test_view_a1_filters_match_reference_design(self):
        # Must have the 5 filter inputs from reference design
        self.assertIn('filter-a1-id', self.view_a1, "View_A1 must include filter-a1-id input")
        self.assertIn('filter-a1-date', self.view_a1, "View_A1 must include filter-a1-date input")
        self.assertIn('filter-a1-applicant', self.view_a1, "View_A1 must include filter-a1-applicant input")
        self.assertIn('filter-a1-actor', self.view_a1, "View_A1 must include filter-a1-actor input")
        self.assertIn('filter-a1-classification', self.view_a1, "View_A1 must include filter-a1-classification select")

    def test_view_a1_table_headers_match_reference_design(self):
        # Must have all 9 columns
        headers = [
            'ID Solicitud', 'Fechas', 'Solicitante', 'Destinatarios',
            'Montos', 'Estado Solicitud', 'Actor Actual', 'Clasificación Solicitud', 'Acciones'
        ]
        for h in headers:
            self.assertIn(h, self.view_a1, f"View_A1 table must include column header '{h}'")

    def test_js_a1_filtering_logic_supports_all_filters(self):
        # JS_A1 must parse all filter values
        self.assertIn("document.getElementById('filter-a1-id')", self.js_a1)
        self.assertIn("document.getElementById('filter-a1-date')", self.js_a1)
        self.assertIn("document.getElementById('filter-a1-applicant')", self.js_a1)
        self.assertIn("document.getElementById('filter-a1-actor')", self.js_a1)
        self.assertIn("document.getElementById('filter-a1-classification')", self.js_a1)

    def test_js_a1_row_rendering_matches_reference_design(self):
        # Ver detalles button and column rendering
        self.assertIn('Ver', self.js_a1)
        self.assertIn('detalles', self.js_a1)
        self.assertIn('verDetalleAutorizacionA1_1', self.js_a1)

if __name__ == '__main__':
    unittest.main()
