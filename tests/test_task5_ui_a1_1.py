import os
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEW_A1_1_PATH = os.path.join(BASE_DIR, 'Codigo producido', 'View_A1_1.html')
JS_A1_PATH = os.path.join(BASE_DIR, 'Codigo producido', 'JS_A1.html')
CODIGO_GS_PATH = os.path.join(BASE_DIR, 'Codigo producido', 'Código.gs.txt')

class TestTask5UIA1_1(unittest.TestCase):
    def setUp(self):
        with open(VIEW_A1_1_PATH, 'r', encoding='utf-8') as f:
            self.view_a1_1 = f.read()
        with open(JS_A1_PATH, 'r', encoding='utf-8') as f:
            self.js_a1 = f.read()
        with open(CODIGO_GS_PATH, 'r', encoding='utf-8') as f:
            self.codigo_gs = f.read()

    def test_view_a1_1_applicant_section_has_all_official_fields(self):
        """Valida que la sección 1 (Información del Solicitante) incluya todos los campos oficiales."""
        fields = [
            'a1-1-sol-nombre', 'a1-1-sol-correo', 'a1-1-sol-cargo',
            'a1-1-sol-gerencia', 'a1-1-sol-centro-costo', 'a1-1-sol-agencia'
        ]
        for field in fields:
            self.assertIn(field, self.view_a1_1, f"View_A1_1 must include applicant field '{field}'")

    def test_view_a1_1_expense_details_and_banking_table(self):
        """Valida que la sección 2 incluya campos de viático, tabla bancaria, presupuesto, archivos y firmas."""
        fields = [
            'a1-1-viatico-duracion', 'a1-1-viatico-fecha-ini', 'a1-1-viatico-fecha-fin',
            'a1-1-viatico-tipo', 'a1-1-viatico-hora', 'a1-1-viatico-solicitud-tipo',
            'a1-1-banco-destinatario', 'a1-1-banco-monto', 'a1-1-banco-nombre',
            'a1-1-banco-tipo', 'a1-1-banco-numero', 'a1-1-badge-editado',
            'a1-1-viatico-motivo', 'a1-1-badge-presupuesto',
            'a1-1-justificacion-extra-container', 'a1-1-justificacion-extra',
            'a1-1-archivos-galeria', 'a1-1-firmas-container', 'a1-1-firmas-lista'
        ]
        for field in fields:
            self.assertIn(field, self.view_a1_1, f"View_A1_1 must include expense detail field '{field}'")

    def test_view_a1_1_decision_section_and_buttons(self):
        """Valida que la sección 3 incluya radios de decisión, comentario, errores y botón de confirmación."""
        fields = [
            'a1_1_decision', 'a1-1-comentario', 'a1-1-comentario-error',
            'a1-1-btn-guardar', 'a1-1-id-badge', 'a1-1-status-badge'
        ]
        for field in fields:
            self.assertIn(field, self.view_a1_1, f"View_A1_1 must include authorization action element '{field}'")

    def test_js_a1_populates_all_applicant_and_expense_fields(self):
        """Valida que JS_A1 contenga la lógica para poblar todos los campos del solicitante, viático y banco."""
        expected_mappings = [
            'a1-1-sol-nombre', 'a1-1-sol-correo', 'a1-1-sol-cargo',
            'a1-1-sol-gerencia', 'a1-1-sol-centro-costo', 'a1-1-sol-agencia',
            'a1-1-viatico-duracion', 'a1-1-viatico-fecha-ini', 'a1-1-viatico-fecha-fin',
            'a1-1-viatico-tipo', 'a1-1-banco-destinatario', 'a1-1-banco-monto',
            'a1-1-banco-nombre', 'a1-1-banco-tipo', 'a1-1-banco-numero',
            'a1-1-badge-editado', 'a1-1-viatico-motivo', 'a1-1-badge-presupuesto',
            'a1-1-justificacion-extra', 'a1-1-archivos-galeria', 'a1-1-firmas-container'
        ]
        for mapping in expected_mappings:
            self.assertIn(mapping, self.js_a1, f"JS_A1 must handle element '{mapping}' in poblarFormularioA1_1")

    def test_js_a1_resolution_functions_exist(self):
        """Valida que JS_A1 exponga y use las funciones de resolución y confirmación corporativa."""
        self.assertIn('function verDetalleAutorizacionA1_1', self.js_a1)
        self.assertIn('function poblarFormularioA1_1', self.js_a1)
        self.assertIn('function solicitarConfirmacionAutorizacionA1_1', self.js_a1)
        self.assertIn('function ejecutarResolucionA1_1', self.js_a1)
        self.assertIn('function toggleDecisionA1_1', self.js_a1)

    def test_backend_a1_1_functions_defined_and_resilient(self):
        """Valida que Código.gs.txt defina las funciones backend para A1.1 con nombres exactos."""
        self.assertIn('function obtenerDetalleAutorizacionA1_1', self.codigo_gs)
        self.assertIn('function procesarResolucionA1_1', self.codigo_gs)
        self.assertIn('function obtenerColMapTransaccional', self.codigo_gs)
        self.assertIn('function establecerColVal', self.codigo_gs)

if __name__ == '__main__':
    unittest.main()
