import os
import re
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODIGO_GS = os.path.join(BASE_DIR, "Codigo producido", "Código.gs.txt")
JS_NUEVA_SOL = os.path.join(BASE_DIR, "Codigo producido", "JS_NuevaSolicitud.html")

class TestS1ArchivosAdjuntos(unittest.TestCase):
    def setUp(self):
        with open(CODIGO_GS, "r", encoding="utf-8") as f:
            self.gs_code = f.read()
        with open(JS_NUEVA_SOL, "r", encoding="utf-8") as f:
            self.js_s1 = f.read()

    def test_single_definition_of_guardar_archivos_en_drive(self):
        # Must not have duplicate function declarations in Código.gs.txt
        matches = re.findall(r'function\s+guardarArchivosEnDrive\s*\(', self.gs_code)
        self.assertEqual(
            len(matches), 1,
            f"Expected exactly 1 definition of function guardarArchivosEnDrive in Código.gs.txt, found {len(matches)}"
        )

    def test_guardar_archivos_en_drive_supports_all_base64_and_property_keys(self):
        # Extract the function body of guardarArchivosEnDrive
        match = re.search(r'function\s+guardarArchivosEnDrive\s*\([^)]*\)\s*\{([\s\S]*?)\n\}', self.gs_code)
        self.assertIsNotNone(match, "guardarArchivosEnDrive must be defined in Código.gs.txt")
        body = match.group(1)

        # Must support contenidoBase64 (camelCase), ContenidoBase64 (PascalCase), dataUrl, and base64
        self.assertTrue(
            'contenidoBase64' in body and 'ContenidoBase64' in body,
            "guardarArchivosEnDrive must support both contenidoBase64 and ContenidoBase64"
        )
        self.assertTrue(
            'nombre' in body and 'NombreArchivo' in body,
            "guardarArchivosEnDrive must support both nombre and NombreArchivo"
        )
        self.assertTrue(
            'tipo' in body and 'TipoArchivo' in body,
            "guardarArchivosEnDrive must support both tipo and TipoArchivo"
        )

    def test_guardar_archivos_en_drive_drive_parameters_and_subfolder(self):
        match = re.search(r'function\s+guardarArchivosEnDrive\s*\([^)]*\)\s*\{([\s\S]*?)\n\}', self.gs_code)
        self.assertIsNotNone(match)
        body = match.group(1)

        # Check ID_CARPETA parameter lookups
        self.assertTrue(
            'ID_CARPETA_ADJUNTOS' in body or 'ID_CARPETA_COMPROBANTES' in body,
            "guardarArchivosEnDrive must look up Drive folder parameters"
        )
        # Check getRootFolder fallback
        self.assertIn('getRootFolder', body, "guardarArchivosEnDrive must provide getRootFolder fallback")
        # Check subfolder creation by idSolicitud/correlativo
        self.assertTrue(
            'Archivos - ' in body,
            "guardarArchivosEnDrive must create/use subfolder 'Archivos - [idSolicitud]'"
        )

    def test_guardar_nueva_solicitud_s1_saves_archivos_adjuntos(self):
        match = re.search(r'function\s+guardarNuevaSolicitudS1\s*\([^)]*\)\s*\{([\s\S]*?)\n\}', self.gs_code)
        self.assertIsNotNone(match, "guardarNuevaSolicitudS1 must be defined in Código.gs.txt")
        body = match.group(1)

        self.assertIn('guardarArchivosEnDrive', body)
        self.assertIn('"ArchivosAdjuntos"', body)

    def test_frontend_s1_includes_base64_payload(self):
        # Frontend must attach base64 content when files are read
        self.assertIn('contenidoBase64', self.js_s1)
        self.assertIn('renderizarGaleriaArchivosS1', self.js_s1)

if __name__ == '__main__':
    unittest.main()
