import os
import re
import unittest

class TestTask2BackendDatosAutorizacion(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Codigo producido', 'Código.gs.txt'), 'r', encoding='utf-8') as f:
            self.gs_code = f.read()

    def test_datos_autorizacion_not_initialized_with_nivel_0_applicant(self):
        # bitacoraInicial in guardarNuevaSolicitudS1 should be an empty list [] and not contain nivel: 0 for applicant
        match = re.search(r'var\s+bitacoraInicial\s*=\s*\[\s*\{\s*nivel\s*:\s*0[^\]]*\}\s*\];', self.gs_code)
        self.assertIsNone(
            match,
            "guardarNuevaSolicitudS1 must NOT assign nivel: 0 to applicant in DatosAutorizacion. Nivel 0 is strictly for Jefe Regional."
        )

    def test_datos_autorizacion_initialized_empty_array(self):
        # bitacoraInicial should be []
        self.assertTrue(
            'var bitacoraInicial = [];' in self.gs_code or 'var bitacoraInicial = JSON.stringify([]);' in self.gs_code,
            "bitacoraInicial in guardarNuevaSolicitudS1 must be initialized as an empty array []."
        )

    def test_guardar_archivos_en_drive_fallback_resilience(self):
        # guardarArchivosEnDrive should have robust fallback if getFolderById fails
        self.assertIn('guardarArchivosEnDrive', self.gs_code)
        # Should have getRootFolder fallback or multi-try error handling
        self.assertIn('getRootFolder', self.gs_code, "guardarArchivosEnDrive must provide a fallback to getRootFolder() or safe metadata handling.")

    def test_dimtransaccional_column_mapping(self):
        # Verify registroValores contains essential column keys matching the 57 column dictionary
        expected_cols = [
            "ID_Solicitud", "EstadoSolicitud", "AutorizacionesPendientes", "ActorActual",
            "FechaSolicitud", "FechaModificacion", "NombreSolicitante", "CorreoSolicitante",
            "CargoSolicitante", "Gerencia", "CentroCosto", "Agencia", "DuracionActividad",
            "FechaInicio", "FechaFin", "TipoViatico", "HoraEvento", "TipoSolicitud",
            "Destinatario", "CorreoDestinatario", "Monto", "Banco", "TipoCuenta",
            "NumeroCuenta", "MotivoViatico", "RubroContable", "ClasificacionSolicitud",
            "ArchivosAdjuntos", "CorreoJefeRegional", "CorreoAutorizador1",
            "CorreoAutorizador2", "CorreoAutorizador3", "DentroPresupuesto", "DatosAutorizacion"
        ]
        for col in expected_cols:
            self.assertIn(f'"{col}"', self.gs_code, f"registroValores must contain mapped column {col}")

if __name__ == '__main__':
    unittest.main()
