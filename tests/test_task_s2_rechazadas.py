import os
#!/usr/bin/env python3
"""
test_task_s2_rechazadas.py
Unit tests for S2 (Bandeja Solicitudes Rechazadas) and S2.1 (Multi-Resolución de Rechazo)
and validation of DatosAutorizacion integrity rules.
"""

import unittest
import re
import json

class TestS2RechazadasBackendAndRules(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Codigo producido', 'Código.gs.txt'), "r", encoding="utf-8") as f:
            cls.code_gs = f.read()
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Codigo producido', 'View_S2.html'), "r", encoding="utf-8") as f:
            cls.view_s2 = f.read()
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Codigo producido', 'JS_S2.html'), "r", encoding="utf-8") as f:
            cls.js_s2 = f.read()
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Codigo producido', 'View_S2_1.html'), "r", encoding="utf-8") as f:
            cls.view_s2_1 = f.read()

    def test_datos_autorizacion_integrity_and_no_solicitante(self):
        """Validar que DatosAutorizacion inicie como array vacío y no agregue al solicitante en ningún punto."""
        # 1. En creación inicial de S1
        self.assertIn('var bitacoraInicial = [];', self.code_gs)
        self.assertNotIn('"resolucion": "CREADO"', self.code_gs)
        self.assertNotIn('"comentario": "Creación de solicitud', self.code_gs)
        
        # 2. En S2.1 RECHAZO-PRESUPUESTO no debe meter al solicitante como nivel 0 en DatosAutorizacion
        # La justificación se guarda en JustificacionPresupuesto
        s2_1_section = self.code_gs[self.code_gs.find('CASO 1: RECHAZO-PRESUPUESTO'):self.code_gs.find('CASO 2: RECHAZO-PROVISION 1')]
        self.assertNotIn('bitacora.push({', s2_1_section, "RECHAZO-PRESUPUESTO no debe agregar entradas del solicitante a DatosAutorizacion")
        self.assertIn('JustificacionPresupuesto', s2_1_section)

    def test_s2_obtener_solicitudes_rechazadas_logic(self):
        """Verifica que obtenerSolicitudesRechazadas use colMap dinámico y filtre por correo y los 5 estados."""
        self.assertIn('function obtenerSolicitudesRechazadas(correoUsuario)', self.code_gs)
        self.assertIn('RECHAZO-PRESUPUESTO', self.code_gs)
        self.assertIn('RECHAZO-PROVISION 1', self.code_gs)
        self.assertIn('RECHAZO-PROVISION 2', self.code_gs)
        self.assertIn('RECHAZO-PAGO 1', self.code_gs)
        self.assertIn('RECHAZO-CIERRE', self.code_gs)
        self.assertIn('correoFiltro', self.code_gs)

    def test_s2_1_resolver_rechazo_all_5_cases(self):
        """Verifica que resolverRechazoS2_1 cubra los 5 estados de rechazo conforme a la Fuente de Verdad."""
        self.assertIn('function resolverRechazoS2_1(', self.code_gs)
        
        # Caso 1: RECHAZO-PRESUPUESTO -> Guarda JustificacionPresupuesto, rutas extraordinarias
        self.assertIn('CASO 1: RECHAZO-PRESUPUESTO', self.code_gs)
        self.assertIn('calcularRutaAutorizante(', self.code_gs)
        
        # Caso 2: RECHAZO-PROVISION 1 -> Reinicia DatosAutorizacion = [], revalida saldo
        self.assertIn('CASO 2: RECHAZO-PROVISION 1', self.code_gs)
        self.assertIn('JSON.stringify([])', self.code_gs)
        self.assertIn('validarYAfectarPresupuesto(', self.code_gs)
        
        # Caso 3: RECHAZO-PROVISION 2 -> AUTORIZADO, Compras, notifica a compras
        self.assertIn('CASO 3: RECHAZO-PROVISION 2', self.code_gs)
        
        # Caso 4: RECHAZO-PAGO 1 -> Limpia provisión previa, pasa a AUTORIZADO / Compras
        self.assertIn('CASO 4: RECHAZO-PAGO 1', self.code_gs)
        self.assertIn('ResolucionProvision', self.code_gs)
        self.assertIn('ComentarioProvision', self.code_gs)
        self.assertIn('FechaProvision', self.code_gs)
        self.assertIn('NombreProvision', self.code_gs)
        self.assertIn('AgrupableProvision', self.code_gs)
        
        # Caso 5: RECHAZO-CIERRE -> Guarda liquidación, LIQUIDADO / Compras
        self.assertIn('CASO 5: RECHAZO-CIERRE', self.code_gs)
        self.assertIn('TipoCierre', self.code_gs)
        self.assertIn('MontoReintegro', self.code_gs)
        self.assertIn('FechaReintegro', self.code_gs)
        self.assertIn('FechaCierreS', self.code_gs)

    def test_s2_tray_8_columns_and_no_solicitante_column(self):
        """Verifica que la tabla de S2 tenga exactamente las 8 columnas oficiales y NO tenga columna Solicitante."""
        headers = re.findall(r'<th[^>]*>(.*?)</th>', self.view_s2, re.DOTALL)
        clean_headers = [re.sub(r'<[^>]+>', '', h).strip() for h in headers]
        
        # No debe haber columna 'Solicitante'
        self.assertFalse(any('SOLICITANTE' in h.upper() for h in clean_headers), "La columna 'Solicitante' no debe existir en S2")
        
        # Debe contener las 8 columnas
        self.assertTrue(any('ID SOLICITUD' in h.upper() for h in clean_headers))
        self.assertTrue(any('FECHAS' in h.upper() for h in clean_headers))
        self.assertTrue(any('TIPO DE VI' in h.upper() for h in clean_headers))
        self.assertTrue(any('MONTO' in h.upper() for h in clean_headers))
        self.assertTrue(any('ESTADO SOLICITUD' in h.upper() for h in clean_headers))
        self.assertTrue(any('ACTOR ACTUAL' in h.upper() for h in clean_headers))
        self.assertTrue(any('CLASIFICACI' in h.upper() for h in clean_headers))
        self.assertTrue(any('ACCIONES' in h.upper() for h in clean_headers))
        self.assertEqual(len(clean_headers), 8, f"Se esperaban 8 columnas pero se encontraron {len(clean_headers)}: {clean_headers}")

    def test_s2_filters_and_pagination(self):
        """Verifica que existan los 5 filtros reactivos, botón limpiar filtros y selector de páginas."""
        self.assertIn('filter-s2-id', self.view_s2)
        self.assertIn('filter-s2-date', self.view_s2)
        self.assertIn('filter-s2-status', self.view_s2)
        self.assertIn('filter-s2-type', self.view_s2)
        self.assertIn('filter-s2-classification', self.view_s2)
        self.assertIn('limpiarFiltrosS2', self.view_s2)
        self.assertIn('s2-page-size', self.view_s2)
        
        # En JS_S2.html
        self.assertIn('function filtrarTablaS2()', self.js_s2)
        self.assertIn('function limpiarFiltrosS2()', self.js_s2)
        self.assertIn('function cambiarPageSizeS2(', self.js_s2)

    def test_s2_1_sections_and_visual_elements(self):
        """Verifica que View_S2_1.html contenga las secciones adaptativas y elementos visuales de acuerdo a la Fuente de Verdad."""
        # Sección 1: Solicitante #E2E8F0
        self.assertIn('s2-1-sol-nombre', self.view_s2_1)
        self.assertIn('s2-1-sol-correo', self.view_s2_1)
        self.assertIn('s2-1-sol-cargo', self.view_s2_1)
        self.assertIn('s2-1-sol-gerencia', self.view_s2_1)
        self.assertIn('s2-1-sol-cc', self.view_s2_1)
        self.assertIn('s2-1-sol-agencia', self.view_s2_1)
        self.assertIn('#E2E8F0', self.view_s2_1)
        
        # Sección 2A: Detalle Viático Readonly
        self.assertIn('s2-1-viatico-readonly-container', self.view_s2_1)
        self.assertIn('s2-1-banco', self.view_s2_1)
        self.assertIn('s2-1-archivos-lista', self.view_s2_1)
        
        # Sección 2B: Detalle Viático Editable
        self.assertIn('s2-1-viatico-editable-container', self.view_s2_1)
        self.assertIn('s2-1-edit-monto', self.view_s2_1)
        self.assertIn('s2-1-edit-motivo', self.view_s2_1)
        self.assertIn('s2-1-edit-dropzone', self.view_s2_1)
        self.assertIn('s2-1-btn-editar-banco', self.view_s2_1)
        
        # Sección 3: Tablas Informativas de Retroalimentación
        self.assertIn('s2-1-info-provision', self.view_s2_1)
        self.assertIn('s2-1-provision-nombre', self.view_s2_1)
        self.assertIn('s2-1-provision-comentario', self.view_s2_1)
        
        self.assertIn('s2-1-info-procesamiento', self.view_s2_1)
        self.assertIn('s2-1-procesamiento-nombre', self.view_s2_1)
        self.assertIn('s2-1-procesamiento-comentario', self.view_s2_1)
        
        self.assertIn('s2-1-info-cierre', self.view_s2_1)
        self.assertIn('s2-1-cierre-nombre', self.view_s2_1)
        self.assertIn('s2-1-cierre-comentario', self.view_s2_1)
        
        # Sección 4A: Justificación
        self.assertIn('s2-1-justificacion-container', self.view_s2_1)
        self.assertIn('s2-1-justificacion-input', self.view_s2_1)
        
        # Sección 4B: Acciones de Cierre
        self.assertIn('s2-1-acciones-cierre', self.view_s2_1)
        self.assertIn('s2-1-cierre-tipo', self.view_s2_1)
        self.assertIn('s2-1-cierre-monto-reintegro', self.view_s2_1)
        self.assertIn('s2-1-cierre-fecha-reintegro', self.view_s2_1)
        self.assertIn('s2-1-cierre-dropzone', self.view_s2_1)
        
        # Modales
        self.assertIn('s2-1-modal-confirmar', self.view_s2_1)
        self.assertIn('s2-1-modal-edicion-banco', self.view_s2_1)

    def test_s2_1_js_handlers(self):
        """Verifica que JS_S2.html contenga todos los controladores necesarios para S2.1."""
        self.assertIn('function verDetalleRechazadaS2(', self.js_s2)
        self.assertIn('function poblarFormularioS2_1(', self.js_s2)
        self.assertIn('function ejecutarResolucionS2_1()', self.js_s2)
        self.assertIn('function confirmarResolucionFinalS2_1()', self.js_s2)
        self.assertIn('function abrirModalEdicionBancoS2_1()', self.js_s2)
        self.assertIn('function proseguirEdicionBancoS2_1()', self.js_s2)
        self.assertIn('function configurarDropzoneS2_1(', self.js_s2)
        self.assertIn('function validarJustificacionS2_1(', self.js_s2)
        self.assertIn('function toggleCamposReintegroS2_1(', self.js_s2)

if __name__ == '__main__':
    unittest.main()
