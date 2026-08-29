import os
import re
import unittest

class TestTask1S1Dedup(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Codigo producido', 'View_NuevaSolicitud.html'), 'r', encoding='utf-8') as f:
            self.view_s1 = f.read()
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Codigo producido', 'JS_NuevaSolicitud.html'), 'r', encoding='utf-8') as f:
            self.js_s1 = f.read()

    def test_no_inline_onclick_on_file_container(self):
        # The container should not have inline onclick opening the file input directly
        match = re.search(r'id=["\']s1_fileContainer["\'][^>]*onclick=["\'][^"\']*s1_fileInput', self.view_s1)
        self.assertIsNone(match, "Found dangerous inline onclick on s1_fileContainer that causes duplicate drop+click events.")

    def test_idempotent_event_listener_registration(self):
        # S1_STATE or configurarEventosS1 should have a flag to prevent multiple registrations
        self.assertIn('eventosConfigurados', self.js_s1, "JS_NuevaSolicitud must include 'eventosConfigurados' guard to prevent duplicate listeners.")

    def test_file_deduplication_in_processing(self):
        # procesarArchivosSeleccionados should check for existing file with same name and size
        self.assertTrue(
            'S1_STATE.archivos.some' in self.js_s1 or 'yaExiste' in self.js_s1 or 'existe' in self.js_s1,
            "procesarArchivosSeleccionados must verify if file already exists in S1_STATE.archivos."
        )

    def test_atomic_submission_lock(self):
        # ejecutarGuardadoSolicitudS1 must have submission locking flag
        self.assertTrue(
            'S1_STATE.guardando' in self.js_s1 or 'S1_STATE.isSubmitting' in self.js_s1,
            "ejecutarGuardadoSolicitudS1 must have an atomic lock (e.g. S1_STATE.guardando) to prevent double submissions."
        )

if __name__ == '__main__':
    unittest.main()
