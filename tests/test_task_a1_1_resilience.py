import os
import re
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODIGO_GS = os.path.join(BASE_DIR, "Codigo producido", "Código.gs.txt")
JS_A1_FILE = os.path.join(BASE_DIR, "Codigo producido", "JS_A1.html")
VIEW_A1_1_FILE = os.path.join(BASE_DIR, "Codigo producido", "View_A1_1.html")

class TestA1_1Resilience(unittest.TestCase):
    def setUp(self):
        with open(CODIGO_GS, "r", encoding="utf-8") as f:
            self.gs_code = f.read()
        with open(JS_A1_FILE, "r", encoding="utf-8") as f:
            self.js_a1 = f.read()
        with open(VIEW_A1_1_FILE, "r", encoding="utf-8") as f:
            self.view_a1_1 = f.read()

    def test_single_definition_of_obtener_col_map_transaccional(self):
        matches = re.findall(r'function\s+obtenerColMapTransaccional\s*\(', self.gs_code)
        self.assertEqual(len(matches), 1, f"Expected 1 definition of obtenerColMapTransaccional, found {len(matches)}")

    def test_single_definition_of_guardar_archivos_en_drive(self):
        matches = re.findall(r'function\s+guardarArchivosEnDrive\s*\(', self.gs_code)
        self.assertEqual(len(matches), 1, f"Expected 1 definition of guardarArchivosEnDrive, found {len(matches)}")

    def test_canonical_57_columns_present_in_backend(self):
        self.assertIn("COLUMNAS_DIM_TRANSACCIONAL_CANONICAS", self.gs_code)
        self.assertIn("ID_Solicitud", self.gs_code)
        self.assertIn("AutorizacionesPendientes", self.gs_code)
        self.assertIn("ActorActual", self.gs_code)
        self.assertIn("DatosAutorizacion", self.gs_code)
        self.assertIn("JustificacionPresupuesto", self.gs_code)

    def test_obtener_col_val_and_establecer_col_val_exist(self):
        self.assertIn("function obtenerColVal", self.gs_code)
        self.assertIn("function establecerColVal", self.gs_code)
        self.assertIn("function obtenerIndiceColumna", self.gs_code)

    def test_obtener_detalle_a1_1_extracts_all_fields_with_robust_fallbacks(self):
        match = re.search(r'function\s+obtenerDetalleAutorizacionA1_1\s*\([^)]*\)\s*\{([\s\S]*?)\n\}', self.gs_code)
        self.assertIsNotNone(match, "obtenerDetalleAutorizacionA1_1 must be defined in Código.gs.txt")
        body = match.group(1)

        # Check robust parameter lookups
        self.assertIn("ID_DB_TRANSACCIONAL", body)
        # Check linear fallback search
        self.assertIn("filaEncontrada", body)
        # Check all extracted keys in detalle object
        required_keys = [
            "idSolicitud", "nombreSolicitante", "correoSolicitante", "cargoSolicitante",
            "gerencia", "centroCosto", "agencia", "duracionActividad", "fechaInicio",
            "fechaFin", "tipoViatico", "horaEvento", "tipoSolicitud", "destinatario",
            "correoDestinatario", "monto", "banco", "tipoCuenta", "numeroCuenta",
            "esEditado", "motivoViatico", "rubroContable", "clasificacionSolicitud",
            "dentroPresupuesto", "justificacionPresupuesto", "estadoSolicitud",
            "autorizacionesPendientes", "actorActual", "datosAutorizacion", "archivosAdjuntos"
        ]
        for key in required_keys:
            self.assertIn(key, body, f"obtenerDetalleAutorizacionA1_1 must extract key '{key}'")

    def test_procesar_resolucion_a1_1_handles_approval_and_rejection_safely(self):
        match = re.search(r'function\s+procesarResolucionA1_1\s*\([^)]*\)\s*\{([\s\S]*?)\n\}', self.gs_code)
        self.assertIsNotNone(match, "procesarResolucionA1_1 must be defined in Código.gs.txt")
        body = match.group(1)

        # Check rejection validation
        self.assertIn("comTrim.length < 5", body)
        # Check state transition
        self.assertIn("RECHAZO-AUTORIZACION", body)
        self.assertIn("AUTORIZADO", body)
        self.assertIn("Compras", body)
        # Check writing to sheet with safe helper
        self.assertIn("establecerColVal(sheetFact, filaEncontrada, colMap, \"EstadoSolicitud\"", body)
        self.assertIn("establecerColVal(sheetFact, filaEncontrada, colMap, \"AutorizacionesPendientes\"", body)
        self.assertIn("establecerColVal(sheetFact, filaEncontrada, colMap, \"ActorActual\"", body)
        self.assertIn("establecerColVal(sheetFact, filaEncontrada, colMap, \"DatosAutorizacion\"", body)
        self.assertIn("SpreadsheetApp.flush()", body)

    def test_frontend_poblar_formulario_a1_1_populates_all_ui_elements(self):
        # Must populate all UI elements in View_A1_1
        expected_ids = [
            'a1-1-sol-nombre', 'a1-1-sol-correo', 'a1-1-sol-cargo', 'a1-1-sol-gerencia',
            'a1-1-sol-centro-costo', 'a1-1-sol-agencia', 'a1-1-viatico-duracion',
            'a1-1-viatico-fecha-ini', 'a1-1-viatico-fecha-fin', 'a1-1-viatico-tipo',
            'a1-1-banco-destinatario', 'a1-1-banco-monto', 'a1-1-banco-nombre',
            'a1-1-banco-tipo', 'a1-1-banco-numero', 'a1-1-badge-editado',
            'a1-1-viatico-motivo', 'a1-1-badge-presupuesto', 'a1-1-justificacion-extra',
            'a1-1-archivos-galeria', 'a1-1-firmas-container'
        ]
        for el_id in expected_ids:
            self.assertIn(el_id, self.js_a1, f"JS_A1 must populate #{el_id}")

    def test_frontend_modal_confirmations_used(self):
        self.assertIn("mostrarModalConfirmacion", self.js_a1)
        self.assertIn("mostrarModalFeedback", self.js_a1)

if __name__ == '__main__':
    unittest.main()
