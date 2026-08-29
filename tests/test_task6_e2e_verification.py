import os
import re
import unittest

class TestTask6E2EVerification(unittest.TestCase):
    def setUp(self):
        self.preview_path = 'Codigo producido/preview_local.html'
        self.code_dir = 'Codigo producido'
        
        with open(os.path.join(self.code_dir, 'Código.gs.txt'), 'r', encoding='utf-8') as f:
            self.gs_code = f.read()
        with open(os.path.join(self.code_dir, 'Index.html'), 'r', encoding='utf-8') as f:
            self.index_html = f.read()
        with open(os.path.join(self.code_dir, 'JS_Logic.html'), 'r', encoding='utf-8') as f:
            self.js_logic = f.read()
        with open(os.path.join(self.code_dir, 'JS_NuevaSolicitud.html'), 'r', encoding='utf-8') as f:
            self.js_s1 = f.read()
        with open(os.path.join(self.code_dir, 'JS_A1.html'), 'r', encoding='utf-8') as f:
            self.js_a1 = f.read()
        with open(os.path.join(self.code_dir, 'View_A1.html'), 'r', encoding='utf-8') as f:
            self.view_a1 = f.read()
        with open(os.path.join(self.code_dir, 'View_A1_1.html'), 'r', encoding='utf-8') as f:
            self.view_a1_1 = f.read()

    def test_bundle_preview_exists_and_is_not_empty(self):
        self.assertTrue(os.path.exists(self.preview_path), "preview_local.html must exist")
        self.assertGreater(os.path.getsize(self.preview_path), 500000, "preview_local.html size should be > 500KB")

    def test_no_unresolved_template_includes_in_bundle(self):
        with open(self.preview_path, 'r', encoding='utf-8') as f:
            bundle = f.read()
        self.assertNotIn('<?!= include(', bundle, "preview_local.html must not contain unparsed include tags")

    def test_s1_deduplication_and_atomic_lock(self):
        self.assertIn('S1_STATE.guardando', self.js_s1, "S1 must have guardando lock")
        self.assertIn('S1_STATE.archivos.some', self.js_s1, "S1 must deduplicate files by name/size")

    def test_backend_datos_autorizacion_and_resilient_drive(self):
        self.assertIn('var bitacoraInicial = [];', self.gs_code, "Applicant must not be saved as nivel 0 authorizer")
        self.assertIn('DriveApp.getRootFolder', self.gs_code, "Drive fallback must be present")

    def test_deep_linking_alias_and_navigation(self):
        self.assertIn('cargarDetalleAutorizacionA1_1', self.js_a1)
        self.assertIn('verDetalleAutorizacionA1_1', self.js_a1)
        self.assertIn("'a1_1': 'view-a1-1-detalle'", self.js_logic)

    def test_a1_and_a1_1_views_alignment(self):
        # A1 filters and headers
        for field in ['filter-a1-id', 'filter-a1-date', 'filter-a1-applicant', 'filter-a1-actor', 'filter-a1-classification']:
            self.assertIn(field, self.view_a1)
        for h in ['ID Solicitud', 'Fechas', 'Solicitante', 'Destinatarios', 'Montos', 'Estado Solicitud', 'Actor Actual', 'Clasificación Solicitud', 'Acciones']:
            self.assertIn(h, self.view_a1)
        
        # A1.1 official applicant section and fields
        for sol_field in ['a1-1-sol-nombre', 'a1-1-sol-correo', 'a1-1-sol-cargo', 'a1-1-sol-gerencia', 'a1-1-sol-centro-costo', 'a1-1-sol-agencia']:
            self.assertIn(sol_field, self.view_a1_1)
        self.assertIn('a1-1-banco-destinatario', self.view_a1_1)
        self.assertIn('a1-1-banco-monto', self.view_a1_1)
        self.assertIn('a1-1-archivos-galeria', self.view_a1_1)
        self.assertIn('a1-1-comentario', self.view_a1_1)
        self.assertIn('a1-1-btn-guardar', self.view_a1_1)

if __name__ == '__main__':
    unittest.main()
