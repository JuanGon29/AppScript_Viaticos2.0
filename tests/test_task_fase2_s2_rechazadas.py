import unittest
import os
import re
import json

class TestFase2S2Rechazadas(unittest.TestCase):
    """
    Test Suite Exhaustiva para la Fase 2: Módulo de Solicitudes Rechazadas (S2 y S2.1)
    Verifica los contratos estipulados en Observaciones y Comentarios.pdf y la Fuente de Verdad.
    """

    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.codigo_path = os.path.join(cls.base_dir, "Codigo producido", "Código.gs.txt")
        cls.view_s2_path = os.path.join(cls.base_dir, "Codigo producido", "View_S2.html")
        cls.view_s2_1_path = os.path.join(cls.base_dir, "Codigo producido", "View_S2_1.html")
        cls.js_s2_path = os.path.join(cls.base_dir, "Codigo producido", "JS_S2.html")

        with open(cls.codigo_path, "r", encoding="utf-8") as f:
            cls.codigo_content = f.read()
        with open(cls.view_s2_path, "r", encoding="utf-8") as f:
            cls.view_s2_content = f.read()
        with open(cls.view_s2_1_path, "r", encoding="utf-8") as f:
            cls.view_s2_1_content = f.read()
        with open(cls.js_s2_path, "r", encoding="utf-8") as f:
            cls.js_s2_content = f.read()

    # =========================================================================
    # 1. PRUEBAS DEL BACKEND (Código.gs.txt)
    # =========================================================================

    def test_backend_obtener_solicitudes_rechazadas_defined(self):
        """Verifica que obtenerSolicitudesRechazadas esté definida y maneje los 5 estados de rechazo."""
        self.assertIn("function obtenerSolicitudesRechazadas", self.codigo_content)
        # Debe filtrar los 5 estados de rechazo
        estados_esperados = [
            "RECHAZO-PRESUPUESTO",
            "RECHAZO-PROVISION 1",
            "RECHAZO-PROVISION 2",
            "RECHAZO-PAGO 1",
            "RECHAZO-CIERRE"
        ]
        for est in estados_esperados:
            self.assertIn(est, self.codigo_content, f"El estado {est} debe ser manejado en el backend")

    def test_backend_obtener_detalle_solicitud_rechazada_defined(self):
        """Verifica que obtenerDetalleSolicitudRechazada esté implementada con búsqueda por mapeo dinámico."""
        self.assertIn("function obtenerDetalleSolicitudRechazada", self.codigo_content)
        self.assertIn("obtenerColVal", self.codigo_content)
        # Debe recuperar comentarios de provision, procesamiento y cierre
        self.assertIn("ComentarioProvision", self.codigo_content)
        self.assertIn("ComentarioProcesamiento", self.codigo_content)
        self.assertIn("ComentarioCierreE", self.codigo_content)

    def test_backend_resolver_rechazo_s2_1_cases(self):
        """Verifica que resolverRechazoS2_1 cubra los 5 casos funcionales requeridos."""
        self.assertIn("function resolverRechazoS2_1", self.codigo_content)
        
        # Caso 1: RECHAZO-PRESUPUESTO -> INICIADO (Fuera de Presupuesto)
        self.assertIn("CASO 1: RECHAZO-PRESUPUESTO", self.codigo_content)
        self.assertIn("JustificacionPresupuesto", self.codigo_content)
        
        # Caso 2: RECHAZO-PROVISION 1 -> Reinicio de bitácora y revalidación de fondos
        self.assertIn("CASO 2: RECHAZO-PROVISION 1", self.codigo_content)
        self.assertIn("validarYAfectarPresupuesto", self.codigo_content)
        
        # Caso 3: RECHAZO-PROVISION 2 -> AUTORIZADO a Compras
        self.assertIn("CASO 3: RECHAZO-PROVISION 2", self.codigo_content)
        
        # Caso 4: RECHAZO-PAGO 1 -> Limpieza de las 5 columnas de provisión
        self.assertIn("CASO 4: RECHAZO-PAGO 1", self.codigo_content)
        self.assertIn('establecerColVal(sheetFact, filaEncontrada, colMap, "ResolucionProvision", "", 37)', self.codigo_content)
        self.assertIn('establecerColVal(sheetFact, filaEncontrada, colMap, "ComentarioProvision", "", 38)', self.codigo_content)
        self.assertIn('establecerColVal(sheetFact, filaEncontrada, colMap, "FechaProvision", "", 39)', self.codigo_content)
        self.assertIn('establecerColVal(sheetFact, filaEncontrada, colMap, "NombreProvision", "", 40)', self.codigo_content)
        self.assertIn('establecerColVal(sheetFact, filaEncontrada, colMap, "AgrupableProvision", "", 41)', self.codigo_content)

        # Caso 5: RECHAZO-CIERRE -> Reenvío de liquidación hacia Compras
        self.assertIn("CASO 5: RECHAZO-CIERRE", self.codigo_content)
        self.assertIn("TipoCierre", self.codigo_content)
        self.assertIn("MontoReintegro", self.codigo_content)
        self.assertIn("FechaReintegro", self.codigo_content)
        self.assertIn("FechaCierreS", self.codigo_content)

    def test_backend_flush_consistency(self):
        """Verifica que SpreadsheetApp.flush() se ejecute para persistencia inmediata."""
        self.assertIn("SpreadsheetApp.flush()", self.codigo_content)

    # =========================================================================
    # 2. PRUEBAS DEL FRONTEND BANDEJA S2 (View_S2.html)
    # =========================================================================

    def test_view_s2_columns(self):
        """Verifica las 8 columnas requeridas en S2 y la ausencia de columna solicitante."""
        columnas_esperadas = [
            "ID Solicitud",
            "Fechas",
            "Tipo de Viático",
            "Monto",
            "Estado Solicitud",
            "Actor Actual",
            "Clasificación",
            "Acciones"
        ]
        for col in columnas_esperadas:
            self.assertIn(col, self.view_s2_content, f"La columna '{col}' debe estar en View_S2.html")

        # No debe tener columna 'Solicitante' en el thead de S2
        self.assertNotIn("<th class=\"py-3 px-4 font-label-md text-label-md text-on-primary uppercase font-bold text-center align-middle\">Solicitante</th>", self.view_s2_content)

    def test_view_s2_dom_elements(self):
        """Verifica que existan los IDs clave de filtros, tabla y paginación en View_S2.html."""
        ids_requeridos = [
            "filter-s2-id",
            "filter-s2-date",
            "filter-s2-status",
            "filter-s2-type",
            "filter-s2-classification",
            "tabla-s2-body",
            "s2-no-results-row",
            "s2-solicitudes-count",
            "s2-page-size",
            "s2-pagination-controls"
        ]
        for el_id in ids_requeridos:
            self.assertIn(f'id="{el_id}"', self.view_s2_content, f"Elemento #{el_id} debe existir en View_S2.html")

    # =========================================================================
    # 3. PRUEBAS DEL FRONTEND VISTA ADAPTATIVA S2.1 (View_S2_1.html)
    # =========================================================================

    def test_view_s2_1_applicant_section(self):
        """Verifica la sección de Información del Solicitante con fondo #E2E8F0 y modo solo lectura."""
        self.assertIn("#E2E8F0", self.view_s2_1_content)
        self.assertIn("Información del Solicitante", self.view_s2_1_content)
        
        campos_solicitante = [
            "s2-1-sol-nombre",
            "s2-1-sol-correo",
            "s2-1-sol-cargo",
            "s2-1-sol-gerencia",
            "s2-1-sol-cc",
            "s2-1-sol-agencia"
        ]
        for c_id in campos_solicitante:
            self.assertIn(f'id="{c_id}"', self.view_s2_1_content, f"Campo #{c_id} debe estar en Información del Solicitante")

    def test_view_s2_1_dynamic_sections(self):
        """Verifica la existencia de los contenedores para los 5 comportamientos de rechazo."""
        contenedores = [
            "s2-1-viatico-readonly-container",
            "s2-1-viatico-editable-container",
            "s2-1-info-provision",
            "s2-1-info-procesamiento",
            "s2-1-info-cierre",
            "s2-1-justificacion-container",
            "s2-1-acciones-cierre"
        ]
        for cont_id in contenedores:
            self.assertIn(f'id="{cont_id}"', self.view_s2_1_content, f"Contenedor #{cont_id} debe existir en View_S2_1.html")

    def test_view_s2_1_corporate_modals(self):
        """Verifica los modales corporativos de confirmación de resolución y de edición bancaria."""
        self.assertIn('id="s2-1-modal-confirmar"', self.view_s2_1_content)
        self.assertIn('id="s2-1-modal-edicion-banco"', self.view_s2_1_content)
        self.assertIn("Confirmación de Edición Bancaria", self.view_s2_1_content)

    # =========================================================================
    # 4. PRUEBAS DEL CONTROLADOR JS_S2 (JS_S2.html)
    # =========================================================================

    def test_js_s2_date_formatting(self):
        """Verifica que formatearFechaS2 devuelva dd/mm/aaaa de forma consistente."""
        self.assertIn("function formatearFechaS2", self.js_s2_content)
        self.assertIn("formatearFechaS2(sol.fechaSolicitud)", self.js_s2_content)

    def test_js_s2_e1_styling_alignment(self):
        """Verifica que renderTablaS2 aplique la estética de E1: iconos de fecha y botón [Ver detalles]."""
        self.assertIn("calendar_today", self.js_s2_content)
        self.assertIn("visibility", self.js_s2_content)
        self.assertIn("Ver detalles", self.js_s2_content)
        self.assertIn("bg-secondary-container hover:bg-secondary text-on-secondary", self.js_s2_content)

    def test_js_s2_no_native_alerts_in_business_logic(self):
        """Verifica que se use window.mostrarModalFeedback en lugar de alerts bloqueantes."""
        self.assertIn("window.mostrarModalFeedback", self.js_s2_content)

    def test_js_s2_return_navigation_on_success(self):
        """Verifica que al confirmar exitosamente la resolución, se redirija a la bandeja S2."""
        self.assertIn("navegarSubmenu('view-solicitudes-rechazadas')", self.js_s2_content)
        self.assertIn("cargarSolicitudesRechazadas()", self.js_s2_content)

    def test_js_s2_poblar_formulario_all_5_states(self):
        """Verifica que poblarFormularioS2_1 cubra explícitamente los 5 estados de rechazo."""
        self.assertIn("RECHAZO-PRESUPUESTO", self.js_s2_content)
        self.assertIn("RECHAZO-PROVISION 1", self.js_s2_content)
        self.assertIn("RECHAZO-PROVISION 2", self.js_s2_content)
        self.assertIn("RECHAZO-PAGO 1", self.js_s2_content)
        self.assertIn("RECHAZO-CIERRE", self.js_s2_content)


if __name__ == "__main__":
    unittest.main()
