# Guía Maestra de Despliegue y Configuración en Google Apps Script
## Sistema de Gestión de Viáticos 2.0 — Banco Integral

Esta guía detalla paso a paso el procedimiento técnico para trasladar el código fuente producido a un entorno de producción en **Google Apps Script**, configurar las bases de datos en **Google Sheets**, configurar las carpetas de **Google Drive**, habilitar el sistema de notificaciones por **Correo Electrónico (Gmail)** con enlace directo deep-link, configurar el **trigger diario de 15 días** para cancelaciones automáticas y parametrizar los roles de usuario.

---

## 1. Arquitectura y Componentes del Sistema

El sistema opera bajo una arquitectura de **Single Page Application (SPA)** modular alojada en Google Apps Script, respaldada por hojas de cálculo como base de datos relacional/dimensional y Google Drive como repositorio de archivos:

```
                  ┌─────────────────────────────────────────────────────────┐
                  │            Google Workspace / Apps Script               │
                  │  ┌───────────────────────────────────────────────────┐  │
                  │  │            Index.html (SPA Contenedor)            │  │
                  │  │  - CSS_Styles.html (Tailwind CSS Material 3)      │  │
                  │  │  - JS_Logic.html (Enrutador, Auth & Deep Links)   │  │
                  │  │  - 17 Sub-vistas (S1, S2, S2.1, E1, E2, S3, E3,   │  │
                  │  │    A1, A1.1, A2, EnCurso, Historico, etc.)        │  │
                  │  │  - 10 Controladores Modulares JavaScript          │  │
                  │  └─────────────────────────┬─────────────────────────┘  │
                  │                            │ (google.script.run)        │
                  │  ┌─────────────────────────▼─────────────────────────┐  │
                  │  │           Código.gs (Servidor Backend)            │  │
                  │  │  - 9 Módulos Funcionales                          │  │
                  │  │  - Trigger Diario de 15 Días                      │  │
                  │  └───────────────┬─────────┬─────────┬───────────────┘  │
                  └──────────────────┼─────────┼─────────┼──────────────────┘
                                     │         │         │
                ┌────────────────────▼┐   ┌────▼────┐   ┌▼───────────────────┐
                │ Parametros_Viaticos │   │ Gmail / │   │   Google Drive     │
                │ - DB_Maestro_Global │   │ Single  │   │ (Carpeta Adjuntos) │
                │ - BaseDatos (Trans) │   │ CTA Card│   └────────────────────┘
                │ - Presupuesto       │   └─────────┘
                └─────────────────────┘
```

---

## 2. Paso 1: Configuración de Hojas de Cálculo (Google Sheets)

Antes de desplegar el código, asegúrate de que existan los siguientes 4 archivos en Google Drive:

### 2.1. Hoja Maestra de Parámetros: `Parametros_Viaticos2.0`
Crea una hoja de cálculo llamada `Parametros_Viaticos2.0` con una pestaña llamada **`Parametros`**:

| Clave | Valor | Descripción |
| :--- | :--- | :--- |
| `ID_DB_MAESTRO` | `[ID_DE_TU_HOJA_DB_MAESTRO]` | ID de la hoja `1 - DB_Maestro_Global` |
| `ID_DB_TRANSACCIONES` | `[ID_DE_TU_HOJA_BASEDATOS]` | ID de la hoja `BaseDatos_Viaticos2.0` |
| `ID_DB_PRESUPUESTO` | `[ID_DE_TU_HOJA_PRESUPUESTO]` | ID de la hoja `Presupuesto_Viaticos2.0` |
| `ID_CARPETA_COMPROBANTES` | `[ID_DE_TU_CARPETA_DRIVE]` | ID de la carpeta en Google Drive para archivos |
| `URL_WEB_APP` | `[URL_DESPLIEGUE_APPS_SCRIPT]` | URL de la Web App obtenida tras el despliegue |

> [!IMPORTANT]
> El ID de este archivo (`Parametros_Viaticos2.0`) es el **único ID quemado** en el código fuente (variable `ID_DB_PARAMETROS` en la línea 14 de `Código.gs`).

---

### 2.2. Hoja de Catálogos Globales: `1 - DB_Maestro_Global`
Debe contener las siguientes pestañas con sus columnas exactas (respetar mayúsculas y minúsculas):

1. **`DimUsuarios`**:
   - Columnas obligatorias: `NombreUsuario`, `CorreoUsuario`, `Plaza`, `NombreGerencia`, `NombreArea`, `NombreRegion`, `CentroCosto`, `NombreBanco`, `TipoCuenta`, `NumeroCuenta`, `EsMovil`, `AccesoViaticos`, `RolUsuario_Viaticos`.
   - **Valores para `RolUsuario_Viaticos`**: `SOLICITANTE`, `EDITOR-COMPRAS`, `EDITOR-TESORERIA`, `AUTORIZADOR`, `ADMINISTRADOR`.
   - **Valores para `AccesoViaticos`**: `SI` o `NO`.
   - **Valores para `EsMovil`**: `Si` (habilita la opción "Viático Movilidad") o `No`.

2. **`DimGerencias`**:
   - Columnas: `NombreGerencia`, `NombreGerente`, `CorreoGerente`.
   - *Nota*: Debe existir una fila donde `NombreGerencia = "GERENCIA DE FINANZAS"` y otra con `NombreGerencia = "DIRECCION EJECUTIVA"`.

3. **`DimRegiones`**:
   - Columnas: `NombreRegion`, `NombreJefeRegional`, `CorreoJefeRegional`.

4. **`DimAgencias`**:
   - Columnas: `NombreAgencia`, `NombreRegion`, `TipoUbicacion`.

5. **`DimAreas`**:
   - Columnas: `NombreArea`, `NombreGerencia`.

---

### 2.3. Hoja de Transacciones: `BaseDatos_Viaticos2.0`
Debe contener una pestaña llamada **`DimTransaccional`** con las 54 columnas oficiales en la primera fila:

```text
A: ID_Solicitud
B: NombreSolicitante
C: CorreoSolicitante
D: CargoSolicitante
E: Gerencia
F: CentroCosto
G: Agencia
H: DuracionActividad
I: FechaInicio
J: FechaFin
K: TipoViatico
L: HoraEvento
M: TipoSolicitud
N: Destinatario
O: CorreoDestinatario
P: MontoTotal
Q: InstitucionBancaria
R: TipoCuentaBancaria
S: NumeroCuentaBancaria
T: MotivoViatico
U: RubroContable
V: ClasificacionSolicitud
W: EsEditado
X: EstadoSolicitud
Y: ActorActual
Z: FechaSolicitud
AA: FechaModificacion
AB: ArchivosAdjuntos
AC: DatosAutorizacion
AD: JustificacionPresupuesto
AE: AutorizacionesPendientes
AF: CorreoAutorizador0
AG: CorreoAutorizador1
AH: CorreoAutorizador2
AI: CorreoAutorizador3
AJ: ResolucionProvision
AK: ComentarioProvision
AL: FechaProvision
AM: NombreProvision
AN: AgrupableProvision
AO: ResolucionProcesamiento
AP: ComentarioProcesamiento
AQ: FechaProcesamiento
AR: NombreProcesamiento
AS: AgrupableProcesamiento
AT: TipoCierre
AU: MontoReintegro
AV: FechaReintegro
AW: FechaCierreS
AX: ResolucionCierreE
AY: ComentarioCierreE
AZ: FechaCierreE
BA: NombreCierreE
BB: AgrupableCierreE
```

---

### 2.4. Hoja de Presupuestos: `Presupuesto_Viaticos2.0`
Debe contener las siguientes pestañas con sus columnas correspondientes:

1. **`DimPresupuesto`**: Presupuestos aprobados anuales asignados por `CentroCosto` y columnas mensuales: `Enero`, `Febrero`, `Marzo`, `Abril`, `Mayo`, `Junio`, `Julio`, `Agosto`, `Septiembre`, `Octubre`, `Noviembre`, `Diciembre`.
2. **`DimConsumo`**: Registro acumulado de fondos reservados o consumidos por cada `CentroCosto` y mes.
3. **`DimDisponible`**: Saldo disponible en tiempo real calculado como $\text{Disponible} = \text{Presupuesto} - \text{Consumo}$.

---

## 3. Paso 2: Creación de Carpeta en Google Drive

1. Ve a **Google Drive** institucional.
2. Crea una carpeta llamada `Comprobantes_Viaticos_2.0`.
3. Haz clic derecho sobre la carpeta >> **Compartir**.
4. Configura el acceso general para que cualquier usuario de la organización con el enlace pueda **Ver/Editar** (o añade permisos de edición al grupo de colaboradores que gestionarán viáticos).
5. Copia el **ID de la carpeta** (la cadena alfanumérica al final de la URL en la barra de direcciones).
6. Pega este ID en la fila `ID_CARPETA_COMPROBANTES` de la hoja `Parametros_Viaticos2.0`.

---

## 4. Paso 3: Creación y Carga de Archivos en Google Apps Script

### 4.1. Crear el Proyecto
1. Ingresa a [script.google.com](https://script.google.com/).
2. Haz clic en **Nuevo proyecto**.
3. Renombra el proyecto a: `Portal_Viaticos_2.0_BancoIntegral`.

### 4.2. Configurar el Manifiesto (`appsscript.json`)
1. En el menú lateral izquierdo, haz clic en **Configuración del proyecto** (icono de engranaje ⚙️).
2. Marca la casilla **"Mostrar el archivo de manifiesto 'appsscript.json' en el editor"**.
3. Regresa al **Editor** (icono de código `< >`).
4. Abre el archivo `appsscript.json` y reemplaza su contenido por:

```json
{
  "timeZone": "America/El_Salvador",
  "dependencies": {
    "enabledAdvancedServices": []
  },
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "webapp": {
    "executeAs": "USER_DEPLOYING",
    "access": "ANYONE"
  },
  "oauthScopes": [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/script.send_mail",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/script.external_request",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
  ]
}
```

---

### 4.3. Cargar el Archivo de Servidor (`Código.gs`)
1. Abre el archivo `Código.gs` predeterminado.
2. Copia todo el contenido del archivo local [Código.gs.txt](file:///d:/Roberto/Documents/Antigravity%20D/Viaticos/V3_MVP/Codigo%20producido/Código.gs.txt).
3. Pégalo en `Código.gs`.
4. Verifica que en la **línea 14** la variable `ID_DB_PARAMETROS` tenga el ID de tu hoja `Parametros_Viaticos2.0`:
   ```javascript
   var ID_DB_PARAMETROS = "TU_ID_DE_PARAMETROS_AQUI";
   ```

---

### 4.4. Crear los Archivos HTML del Frontend
En el editor de Google Apps Script, haz clic en el botón **`+`** >> **HTML** y crea los siguientes **29 archivos** con sus nombres exactos, pegando el código respectivo de la carpeta `Codigo producido`:

| Tipo | Nombre del Archivo en Apps Script | Archivo de Origen | Propósito |
| :--- | :--- | :--- | :--- |
| **Shell** | `Index` | `Index.html` | Contenedor base de la SPA |
| **Estilos** | `CSS_Styles` | `CSS_Styles.html` | Tailwind CSS y tokens de diseño Material 3 |
| **Vistas** | `View_Login` | `View_Login.html` | Pantalla de inicio de sesión y autenticación |
| | `View_Home` | `View_Home.html` | Layout principal (Sidebar con 5 roles, TopAppBar, Dashboard) |
| | `View_NuevaSolicitud` | `View_NuevaSolicitud.html` | Formulario de creación de viáticos S1 con modal de bloqueo de 15 días |
| | `View_Resolucion` | `View_Resolucion.html` | Vista web de resolución rápida para autorizadores |
| | `View_S2` | `View_S2.html` | Bandeja de solicitudes rechazadas (S2) |
| | `View_S2_1` | `View_S2_1.html` | Formulario de resolución de los 5 estados de rechazo (S2.1) |
| | `View_E1` | `View_E1.html` | Bandeja de provisión de pagos en Compras (E1) |
| | `View_E1_1` | `View_E1_1.html` | Detalle de provisión con badge ¿Información editada? (E1.1) |
| | `View_E2` | `View_E2.html` | Bandeja de procesamiento de pagos en Tesorería (E2) |
| | `View_E2_1` | `View_E2_1.html` | Detalle de desembolso con badge ¿Información editada? (E2.1) |
| | `View_S3` | `View_S3.html` | Bandeja de cierre de solicitudes - Solicitante (S3) |
| | `View_S3_1` | `View_S3_1.html` | Formulario de liquidación, facturas y reintegro (S3.1) |
| | `View_E3` | `View_E3.html` | Bandeja de cierre de solicitudes en Compras (E3) |
| | `View_E3_1` | `View_E3_1.html` | Detalle y dictamen de cierre en Compras con badge editado (E3.1) |
| | `View_A1` | `View_A1.html` | Bandeja de solicitudes pendientes de autorización (A1) |
| | `View_A1_1` | `View_A1_1.html` | Detalle confidencial y resolución de autorización (A1.1) |
| | `View_A2` | `View_A2.html` | Catálogo interactivo de las 16 rutas autorizantes (A2) |
| | `View_EnCurso` | `View_EnCurso.html` | Visor de solicitudes activas y expediente acumulativo progresivo |
| | `View_Historico` | `View_Historico.html` | Archivo histórico inmutable de solicitudes concluidas con impresión |
| **JS** | `JS_Logic` | `JS_Logic.html` | Controlador principal de sesión, 5 roles, enrutador y deep links |
| | `JS_NuevaSolicitud` | `JS_NuevaSolicitud.html` | Controlador S1 con validación reactiva de 15 días |
| | `JS_S2` | `JS_S2.html` | Controlador S2/S2.1 para los 5 estados de rechazo |
| | `JS_E1` | `JS_E1.html` | Controlador E1/E1.1 de provisión y asientos con append seguro |
| | `JS_E2` | `JS_E2.html` | Controlador E2/E2.1 de procesamiento de pagos y desembolso |
| | `JS_S3` | `JS_S3.html` | Controlador S3/S3.1 de liquidación de comprobantes y reintegro |
| | `JS_E3` | `JS_E3.html` | Controlador E3/E3.1 de cierre y dictamen contable |
| | `JS_A1` | `JS_A1.html` | Controlador A1/A1.1 de autorizaciones y escalamiento |
| | `JS_EnCurso` | `JS_EnCurso.html` | Controlador de solicitudes en curso y visor progresivo |
| | `JS_Historico` | `JS_Historico.html` | Controlador del repositorio histórico y generación de impresión |

> [!TIP]
> Al crear archivos HTML en Google Apps Script, omite la extensión `.html` en el cuadro de diálogo (Apps Script la añade automáticamente).

---

## 5. Paso 4: Despliegue de la Aplicación Web (Web App)

1. En la esquina superior derecha del editor de Apps Script, haz clic en **Implementar** (Deploy) >> **Nueva implementación** (New deployment).
2. Haz clic en el icono de engranaje ⚙️ junto a *Seleccionar tipo* y elige **Aplicación web** (Web app).
3. Configura los parámetros de implementación:
   - **Descripción**: `Versión 2.0 - Producción Viáticos`.
   - **Ejecutar como**: **Usuario que accede a la aplicación web** (`USER_ACCESSING`) o **Yo (tu cuenta)** (`USER_DEPLOYING`).
     > **Recomendación**: Usa `USER_DEPLOYING` para que las escrituras en Google Sheets y subidas a Drive se ejecuten con una cuenta de servicio / administrador con permisos completos sin depender de que cada usuario tenga permisos individuales sobre los Sheets maestros.
   - **Quién tiene acceso**: **Cualquier usuario de Banco Integral** (o *Cualquier usuario* según la política de tu dominio).
4. Haz clic en **Implementar**.
5. Se solicitará otorgar permisos OAuth:
   - Haz clic en **Revisar permisos**.
   - Selecciona tu cuenta corporativa.
   - Haz clic en **Configuración avanzada** >> **Ir a Portal_Viaticos_2.0 (no seguro)**.
   - Haz clic en **Permitir**.
6. Copia la **URL de la aplicación web** generada (termina en `/exec`).
7. **Pega esta URL** en la fila `URL_WEB_APP` de tu hoja `Parametros_Viaticos2.0`.

---

## 6. Paso 5: Configuración del Activador Diario (Trigger 15 Días)

Para que el sistema cancele automáticamente las solicitudes rechazadas pre-pago que permanezcan inactivas durante 15 días o más y reintegre los fondos a `DimDisponible`, se debe programar un activador basado en tiempo:

1. En el menú lateral izquierdo de Apps Script, haz clic en **Activadores** (icono de reloj ⏰).
2. Haz clic en el botón azul **Añadir activador** (esquina inferior derecha).
3. Configura los siguientes parámetros exactos:
   - **Elige qué función quieres ejecutar**: `verificarVencimientoSolicitudesRechazadas`
   - **Elige qué implementación debe ejecutarse**: `Principal` (Head) o la versión desplegada activa.
   - **Selecciona la fuente del evento**: `Según el tiempo` (Time-driven).
   - **Selecciona el tipo de activador basado en el tiempo**: `Temporizador por días` (Day timer).
   - **Selecciona la hora del día**: `De medianoche a 1:00 a.m.` (Medianoche).
   - **Ajustes de notificación de errores**: `Notificarme inmediatamente`.
4. Haz clic en **Guardar**.

---

## 7. Paso 6: Sistema de Notificaciones por Correo (Gmail) y Deep Linking

El sistema envía notificaciones interactivas por correo electrónico cuando una solicitud requiere autorización corporativa:

### 7.1. Plantilla Gmail con Botón Único (Single CTA)
- **Remitente**: Los correos se emiten con el alias institucional `Notificaciones_Viaticos2.0`.
- **Plantilla HTML Responsive**: Contiene una tarjeta visual con:
  - Encabezado institucional con ID de solicitud (`SOL-XXXX-XXXX`).
  - Resumen ejecutivo: Solicitante, Cargo, Gerencia, Centro de Costo, Monto, Tipo de Viático y Motivo.
  - Indicador de presupuesto y estado del flujo.
  - **Botón Único**: **`[ Revisar Solicitud ]`** con enlace seguro deep-link.

### 7.2. Enrutamiento Deep-Link a A1.1
El enlace del botón apunta a:
`[URL_WEB_APP]?view=a1_1&id=SOL-XXXX-XXXX`

Al hacer clic:
1. Si el usuario ya cuenta con sesión activa, el enrutador [JS_Logic.html](file:///d:/Roberto/Documents/Antigravity%20D/Viaticos/V3_MVP/Codigo%20producido/JS_Logic.html) navega directamente a [View_A1_1.html](file:///d:/Roberto/Documents/Antigravity%20D/Viaticos/V3_MVP/Codigo%20producido/View_A1_1.html) y carga la solicitud mediante `cargarDetalleAutorizacionA1_1(id)`.
2. Si el usuario aún no inicia sesión, `JS_Logic.html` almacena el parámetro pendiente (`_pendingDeepLink`) y redirige automáticamente a la pantalla de resolución una vez completada la autenticación.
3. La pantalla A1.1 garantiza la **confidencialidad de datos bancarios** (ocultos para autorizadores) y permite autorizar o rechazar registrando el motivo obligatorio.

---

## 8. Paso 7: Configuración de Roles y Permisos en `DimUsuarios`

Para que los usuarios vean las secciones correspondientes en el Sidebar, configúralos en la columna `RolUsuario_Viaticos` de `DimUsuarios`:

| Rol en `RolUsuario_Viaticos` | Acceso a Módulos |
| :--- | :--- |
| **`SOLICITANTE`** | Menú *Solicitantes* (*Nueva Solicitud*, *Solicitudes Rechazadas*, *Cierre de solicitudes*), *Solicitudes en curso*, *Histórico*. |
| **`EDITOR-COMPRAS`** | Menú *Operaciones* (*Provisión de pagos [E1]*, *Cierre de solicitudes [E3]*), *Solicitudes en curso*, *Histórico*. |
| **`EDITOR-TESORERIA`** | Menú *Operaciones* (*Procesamiento de pagos [E2]*), *Solicitudes en curso*, *Histórico*. |
| **`AUTORIZADOR`** | Menú *Solicitantes*, Menú *Autorizadores* (*Autorización de Solicitudes [A1]*, *Niveles Autorizantes [A2]*), *Solicitudes en curso*, *Histórico*. |
| **`ADMINISTRADOR`** | **Acceso total**: Los 5 menús y las 17 sub-vistas habilitadas. |

---

## 9. Paso 8: Checklist de Pruebas y Certificación Post-Despliegue

Una vez completado el despliegue, realiza las siguientes pruebas de verificación:

- [ ] **Acceso y Perfil**: Abre la URL de la Web App en una ventana de incógnito; debe cargar tu nombre, correo y foto desde Google Workspace.
- [ ] **Bloqueo de 15 Días en S1**: Si el usuario tiene un anticipo en `PAGADO` o en `RECHAZO-CIERRE` con antigüedad $\ge 15\text{ días}$, el modal de bloqueo debe activarse e impedir la creación de nuevas solicitudes.
- [ ] **Creación de Solicitud (S1)**: Crea una solicitud con presupuesto suficiente; debe registrarse con estado `INICIADO` y enviar correo al Autorizador Nivel 1 con el botón `[ Revisar Solicitud ]`.
- [ ] **Flujo Sin Presupuesto (S1 $\rightarrow$ S2 $\rightarrow$ S2.1)**: Crea una solicitud con monto superior al presupuesto; debe guardarse como `RECHAZO-PRESUPUESTO`, aparecer en *Solicitudes Rechazadas (S2)* y permitir justificar en *S2.1*.
- [ ] **Resolución por Correo y Deep-Link (A1 / A1.1)**: Haz clic en el botón `[ Revisar Solicitud ]` del correo; debe abrir [View_A1_1.html](file:///d:/Roberto/Documents/Antigravity%20D/Viaticos/V3_MVP/Codigo%20producido/View_A1_1.html) omitiendo datos bancarios y permitiendo resolver con comentarios.
- [ ] **Catálogo de Rutas (A2)**: Ingresa a *Niveles Autorizantes*; debe mostrar las 16 rutas corporativas con los umbrales $x_1=\$50$ y $x_2=\$200$.
- [ ] **Provisión en Compras (E1 $\rightarrow$ E1.1)**: Con rol `EDITOR-COMPRAS`, aprueba en E1.1, verifica el badge de cuenta editada (`Modificado manualmente` vs `Normal`), agrúpala con asiento contable en E1; debe transicionar a `ENVIADO A PAGO` y anexar el comprobante contable sin sobreescribir archivos.
- [ ] **Procesamiento en Tesorería (E2 $\rightarrow$ E2.1)**: Con rol `EDITOR-TESORERIA`, procesa el desembolso en E2.1, agrúpala en E2 adjuntando comprobante bancario; debe transicionar a `PAGADO` (si es anticipo) o `FINALIZADO` (si es reintegro).
- [ ] **Cierre Solicitante (S3 $\rightarrow$ S3.1)**: Con rol `SOLICITANTE`, ingresa a *Cierre de solicitudes*, sube las facturas y comprobantes en S3.1; debe transicionar a `LIQUIDADO`.
- [ ] **Cierre Compras (E3 $\rightarrow$ E3.1)**: Con rol `EDITOR-COMPRAS`, revisa la liquidación en E3.1, agrúpala contablemente en E3 si tuvo reintegro; debe culminar con estado `FINALIZADO`.
- [ ] **Visor "Solicitudes en curso"**: Verifica que solo muestre solicitudes en estados activos no terminales y que el expediente progresivo acumulativo renderice condicionalmente las etapas completadas con botón `[ Imprimir ]`.
- [ ] **Repositorio "Histórico"**: Verifica que solo contenga los 3 estados terminales (`FINALIZADO`, `CANCELADO`, `RECHAZO-AUTORIZACION`), muestre el expediente final inmutable y permita imprimir.

---

## 10. Mantenimiento y Actualizaciones Futuras

Cuando realices modificaciones en el código:
1. Aplica los cambios en los archivos correspondientes en Apps Script.
2. Haz clic en **Implementar** >> **Administrar implementaciones**.
3. Edita la implementación activa (icono de lápiz ✏️).
4. En el selector de **Versión**, elige **Nueva versión**.
5. Haz clic en **Implementar**.

> [!CAUTION]
> Si no creas una *Nueva versión* al actualizar la implementación, Google Apps Script continuará sirviendo la versión anterior en caché a los usuarios.
