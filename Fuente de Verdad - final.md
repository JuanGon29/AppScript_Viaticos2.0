# Especificación Funcional y Fuente de Verdad Operativa — Sistema de Viáticos 2.0

---

## 1. Descripción General y Roles del Sistema

El sistema gestiona el ciclo integral de solicitud, validación presupuestaria, aprobación corporativa, provisión contable, desembolso en tesorería y liquidación/cierre de viáticos institucionales.

### Descripción Holística de los Roles

* **SOLICITANTE**: Los usuarios que tengan asignado este rol podrán ver en la Home Page las siguientes pestañas del menú lateral:
  * **Solicitantes** (con subpestañas: *Nueva Solicitud*, *Solicitudes Rechazadas*, *Cierre de solicitudes*)
  * **Solicitudes en curso**
  * **Histórico**
* **EDITOR-COMPRAS**: Tiene acceso a todo lo del rol SOLICITANTE, más la pestaña **Operaciones**, de la cual tiene acceso a las siguientes subpestañas:
  * **Provisión de pagos** (E1)
  * **Cierre de solicitudes** (E3)
  * Adicionalmente: **Solicitudes en curso** e **Histórico**.
* **EDITOR-TESORERIA**: Tiene acceso a todo lo del rol SOLICITANTE, más la pestaña **Operaciones**, de la cual tiene acceso a la siguiente subpestaña:
  * **Procesamiento de pagos** (E2)
  * Adicionalmente: **Solicitudes en curso** e **Histórico**.
* **AUTORIZADOR**: Permite ver lo mismo que el rol de SOLICITANTE, más la pestaña **Autorizadores** (con subpestañas: *Autorización de Solicitudes*, *Niveles Autorizantes*), **Solicitudes en curso** e **Histórico**.
* **ADMINISTRADOR**: Tiene acceso total a todas las pestañas y módulos disponibles en la Home Page (*Solicitantes*, *Operaciones*, *Autorizadores*, *Solicitudes en curso*, *Histórico*).

---

## 2. Ciclo de Vida y Listado Oficial de Estados

El ciclo de vida de una solicitud de viáticos se rige por los siguientes estados operacionales:

* **`INICIADO`**: Cuando el usuario crea una nueva solicitud y el presupuesto para la solicitud es suficiente. Aquí el actor actual será el nivel autorizante que corresponda en primera instancia, y así sucesivamente con los otros niveles autorizantes según se vayan aprobando. También se adquiere este estado cuando una solicitud fuera de presupuesto (`RECHAZO-PRESUPUESTO`) o rechazada en provisión 1 (`RECHAZO-PROVISION 1`) es debidamente solventada y reinicia la ruta de aprobación.
* **`RECHAZO-PRESUPUESTO`**: Cuando el usuario crea una nueva solicitud y el presupuesto para la solicitud no es suficiente. Aquí el actor será `"Solicitante"`, pues este debe ingresar una justificación si desea que la solicitud continúe. Al justificar la solicitud en S2.1, esta volverá a pasar por el proceso de autorización y el estado volverá a `INICIADO`, activando la ruta autorizante correspondiente para solicitudes fuera de presupuesto.
* **`AUTORIZADO`**: Cuando la solicitud ha sido autorizada por todos los niveles autorizantes que correspondan. Corresponde al actor `"Compras"` realizar la revisión de la solicitud para la "Provisión de Pagos" (E1).
* **`RECHAZO-AUTORIZACION`**: Cuando la solicitud ha sido rechazada por algún nivel autorizante en A1.1. En este caso la solicitud se cierra completamente por rechazo y no se le puede dar continuación (estado terminal definitivo); queda sin ningún Actor Actual asociado (`ActorActual = ""`) y se libera el presupuesto reservado.
* **`ENVIADO A PAGO`**: Cuando la solicitud ha sido autorizada por todos los niveles autorizantes y Compras ha realizado la revisión y agrupación formal de provisión de pagos en E1. El actor actual pasa a ser `"Tesorería"` y este deberá gestionar el pago en la página "Procesamiento de Pagos" (E2).
* **`RECHAZO-PROVISION 1`**: Cuando la solicitud ha sido rechazada por Compras en "Provisión de pago" (E1.1) y en el campo `ResolucionProvision` se seleccionó *"Rechazo y requiere reevaluación"*. El actor actual será `"Solicitante"`. Cuando el solicitante solvente este rechazo en S2.1, la solicitud deberá volver a pasar por la validación de presupuesto y por las rutas autorizadoras desde cero con la información actualizada.
* **`RECHAZO-PROVISION 2`**: Cuando la solicitud ha sido rechazada por Compras en "Provisión de pago" (E1.1) y en el campo `ResolucionProvision` se seleccionó *"Rechazo por información faltante"*. El actor actual será `"Solicitante"`. Cuando el solicitante solvente este rechazo en S2.1, no tendrá que volver a pasar por validación de presupuesto ni rutas autorizadoras; actualizará la información y será enviada directamente de regreso a Compras (`AUTORIZADO`) en "Provisión de pagos".
* **`PAGADO`**: Cuando la solicitud ha sido pagada por el departamento de Tesorería. Este estado es usado para solicitudes clasificadas como `"Anticipo"` (`ClasificacionSolicitud`). En este instante aplica la regla operativa de control de 15 días: si transcurren 15 días o más tras la fecha de referencia sin que la solicitud pase a `LIQUIDADO`, se bloqueará al solicitante la creación de nuevas solicitudes en S1. Para solicitudes clasificadas como `"Reintegro"`, al completarse el pago en E2 el estado final pasa directamente a `FINALIZADO`.
* **`RECHAZO-PAGO 1`**: Cuando la solicitud ha sido rechazada por Tesorería en "Procesamiento de pago" (E2.1) y en el campo `ResolucionProcesamiento` se seleccionó *"Rechazo hacia solicitante"*. El actor actual será `"Solicitante"`. Cuando el solicitante solvente este rechazo en S2.1, se limpian los datos de provisión previa y la solicitud regresa a Compras (`AUTORIZADO`) para una nueva provisión contable limpia.
* **`RECHAZO-PAGO 2`**: Cuando la solicitud ha sido rechazada por Tesorería en "Procesamiento de pago" (E2.1) y en el campo `ResolucionProcesamiento` se seleccionó *"Rechazo hacia compras"*. El actor actual será `"Compras"`; Compras en "Provisión de pagos" (E1.1) editará la información requerida y, al guardar, la solicitud pasará nuevamente a `"Procesamiento de pagos"`.
* **`LIQUIDADO`**: Cuando la solicitud ha sido pagada, el viático fue utilizado y el solicitante completó y envió el cierre de solicitud en la página "S3 - Cierre de Solicitudes" (o solventó un rechazo de cierre en S2.1). Este estado es usado para solicitudes clasificadas como `"Anticipo"`.
* **`FINALIZADO`**: Estado terminal exitoso. Aplica cuando:
  1. La solicitud fue clasificada como `"Reintegro"` y Tesorería procesa el pago en E2.
  2. La solicitud fue clasificada como `"Anticipo"`, fue pagada, utilizada, liquidada por el solicitante en S3.1 y Compras auditó y aprobó el cierre definitivo en E3 / E3.1.
* **`RECHAZO-CIERRE`**: Cuando el solicitante ha realizado el cierre en "S3 - Cierre de Solicitudes" y Compras ha decidido rechazar la liquidación en E3.1. El actor de la solicitud se vuelve `"Solicitante"` y este tiene la opción de corregir y reenviar los comprobantes/acciones de cierre en S2.1, retornando la solicitud al estado `LIQUIDADO` con actor `"Compras"`. Aplica la regla de bloqueo de 15 días en S1 si permanece sin solventar.
* **`CANCELADO`**: Estado terminal por caducidad. Cuando una solicitud en estado de rechazo previo al pago (`RECHAZO-PRESUPUESTO`, `RECHAZO-PROVISION 1`, `RECHAZO-PROVISION 2` o `RECHAZO-PAGO 1`) permanece inactiva por 15 días consecutivos o más sin ser solventada por el solicitante. El sistema la cierra automáticamente de forma definitiva mediante un trigger diario, liberando el presupuesto reservado (si correspondía) y dejando el campo `ActorActual` vacío.

---

## 3. Reglas Globales y Políticas Transversales

### 3.1. Lógica General de Presupuesto y Validación

Cuando el solicitante da clic en *"Guardar solicitud"* en S1 (o al reevaluar en S2.1 tras un `RECHAZO-PROVISION 1`):
1. La información se registra inicialmente en la base de datos `BaseDatos_Viaticos2.0`, tabla `DimTransaccional`.
2. Se ejecuta de inmediato la validación de presupuesto dentro del archivo `Presupuesto_Viaticos2.0`, tabla `DimDisponible`.
   * **Ubicación de la fila**: Se determina en base a la clave `"CC-RC"` (concatenación del código de Centro de Costo `"CC"`, guion `"-"` y código de Rubro Contable `"RC"`).
   * **Ubicación de la columna**: Se determina según el mes calendario en que se crea/genera la solicitud del viático (extrayendo el mes de `FechaSolicitud`).

#### Casos de Presupuesto:
1. **Presupuesto disponible $\ge$ Monto solicitado**:
   * La celda consultada en `DimDisponible` se actualiza:
     $$\text{DimDisponible}_{\text{nuevo}} = \text{DimDisponible}_{\text{anterior}} - \text{Monto}$$
   * En la tabla `DimConsumo`, en la celda respectiva (CC-RC y mes), se suma el monto:
     $$\text{DimConsumo}_{\text{nuevo}} = \text{DimConsumo}_{\text{anterior}} + \text{Monto}$$
   * Se registra en la columna `DentroPresupuesto` de `DimTransaccional` el valor `"Si"`.
   * `EstadoSolicitud` adquiere el valor **`INICIADO`** y la solicitud pasa a la ruta de autorización correspondiente.
2. **Presupuesto disponible $<$ Monto solicitado**:
   * Los valores de las celdas en `DimDisponible` y `DimConsumo` no cambian (se mantienen intactos).
   * Se registra en la columna `DentroPresupuesto` de `DimTransaccional` el valor `"No"`.
   * `EstadoSolicitud` adquiere el valor **`RECHAZO-PRESUPUESTO`** y `ActorActual = "Solicitante"`.

#### Automatización Mensual de Arrastre de Presupuesto (Rollover):
El 1er día de cada mes a la 1:00 A.M. se ejecuta una automatización programada:
* Para el mes actual se consulta el saldo remanente del mes anterior en `DimDisponible` (a menos que el mes actual sea enero, en cuyo caso no se realiza arrastre de año anterior).
* El valor remanente del mes anterior se suma al disponible del mes actual en `DimDisponible`.
* Esta automatización cuenta con un interruptor parametrizado de encendido y apagado (`ON` / `OFF`).

#### Devolución Presupuestaria por Reintegro en Cierre (S3.1 / E3.1):
Si en S3.1 el solicitante seleccionó la modalidad `"Reintegro y cierre"` (con un `MontoReintegro` $> 0$) y en E3.1 el analista de Compras aprueba formalmente la liquidación (`ResolucionCierreE == "Aprobado"`):
* El monto a reintegrar (`MontoReintegro`) se devuelve de inmediato al presupuesto disponible de la institución: se **suma de vuelta en `DimDisponible`** para la celda correspondiente al centro de costo (`CC`) y rubro contable (`RC`).
* El mes para la restitución presupuestaria se determina a partir del mes en que se ejecuta la resolución final de cierre (`FechaCierreE`).
* En la tabla `DimConsumo` se **resta** ese mismo `MontoReintegro` de la celda respectiva, reduciendo el consumo presupuestario acumulado.

---

### 3.2. Reglas Globales de Control por Inactividad (15 Días)

El sistema implementa dos políticas diferenciadas de control a los 15 días según la fase del flujo:

#### Regla 1: Cancelación Automática por Inactividad (Solicitudes Pre-Pago en Rechazo)
Aplica exclusivamente a solicitudes en estados de rechazo donde los fondos **aún no han sido desembolsados**:
* `RECHAZO-PRESUPUESTO`
* `RECHAZO-PROVISION 1`
* `RECHAZO-PROVISION 2`
* `RECHAZO-PAGO 1`

* **Mecanismo**: Time-driven Trigger diario en backend (medianoche / 00:00 hrs).
* **Condición**: $\text{FechaHoy} - \text{FechaModificacion} \ge 15 \text{ días}$.
* **Acciones ejecutadas**:
  1. `EstadoSolicitud` pasa a **`CANCELADO`**.
  2. `ActorActual` pasa a **`""`** (vacío).
  3. `FechaModificacion` se actualiza con la marca temporal de cancelación.
  4. **Liberación de Presupuesto**: Si la solicitud retenía saldo reservado (`RECHAZO-PROVISION 2` o `RECHAZO-PAGO 1`), el monto se resta de `DimConsumo` y se suma de vuelta en `DimDisponible` del centro de costo y rubro correspondiente.

---

#### Regla 2: Bloqueo de Nuevas Solicitudes en S1 (Solicitudes Post-Pago sin Liquidar)
Aplica a solicitudes donde los fondos **ya fueron entregados al solicitante** y están pendientes de cierre o corrección de liquidación:
* `PAGADO` (Anticipos pendientes de liquidar en S3.1)
* `RECHAZO-CIERRE` (Liquidaciones rechazadas por Compras pendientes de corrección en S2.1)

* **Mecanismo**: Validación sincrónica al ingresar a la pantalla **S1 (Nueva Solicitud)**.
* **Condición**: El sistema consulta si el solicitante logueado posee al menos 1 solicitud en estado `PAGADO` o `RECHAZO-CIERRE` que cumpla:
  $$\text{FechaReferencia} = \max(\text{FechaFin (o FechaInicio si fue día único)}, \text{FechaModificacion})$$
  $$\text{Días transcurridos} = \text{FechaHoy} - \text{FechaReferencia} \ge 15 \text{ días}$$
* **Acciones ejecutadas**:
  1. La pantalla S1 se **bloquea inmediatamente**.
  2. Se despliega un **Pop-up modal bloqueante** con el siguiente mensaje:
     > *"No puedes crear nuevas solicitudes debido a que tienes solicitudes de viáticos pendientes de liquidar con más de 15 días de antigüedad. Por favor solventa o liquida tus solicitudes pendientes en 'Cierre de solicitudes' o 'Solicitudes rechazadas' antes de continuar."*
  3. El botón **"Entendido"** del modal redirige al usuario a la **Home Page**.
  4. La solicitud vencida **no se cancela** (permanece abierta exigiendo la rendición de cuentas).

---

### 3.3. Estructura de Almacenamiento de Archivos Adjuntos

1. Al guardar archivos adjuntos en el formulario de creación o en las etapas de corrección y liquidación, el sistema crea automáticamente una carpeta en Google Drive nombrada:
   $$\text{Archivos - [ID\_Solicitud]}$$
2. Dicha carpeta se genera dentro del directorio institucional:
   * **ID de Carpeta**: Obtenido en `Parametros_Viaticos2.0` (`ID_CARPETA_ADJUNTOS`).
3. En la columna `ArchivosAdjuntos` de `DimTransaccional` se almacena un arreglo JSON con los metadatos de cada archivo:
   ```json
   [
     {
       "NombreArchivo": "Factura_Hotel.pdf",
       "TipoArchivo": "application/pdf",
       "LinkArchivo": "https://drive.google.com/file/d/xxxx/view"
     }
   ]
   ```
4. Cuando Compras o Tesorería adjuntan archivos en los modales de agrupación contable (E1, E2, E3), o cuando el solicitante sube facturas en S3.1 / S2.1, el archivo nuevo se añade (*append*) al JSON existente sin sobreescribir los comprobantes previos.
5. **Garantía de Persistencia Multi-Pantalla**: Los mecanismos aplicados para asegurar la carga y lectura correcta de archivos en S1 aplican de forma idéntica en E1, E2, E3, S2.1, S3.1, A1.1, Solicitudes en curso e Histórico.

---

### 3.4. Estándar de Interfaz de Usuario (UI/UX), Diálogos y Patrones de Reutilización Modular

1. **Eliminación Total de Diálogos Nativos del Navegador**:
   * Queda estrictamente prohibido el uso de diálogos nativos del navegador (`alert()`, `confirm()`, `prompt()`) o mensajes automáticos del motor de Apps Script (`google.com dice:`).
   * Toda notificación de éxito, confirmación de decisión, error de carga de datos o advertencia de campos obligatorios debe implementarse mediante **modales interactivos HTML/CSS personalizados y componentes Toast corporativos** integrados dentro del DOM de la aplicación (siguiendo el estándar y comportamiento probado en S1).

2. **Mapeo de Plantillas de Diseño UI de Referencia y Archivos Implementados**:
   Cada pantalla del sistema se vincula directamente con sus maquetas en `Diseño UI/` y sus archivos modulares en `Codigo producido/`:

| Módulo / Pantalla | Maqueta Visual (`Diseño UI/`) | Vista Implementada (`Codigo producido/`) | Controlador JS (`Codigo producido/`) | Patrón Visual Base Heredado |
| :--- | :--- | :--- | :--- | :--- |
| **Login** | `Login Page.html` | `View_Login.html` | — | Diseño corporativo de autenticación |
| **Home Page** | `Home Page.html` | `View_Home.html` | `JS_Logic.html` | Layout con barra lateral y tarjetas de acceso |
| **S1 — Nueva Solicitud** | `Solicitantes/S1 Nueva Solicitud.html` | `View_NuevaSolicitud.html` | `JS_NuevaSolicitud.html` | **Patrón Canónico de Formularios** (Secciones Solicitante, Detalle, Modales) |
| **S2 — Solicitudes Rechazadas** | `Solicitantes/S2 Solicitudes Rechazadas.html` | `View_S2.html` | `JS_S2.html` | **Patrón de Bandeja Operativa E1** (Botón `[ Ver detalles ]`, Fechas `DD/MM/YYYY`) |
| **S2.1 — Detalle Rechazos** | `Solicitantes/S2.1 Justificacion de solicitud.html` | `View_S2_1.html` | `JS_S2.html` | **Estructura Formulario S1** + Tablas de rechazo previo + Campos según Caso (A-E) |
| **S3 — Cierre de Solicitudes** | `Solicitantes/S3 Cierre de solicitudes.html` | `View_S3.html` | `JS_S3.html` | **Patrón de Bandeja Operativa E1** |
| **S3.1 — Liquidación / Cierre** | `Solicitantes/S3.1 Cierre de solicitud.html` | `View_S3_1.html` | `JS_S3.html` | **Patrón Canónico de Expediente Progresivo** (Transición `Responder` $\to$ `Guardar`) |
| **A1 — Bandeja Autorización** | `Autorizadores/A1 Autorizacion de Solicitudes.html` | `View_A1.html` | `JS_A1.html` | **Patrón de Bandeja Operativa E1** (Solicitante sólo nombre, Fechas `DD/MM/YYYY`) |
| **A1.1 — Detalle Autorización** | `Autorizadores/A1.1 Autorizacion de Solicitud.html` | `View_A1_1.html` / `View_Resolucion.html` | `JS_A1.html` | **Estructura Formulario S1** en modo lectura (con detalle bancario) + Modal S1 |
| **E1 — Provisión de Pagos** | `Editores/E1 Provision de pagos.html` | `View_E1.html` | `JS_E1.html` | **Patrón Canónico de Bandeja Operativa** (`[ Agrupar ]`, `[ Limpiar filtros ]`) |
| **E1.1 — Detalle Provisión** | `Editores/E1.1 Provision de pago.html` | `View_E1_1.html` | `JS_E1.html` | **Estructura Formulario S1** en modo lectura + Acciones de Provisión |
| **E2 — Procesamiento Pagos** | `Editores/E2 Procesamiento de pagos.html` | `View_E2.html` | `JS_E2.html` | **Patrón de Bandeja Operativa E1** (`[ Agrupar ]` comprobante TEF) |
| **E2.1 — Detalle Procesamiento**| `Editores/E2.1 Procesamiento de pago.html` | `View_E2_1.html` | `JS_E2.html` | **Estructura Formulario S1** en modo lectura + Datos contables E1 |
| **E3 — Cierre Compras** | `Editores/E3 Cierre de solicitudes.html` | `View_E3.html` | `JS_E3.html` | **Patrón de Bandeja Operativa E1** (`[ Agrupar ]` reintegros liquidados) |
| **E3.1 — Detalle Cierre Compras**| `Editores/E3.1 Cierre de solicitud.html` | `View_E3_1.html` | `JS_E3.html` | **Estructura Formulario S1** en modo lectura + 4 campos de liquidación |
| **Solicitudes en curso** | `Solicitudes en curso.html` | `View_EnCurso.html` | `JS_EnCurso.html` | **Tabla E1** (sin col `TIPO`, filtro por rol) / **Detalle idéntico a S3.1** |
| **Histórico** | `Historico.html` | `View_Historico.html` | `JS_Historico.html` | **Copia exacta de Solicitudes en curso** (solo estados terminales) |

3. **Reglas de Reutilización Modular y Jerarquía de Patrones UI (Directrices de `Observaciones y Comentarios.pdf`)**:
   * **Patrón Canónico de Formularios y Lectura (Heredado de S1 / `View_NuevaSolicitud.html`)**:
     * Toda sección denominada *"Información del solicitante"* en pantallas de detalle (S2.1, S3.1, A1.1, E1.1, E2.1, E3.1, Solicitudes en curso e Histórico) debe utilizar exactamente la misma distribución visual de 6 campos en solo lectura: *Nombre, Correo institucional, Cargo / Plaza, Gerencia, Centro de Costo, Agencia*.
     * Toda sección denominada *"Detalle del viático"* en modo lectura (A1.1, S2.1 Casos A y E, S3.1, E1.1, E2.1, E3.1, Solicitudes en curso e Histórico) debe desplegar los mismos campos que S1: *Duración, Fecha inicio, Fecha fin, Tipo de viático, Hora del evento, Tipo de solicitud, Detalle bancario completo (Destinatario, Monto, Banco, Tipo de cuenta, No. de cuenta), Motivo del viático y Archivos Adjuntos*.
   * **Patrón Canónico de Bandejas Operativas Tipo Tabla (Heredado de E1 / `View_E1.html`)**:
     * Las tablas de **S2, S3, A1, E2, E3, Solicitudes en curso e Histórico** deben adoptar el diseño de tabla de E1:
       * Formato de fechas unificado `DD/MM/YYYY` en la columna `Fechas`.
       * Botón de acción **`[ Ver detalles ]`** con icono de ojo estilizado.
       * Botón **`[ Limpiar filtros ]`** posicionado a la derecha de los filtros de cabecera.
       * Selector de paginación inferior de 10 (default), 20 y 30 registros.
       * Columna `SOLICITANTE`: Sólo muestra el nombre del colaborador (sin concatenar plaza/cargo).
   * **Patrón Canónico de Expediente Progresivo de Detalle (Heredado de S3.1 / `View_S3_1.html`)**:
     * La vista de detalle accesible desde `[ Ver detalles ]` en **Solicitudes en curso** e **Histórico** debe ser una réplica estructural de **S3.1**, renderizando progresivamente: *Información del solicitante $\to$ Detalle del viático $\to$ Información de solicitud $\to$ Información autorización $\to$ Información provisión de pagos $\to$ Información procesamiento de pagos*, más las dos secciones finales: *Información Cierre (Solicitante)* e *Información Cierre (Compras)*.
   * **Patrón de Diálogos y Modales Corporativos (Heredado de S1)**:
     * El pop-up modal corporativo de confirmación y feedback de éxito implementado en S1 debe utilizarse de forma homogénea en A1.1 al autorizar/rechazar, en S2.1 al enviar justificaciones o reevaluaciones, en S3.1 al liquidar y en E1/E2/E3 al agrupar o responder.

4. **Consistencia Visual y Directrices de Estilo**:
   * **Paleta Cromática Corporativa**: Navy institucional (`#000c2f` / `#001f5c`), Naranja de acción (`#ff5722`), Acentos de estado (Verde éxito `#28a745`, Rojo advertencia `#dc3545`, Celeste foco `#00b0ff`).
   * **Estados de Campos de Entrada**: Borde rojo (obligatorio vacío), Borde celeste (hover/foco), Borde verde (válido completado), Sin borde adicional (opcional).
   * **Formato de Fechas**: En todas las tablas operativas, filtros y vistas de detalle, las fechas deben formatearse invariablemente como `DD/MM/YYYY` (y `DD/MM/YYYY HH:mm` cuando incluyan hora).
   * **Columna Monto**: Encabezado con etiqueta `"Monto"` (sin usar "Monto Total") y formato numérico con 2 decimales `$XX.XX USD`.

---

## 4. Matriz y Definición de las 16 Rutas Autorizantes

### Parámetros y Umbrales
* $x_1 = \$50$ (Umbral 1)
* $x_2 = \$200$ (Umbral 2)

Las rutas de aprobación se determinan mediante una matriz combinatoria de 3 factores (**16 rutas autorizantes posibles**):
1. **Presupuesto (2 opciones)**: Con Presupuesto (`DentroPresupuesto = "Si"`) o Sin Presupuesto (`DentroPresupuesto = "No"`).
2. **Ubicación / Dependencia (2 opciones)**: Back Office (Gerencia $\neq$ "AGENCIAS") o Agencias (Gerencia $=$ "AGENCIAS").
3. **Caso por Plaza del Solicitante (4 opciones)**:
   * **Caso 1**: Colaborador regular u operativo (no es titular de gerencia ni director ejecutivo).
   * **Caso 2**: Gerente / Titular de Gerencia que cuenta con un Jefe Directo asignado (`PlazaJefe` en `DimGerencias`).
   * **Caso 3**: Gerente de primer nivel que reporta directamente a Dirección Ejecutiva.
   * **Caso 4**: Director Ejecutivo (Plaza "DIRECTOR EJECUTIVO").

---

### Matriz Resumen de las 16 Rutas Autorizantes

| Ruta | Presupuesto | Ubicación | Caso Plaza | Niveles Máx. | Secuencia de Autorización / Aprobadores | Actor Inicial |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **Ruta 1** | Sí | Back Office | Caso 1 | 3 | Nivel 1 (Gerente Área) $\to$ Nivel 2 (Finanzas, si >$50) $\to$ Nivel 3 (Director Ejecutivo, si >$200) | `Autorizador 1` |
| **Ruta 2** | Sí | Back Office | Caso 2 | 2 | Nivel 1 (Jefe Directo) $\to$ Nivel 2 (Director Ejecutivo, si >$50) | `Autorizador 1` |
| **Ruta 3** | Sí | Back Office | Caso 3 | 1 | Nivel 1 (Director Ejecutivo) | `Autorizador 1` |
| **Ruta 4** | Sí | Back Office | Caso 4 | 0 | Auto-aprobado (Sin niveles requeridos $\to$ `AUTORIZADO`) | `Compras` |
| **Ruta 5** | Sí | Agencias | Caso 1 | 4 | Nivel 0 (Jefe Regional) $\to$ Nivel 1 (Gerente Agencias) $\to$ Nivel 2 (Finanzas, si >$50) $\to$ Nivel 3 (Dir. Ejecutivo, si >$200) | `Autorizador 0` |
| **Ruta 6** | Sí | Agencias | Caso 2 | 2 | Nivel 1 (Jefe Directo) $\to$ Nivel 2 (Director Ejecutivo, si >$50) | `Autorizador 1` |
| **Ruta 7** | Sí | Agencias | Caso 3 | 1 | Nivel 1 (Director Ejecutivo) | `Autorizador 1` |
| **Ruta 8** | Sí | Agencias | Caso 4 | 0 | Auto-aprobado (Sin niveles requeridos $\to$ `AUTORIZADO`) | `Compras` |
| **Ruta 9** | No | Back Office | Caso 1 | 2 | Nivel 1 (Gerente Área) $\to$ Nivel 2 (Director Ejecutivo) [Fijo tras justificar] | `Autorizador 1` |
| **Ruta 10** | No | Back Office | Caso 2 | 1 | Nivel 1 (Director Ejecutivo) [Fijo tras justificar] | `Autorizador 1` |
| **Ruta 11** | No | Back Office | Caso 3 | 1 | Nivel 1 (Director Ejecutivo) [Fijo tras justificar] | `Autorizador 1` |
| **Ruta 12** | No | Back Office | Caso 4 | 0 | Auto-aprobado (Sin niveles requeridos $\to$ `AUTORIZADO`) | `Compras` |
| **Ruta 13** | No | Agencias | Caso 1 | 3 | Nivel 0 (Jefe Regional) $\to$ Nivel 1 (Gerente Agencias) $\to$ Nivel 2 (Director Ejecutivo) [Fijo tras justificar] | `Autorizador 0` |
| **Ruta 14** | No | Agencias | Caso 2 | 1 | Nivel 1 (Director Ejecutivo) [Fijo tras justificar] | `Autorizador 1` |
| **Ruta 15** | No | Agencias | Caso 3 | 1 | Nivel 1 (Director Ejecutivo) [Fijo tras justificar] | `Autorizador 1` |
| **Ruta 16** | No | Agencias | Caso 4 | 0 | Auto-aprobado (Sin niveles requeridos $\to$ `AUTORIZADO`) | `Compras` |

---

### Desglose Detallado de las 16 Rutas Autorizantes

#### Grupo A: Rutas con Presupuesto (`DentroPresupuesto = "Si"`) — Back Office

* **Ruta 1**: Colaborador regular de Back Office con presupuesto.
  * **Nivel 1**: Correo autorizador para la gerencia del solicitante (`CorreoGerente` / `CorreoAutorizador` en `DimGerencias`).
  * **Nivel 2**: Correo autorizador de Finanzas (`GERENCIA DE FINANZAS` en `DimGerencias`).
  * **Nivel 3**: Correo autorizador de Dirección Ejecutiva (`DIRECCION EJECUTIVA` en `DimGerencias`).
  * *Escalamiento por monto*:
    * Si $0 < \text{Monto} \le \$50$: Requiere **1 nivel** (Nivel 1). `AutorizacionesPendientes = 1`. `ActorActual = "Autorizador 1"`.
    * Si $\$50 < \text{Monto} \le \$200$: Requiere **2 niveles** (Nivel 1 $\to$ Nivel 2). `AutorizacionesPendientes = 2`. `ActorActual = "Autorizador 1"`.
    * Si $\text{Monto} > \$200$: Requiere **3 niveles** (Nivel 1 $\to$ Nivel 2 $\to$ Nivel 3). `AutorizacionesPendientes = 3`. `ActorActual = "Autorizador 1"`.

* **Ruta 2**: Titular de gerencia de Back Office con jefe directo y con presupuesto.
  * **Nivel 1**: Correo autorizador del jefe directo del solicitante (`PlazaJefe` en `DimGerencias`).
  * **Nivel 2**: Correo autorizador de Dirección Ejecutiva (`DIRECCION EJECUTIVA` en `DimGerencias`).
  * *Escalamiento por monto*:
    * Si $0 < \text{Monto} \le \$50$: Requiere **1 nivel** (Nivel 1). `AutorizacionesPendientes = 1`. `ActorActual = "Autorizador 1"`.
    * Si $\text{Monto} > \$50$: Requiere **2 niveles** (Nivel 1 $\to$ Nivel 2). `AutorizacionesPendientes = 2`. `ActorActual = "Autorizador 1"`.

* **Ruta 3**: Gerente de Back Office que reporta directamente a Dirección Ejecutiva con presupuesto.
  * **Nivel 1**: Correo autorizador para Dirección Ejecutiva (`DIRECCION EJECUTIVA` en `DimGerencias`).
  * Requiere exactamente **1 nivel** fijo sin importar el monto. `AutorizacionesPendientes = 1`. `ActorActual = "Autorizador 1"`.

* **Ruta 4**: Director Ejecutivo en Back Office con presupuesto.
  * No requiere niveles autorizantes (**0 niveles**). `AutorizacionesPendientes = 0`. Pasa automáticamente a `AUTORIZADO` con `ActorActual = "Compras"`.

#### Grupo B: Rutas con Presupuesto (`DentroPresupuesto = "Si"`) — Agencias

* **Ruta 5**: Colaborador regular de Agencia con presupuesto. Cuenta con un **Nivel 0 previo obligatorio (Jefe Regional)** y hasta 4 niveles en total:
  * **Nivel 0**: Correo autorizador del Jefe Regional según región (`CorreoJefeRegional` en `DimRegiones`).
  * **Nivel 1**: Correo autorizador de Gerencia de Agencias (`DimGerencias`).
  * **Nivel 2**: Correo autorizador de Finanzas (`GERENCIA DE FINANZAS` en `DimGerencias`).
  * **Nivel 3**: Correo autorizador de Dirección Ejecutiva (`DIRECCION EJECUTIVA` en `DimGerencias`).
  * *Escalamiento por monto*:
    * Si $0 < \text{Monto} \le \$50$: Requiere **2 niveles** (Nivel 0 $\to$ Nivel 1). `AutorizacionesPendientes = 2`. `ActorActual = "Autorizador 0"`.
    * Si $\$50 < \text{Monto} \le \$200$: Requiere **3 niveles** (Nivel 0 $\to$ Nivel 1 $\to$ Nivel 2). `AutorizacionesPendientes = 3`. `ActorActual = "Autorizador 0"`.
    * Si $\text{Monto} > \$200$: Requiere **4 niveles** (Nivel 0 $\to$ Nivel 1 $\to$ Nivel 2 $\to$ Nivel 3). `AutorizacionesPendientes = 4`. `ActorActual = "Autorizador 0"`.

* **Ruta 6**: Titular de agencia con jefe directo y con presupuesto.
  * **Nivel 1**: Correo autorizador del jefe directo (`PlazaJefe` en `DimGerencias`).
  * **Nivel 2**: Correo autorizador de Dirección Ejecutiva (`DIRECCION EJECUTIVA` en `DimGerencias`).
  * *Escalamiento por monto*:
    * Si $0 < \text{Monto} \le \$50$: Requiere **1 nivel** (Nivel 1). `AutorizacionesPendientes = 1`. `ActorActual = "Autorizador 1"`.
    * Si $\text{Monto} > \$50$: Requiere **2 niveles** (Nivel 1 $\to$ Nivel 2). `AutorizacionesPendientes = 2`. `ActorActual = "Autorizador 1"`.

* **Ruta 7**: Gerente de agencia que reporta directamente a Dirección Ejecutiva con presupuesto.
  * **Nivel 1**: Correo autorizador para Dirección Ejecutiva (`DIRECCION EJECUTIVA` en `DimGerencias`).
  * Requiere exactamente **1 nivel** fijo. `AutorizacionesPendientes = 1`. `ActorActual = "Autorizador 1"`.

* **Ruta 8**: Director Ejecutivo asignado a unidad de agencias con presupuesto.
  * No requiere niveles autorizantes (**0 niveles**). `AutorizacionesPendientes = 0`. Pasa automáticamente a `AUTORIZADO` con `ActorActual = "Compras"`.

#### Grupo C: Rutas sin Presupuesto (`DentroPresupuesto = "No"`) — Back Office
*(Al crearse la solicitud queda en `RECHAZO-PRESUPUESTO` con `ActorActual = "Solicitante"`. Al ingresar y enviar la justificación extraordinaria en S2.1, pasa a `INICIADO` y se activa la ruta autorizante fija correspondiente sin importar el monto).*

* **Ruta 9**: Colaborador regular de Back Office sin presupuesto.
  * Requiere exactamente **2 niveles fijos**:
    * **Nivel 1**: Gerente de Área del solicitante (`DimGerencias`).
    * **Nivel 2**: Dirección Ejecutiva (`DIRECCION EJECUTIVA` en `DimGerencias`).
  * `AutorizacionesPendientes = 2`. `ActorActual = "Autorizador 1"`.

* **Ruta 10**: Titular de gerencia de Back Office sin presupuesto.
  * Requiere exactamente **1 nivel fijo**:
    * **Nivel 1**: Dirección Ejecutiva (`DIRECCION EJECUTIVA` en `DimGerencias`).
  * `AutorizacionesPendientes = 1`. `ActorActual = "Autorizador 1"`.

* **Ruta 11**: Gerente de Back Office que reporta a Dirección Ejecutiva sin presupuesto.
  * Requiere exactamente **1 nivel fijo**:
    * **Nivel 1**: Dirección Ejecutiva (`DIRECCION EJECUTIVA` en `DimGerencias`).
  * `AutorizacionesPendientes = 1`. `ActorActual = "Autorizador 1"`.

* **Ruta 12**: Director Ejecutivo en Back Office sin presupuesto.
  * No requiere niveles autorizantes (**0 niveles**). Pasa automáticamente a `AUTORIZADO` con `ActorActual = "Compras"`.

#### Grupo D: Rutas sin Presupuesto (`DentroPresupuesto = "No"`) — Agencias
*(Al crearse queda en `RECHAZO-PRESUPUESTO` con `ActorActual = "Solicitante"`. Al enviar justificación extraordinaria en S2.1, pasa a `INICIADO` y activa la ruta fija correspondiente).*

* **Ruta 13**: Colaborador regular de Agencia sin presupuesto.
  * Requiere exactamente **3 niveles fijos** (con Nivel 0 obligatorio):
    * **Nivel 0**: Jefe Regional (`CorreoJefeRegional` en `DimRegiones`).
    * **Nivel 1**: Gerente de Agencias (`DimGerencias`).
    * **Nivel 2**: Dirección Ejecutiva (`DIRECCION EJECUTIVA` en `DimGerencias`).
  * `AutorizacionesPendientes = 3`. `ActorActual = "Autorizador 0"`.

* **Ruta 14**: Titular de agencia sin presupuesto.
  * Requiere exactamente **1 nivel fijo**:
    * **Nivel 1**: Dirección Ejecutiva (`DIRECCION EJECUTIVA` en `DimGerencias`).
  * `AutorizacionesPendientes = 1`. `ActorActual = "Autorizador 1"`.

* **Ruta 15**: Gerente de agencia que reporta a Dirección Ejecutiva sin presupuesto.
  * Requiere exactamente **1 nivel fijo**:
    * **Nivel 1**: Dirección Ejecutiva (`DIRECCION EJECUTIVA` en `DimGerencias`).
  * `AutorizacionesPendientes = 1`. `ActorActual = "Autorizador 1"`.

* **Ruta 16**: Director Ejecutivo asignado a agencias sin presupuesto.
  * No requiere niveles autorizantes (**0 niveles**). Pasa automáticamente a `AUTORIZADO` con `ActorActual = "Compras"`.

---

## 5. Sistema de Notificaciones y Flujo de Resolución de Autorizaciones

### 5.1. Arquitectura de Notificación vía Correo Electrónico (Gmail HTML Cards)

Para garantizar total viabilidad operativa sin requerir configuraciones complejas de dominios ni APIs externas, el sistema utiliza **Tarjetas HTML Interactivas por Gmail (`GmailApp.sendEmail`)** combinadas con la **Página de Resolución Web (`A1.1` / `View_Resolucion.html`)** servida desde la Web App (`doGet`).

1. **Remitente Oficial del Sistema**: Todo correo de notificación de viáticos se despacha con el nombre de remitente: **`Notificaciones_Viaticos2.0`**.
2. **Estructura y Privacidad de la Tarjeta HTML**:
   * **Encabezado y Branding**: Colores corporativos Banco Integral (Navy `#000c2f` / `#001f5c`, Naranja `#ff5722`), logotipo institucional y badge destacado con el `ID_Solicitud`.
   * **Monto y Presupuesto**: Monto en dólares (`$XX.XX USD`) y badge visual (`✓ Dentro de Presupuesto` / `⚠ Fuera de Presupuesto`).
   * **Campos Informativos de Lectura**: Solicitante, Cargo, Gerencia, Centro de Costo, Agencia, Tipo de Viático, Franja Horaria (si aplica), Duración, Fechas, Clasificación (`Anticipo` o `Reintegro`) y Motivo Detallado.
   * **Privacidad y Seguridad Estricta**: **NUNCA** se incluye información bancaria (Banco, Número de cuenta ni Tipo de cuenta) en los correos electrónicos.
   * **Botón de Acción Único**:
     * **`[ Revisar Solicitud ]`** $\to$ Redirige a: `${WebAppURL}?view=a1_1&id=SOL-XXX`

### 5.2. Estructura de Historial de Comentarios en `DatosAutorizacion`

El historial cronológico de autorizaciones se guarda en la columna `DatosAutorizacion` como un arreglo JSON estructurado:

```json
[
  {
    "nivel": 1,
    "nombre": "Juan Pérez",
    "comentario": "Presupuesto verificado y correcto.",
    "resolucion": "APROBADO",
    "fecha": "10/08/26 09:30"
  },
  {
    "nivel": 2,
    "nombre": "María López",
    "comentario": "Aprobado, pero revisar la entrega en 30 días.",
    "resolucion": "APROBADO",
    "fecha": "11/08/26 14:15"
  },
  {
    "nivel": 3,
    "nombre": "Carlos Ruiz",
    "comentario": "Aprobación final concedida.",
    "resolucion": "APROBADO",
    "fecha": "12/08/26 11:00"
  }
]
```

### 5.3. Control de Concurrencia y Transición
* Cada vez que un autorizador aprueba en A1.1:
  $$\text{AutorizacionesPendientes} = \text{AutorizacionesPendientes} - 1$$
* Si `AutorizacionesPendientes > 0`: Se despacha el correo al siguiente autorizador y `ActorActual` se actualiza.
* Si `AutorizacionesPendientes == 0`: La solicitud transiciona a `EstadoSolicitud = "AUTORIZADO"`, `ActorActual = "Compras"` y se notifica a Compras.
* Si algún autorizador rechaza: `EstadoSolicitud` pasa a `RECHAZO-AUTORIZACION`, `ActorActual = ""` y se libera de inmediato cualquier presupuesto reservado en `DimDisponible`.
* Se implementa bloqueo de interfaz para evitar votos duplicados o resoluciones contradictorias una vez emitida la decisión.

---

## 6. Modelo de Datos, Catálogos y Parámetros Globales

### 6.1. Identificadores de Google Sheets (`Parametros_Viaticos2.0`)

| Clave | Valor | Descripción | NombreArchivo | TablasArchivo |
| :---- | :---- | :---- | :---- | :---- |
| `ID_DB_MAESTRO` | `1_ZSZS_MBNDtf535kUIhjyJ4KWNzeR1COKr6tYi_TBTs` | Posee las tablas dimensiones o catálogos generales que pueden ser compartidos por diferentes Apps o proyectos. | `1 - DB_Maestro_Global` | `DimGerencias`, `DimAreas`, `DimAgencias`, `DimRegiones`, `DimUsuarios` |
| `ID_DB_TRANSACCIONES` | `1a9uqIqv_Wml_A2yr-GYdXbiyLp6QGxOR5IbD9ggwo5g` | Posee 1 tabla que será donde se guardará la información tabular y los links o URLs de archivos adjuntos. | `BaseDatos_Viaticos2.0` | `DimTransaccional` |
| `ID_DB_PRESUPUESTO` | `1nqlZkKo8QSFx6r4-Nlg1ZUlCN-3YBN_5vH31QWFQ0UA` | Posee las tablas dimensiones o catálogos específicos para temas de presupuestos para viáticos. | `Presupuesto_Viaticos2.0` | `DimPresupuestoInicial`, `DimDisponible`, `DimConsumo` |
| `ID_CARPETA_ADJUNTOS` | `13UoxfM1c0kzrB8yh7JjhlfbeFEjVlKj6` | Posee la carpeta en Google Drive donde se guardarán los archivos adjuntos de las solicitudes. |  |  |
| `CHAT_WEBHOOK_URL` | `https://chat.googleapis.com/v1/spaces/AAAA-8bO66k/messages?key=[GCP_API_KEY]&token=r5lWp281nK-i1uC8u0l3QO0N5U7W44k3` | URL del Webhook de Google Chat para notificaciones auxiliares. |  |  |

---

### 6.2. Catálogo Oficial de Configuración (`CATALOGO_CONFIG`)

```javascript
const CATALOGO_CONFIG = {
  viaticos: {
    // 1. CATEGORÍAS DE VIÁTICOS (Punto de partida del usuario)
    categorias: [
      { id: 1, nombre: "Reunión/Trabajo fuera de horario laboral", fk_rubro: 1, habilitado: true },
      { id: 2, nombre: "Refrigerios por reuniones mayores a 4 horas", fk_rubro: 1, habilitado: true },
      { id: 3, nombre: "Alojamiento", fk_rubro: 2, habilitado: true, roles: ["ADMIN", "SOLICITANTE"] },
      { id: 4, nombre: "Alimentación por visitas agencias", fk_rubro: 2, habilitado: true },
      { id: 5, nombre: "Transporte", fk_rubro: 2, habilitado: true },
      { id: 6, nombre: "Viático Movilidad (Operativos Móviles)", fk_rubro: 2, habilitado: true }
    ],

    // 2. RUBROS CONTABLES
    rubros: [
      { id: 1, codigo: "8110029900000", nombre: "8110029900000-OTRAS PRESTACIONES AL PERSONAL" },
      { id: 2, codigo: "8110050400000", nombre: "8110050400000-VIATICOS Y TRANSPORTE" }
    ],

    // 3. HORAS DE EVENTOS (Dependen de fk_categoria)
    horasEventos: [
      { id: 1, fk_categoria: 1, nombre: "Antes de las 7:00am", habilitado: true },
      { id: 2, fk_categoria: 1, nombre: "Posterior a las 7:30pm", habilitado: true },
      { id: 3, fk_categoria: 1, nombre: "Posterior a las 2:00pm (Sábado)", habilitado: true }
    ]
  }
};
```

---

### 6.3. Diccionario Completo de las 57 Columnas de `DimTransaccional`

La tabla `DimTransaccional` cuenta con **57 columnas estructuradas de forma correlativa** (desde la columna `A` hasta `BE`):

| Columna | Nombre de Cabecera | Tipo de Dato | Origen / Regla de Negocio |
| :--- | :--- | :--- | :--- |
| **1 (A)** | `ID_Solicitud` | Texto | Correlativo único anual generado automáticamente por el sistema (ej. `SOL-2026-0001`). Clave primaria de la solicitud. |
| **2 (B)** | `EsPrueba` | Texto | Bandera `Si` / `No` para identificar registros generados en entorno de pruebas o desarrollo. |
| **3 (C)** | `EsEditado` | Texto | Bandera `Si` / `No` indicando si los datos bancarios fueron editados manualmente en S1 por el solicitante. |
| **4 (D)** | `EstadoSolicitud` | Texto | Estado actual del ciclo de vida (`INICIADO`, `RECHAZO-PRESUPUESTO`, `AUTORIZADO`, `RECHAZO-AUTORIZACION`, `ENVIADO A PAGO`, `RECHAZO-PROVISION 1`, `RECHAZO-PROVISION 2`, `PAGADO`, `RECHAZO-PAGO 1`, `RECHAZO-PAGO 2`, `LIQUIDADO`, `FINALIZADO`, `RECHAZO-CIERRE`, `CANCELADO`). |
| **5 (E)** | `AutorizacionesPendientes` | Número | Conteo numérico de niveles autorizantes pendientes de emitir su resolución (de `0` a `4`). |
| **6 (F)** | `ActorActual` | Texto | Actor o rol responsable de la siguiente acción operativa (`Autorizador 0`, `Autorizador 1`, `Autorizador 2`, `Autorizador 3`, `Compras`, `Tesorería`, `Solicitante`, o vacío si concluida/cancelada). |
| **7 (G)** | `FechaSolicitud` | Fecha/Hora | Fecha y hora exacta de creación y guardado inicial del viático en formato `DD/MM/YYYY HH:mm`. |
| **8 (H)** | `FechaModificacion` | Fecha/Hora | Última fecha y hora en que la solicitud cambió de estado o fue actualizada (`DD/MM/YYYY HH:mm`). |
| **9 (I)** | `NombreSolicitante` | Texto | Nombre completo del colaborador que crea la solicitud (obtenido de `DimUsuarios`). |
| **10 (J)** | `CorreoSolicitante` | Texto | Correo institucional del colaborador solicitante. |
| **11 (K)** | `CargoSolicitante` | Texto | Cargo o plaza institucional del solicitante (obtenido de `DimUsuarios`). |
| **12 (L)** | `Gerencia` | Texto | Gerencia a la que pertenece el solicitante (obtenido de `DimUsuarios`). |
| **13 (M)** | `CentroCosto` | Texto | Centro de Costo asignado al solicitante (ej. `510-PROCESOS`). |
| **14 (N)** | `Agencia` | Texto | Agencia o sucursal física asignada al solicitante (ej. `FLOR BLANCA`). |
| **15 (O)** | `DuracionActividad` | Texto | Modalidad de duración seleccionada: `Día único` o `Rango de días`. |
| **16 (P)** | `FechaInicio` | Fecha | Fecha de inicio de la comisión o actividad de viáticos (`DD/MM/YYYY` o `YYYY-MM-DD`). |
| **17 (Q)** | `FechaFin` | Fecha | Fecha de finalización de la actividad (`DD/MM/YYYY` o `YYYY-MM-DD`). |
| **18 (R)** | `TipoViatico` | Texto | Categoría de viático seleccionada según catálogo oficial (ej. `Reunión/Trabajo fuera de horario laboral`, `Alojamiento`, `Transporte`, etc.). |
| **19 (S)** | `HoraEvento` | Texto | Franja horaria para viáticos fuera de horario laboral (`Antes de las 7:00am`, `Posterior a las 7:30pm`, `Posterior a las 2:00pm (Sábado)`). |
| **20 (T)** | `TipoSolicitud` | Texto | Modalidad de destinatario: `Personal` (para el mismo solicitante) o `Delegado` (para otro colaborador del mismo centro de costo). |
| **21 (U)** | `Destinatario` | Texto | Nombre completo del colaborador que recibirá los fondos del viático. |
| **22 (V)** | `CorreoDestinatario` | Texto | Correo electrónico institucional del beneficiario de los fondos. |
| **23 (W)** | `Monto` | Número | Monto solicitado en dólares ($ USD con 2 decimales). |
| **24 (X)** | `Banco` | Texto | Nombre de la entidad bancaria donde se abonará el viático (ej. `BANCO INTEGRAL`). |
| **25 (Y)** | `TipoCuenta` | Texto | Tipo de cuenta bancaria del destinatario (`AHORRO`, `CORRIENTE`). |
| **26 (Z)** | `NumeroCuenta` | Texto | Número de cuenta bancaria para la transferencia de fondos. |
| **27 (AA)** | `MotivoViatico` | Texto | Justificación y descripción cualitativa del motivo del gasto. |
| **28 (AB)** | `RubroContable` | Texto | Cuenta contable asociada (`8110029900000-OTRAS PRESTACIONES AL PERSONAL` o `8110050400000-VIATICOS Y TRANSPORTE`). |
| **29 (AC)** | `ClasificacionSolicitud` | Texto | Clasificación operativa: `Reintegro` si $\text{FechaSolicitud} - \text{FechaInicio} \le 2\text{ días}$, o `Anticipo` si $> 2\text{ días}$. |
| **30 (AD)** | `ArchivosAdjuntos` | JSON / Texto | Arreglo JSON con la metadata de archivos y comprobantes adjuntos `[{"NombreArchivo": "...", "TipoArchivo": "...", "LinkArchivo": "..."}]`. |
| **31 (AE)** | `CorreoJefeRegional` | Texto | Correo del Autorizador Nivel 0 (Jefe Regional para Agencias de `DimRegiones`). Vacío si no aplica. |
| **32 (AF)** | `CorreoAutorizador1` | Texto | Correo institucional del Autorizador Nivel 1 (Gerente de Área, Jefe Directo o Director Ejecutivo según la ruta). |
| **33 (AG)** | `CorreoAutorizador2` | Texto | Correo institucional del Autorizador Nivel 2 (Gerencia de Finanzas o Director Ejecutivo según la ruta). Vacío si no aplica. |
| **34 (AH)** | `CorreoAutorizador3` | Texto | Correo institucional del Autorizador Nivel 3 (Director Ejecutivo en Caso 1 para montos > $200). Vacío si no aplica. |
| **35 (AI)** | `DentroPresupuesto` | Texto | Indicador de disponibilidad presupuestaria (`Si` si había saldo disponible en `DimDisponible`, `No` si no hubo saldo y requirió justificación). |
| **36 (AJ)** | `DatosAutorizacion` | JSON / Texto | Historial y bitácora estructurada de resoluciones de autorizadores `[{"nivel": N, "nombre": "...", "comentario": "...", "resolucion": "...", "fecha": "..."}]`. |
| **37 (AK)** | `JustifcacionPresupuesto` | Texto | Justificación extraordinaria de sobregiro presupuestario ingresada por el solicitante en S2.1 (cabecera histórica/sincronizada en hoja transaccional). |
| **38 (AL)** | `ResolucionProvision` | Texto | Decisión emitida por Compras en E1.1 (`Aprobado`, `Rechazo y requiere reevaluación`, `Rechazo por información faltante`). |
| **39 (AM)** | `ComentarioProvision` | Texto | Observaciones y comentarios detallados ingresados por el analista de Compras durante la provisión en E1.1. |
| **40 (AN)** | `FechaProvision` | Fecha/Hora | Fecha y hora en que Compras realizó la provisión en E1.1 (`DD/MM/YYYY HH:mm`). |
| **41 (AO)** | `NombreProvision` | Texto | Nombre del analista o usuario del rol EDITOR-COMPRAS que realizó la provisión en E1.1. |
| **42 (AP)** | `AgrupableProvision` | Texto / JSON | Número de lote contable, cuenta contable, o identificador de agrupación asignado por Compras en E1.1. |
| **43 (AQ)** | `ResolucionProcesamiento` | Texto | Decisión emitida por Tesorería en E2.1 (`Aprobado`, `Rechazo hacia solicitante`, `Rechazo hacia compras`). |
| **44 (AR)** | `ComentarioProcesamiento` | Texto | Observaciones y comentarios ingresados por Tesorería al procesar o rechazar el desembolso en E2.1. |
| **45 (AS)** | `FechaProcesamiento` | Fecha/Hora | Fecha y hora en que Tesorería procesó el pago en E2.1 (`DD/MM/YYYY HH:mm`). |
| **46 (AT)** | `NombreProcesamiento` | Texto | Nombre del analista o usuario del rol EDITOR-TESORERIA que procesó el pago en E2.1. |
| **47 (AU)** | `AgrupableProcesamiento` | Texto / JSON | Número de comprobante de transferencia bancaria, lote TEF o referencia bancaria de desembolso en E2.1. |
| **48 (AV)** | `TipoCierre` | Texto | Modalidad de liquidación seleccionada por el solicitante en S3.1: `Solo cierre` (100% gastado) o `Reintegro y cierre` (con devolución de fondos sobrantes). |
| **49 (AW)** | `MontoReintegro` | Número | Monto en dólares ($ USD) devuelto o reintegrado a la cuenta institucional por el solicitante en liquidaciones parciales. |
| **50 (AX)** | `FechaReintegro` | Fecha | Fecha en que el solicitante realizó el depósito o transferencia bancaria de devolución de viáticos sobrantes. |
| **51 (AY)** | `FechaCierreS` | Fecha/Hora | Fecha y hora en que el solicitante completó y envió la liquidación y comprobantes en S3.1 (`DD/MM/YYYY HH:mm`). |
| **52 (AZ)** | `ResolucionCierreE` | Texto | Decisión final emitida por Compras en E3.1 al auditar la liquidación (`Aprobado`, `Rechazado`). |
| **53 (BA)** | `ComentarioCierreE` | Texto | Observaciones, motivos de aprobación o hallazgos ingresados por Compras durante la auditoría de cierre en E3.1. |
| **54 (BB)** | `FechaCierreE` | Fecha/Hora | Fecha y hora en que Compras dictaminó la resolución de cierre y liquidación final en E3.1 (`DD/MM/YYYY HH:mm`). |
| **55 (BC)** | `NombreCierreE` | Texto | Nombre del analista de Compras que auditó la liquidación en E3.1. |
| **56 (BD)** | `AgrupableCierreE` | Texto / JSON | Número de póliza de liquidación, identificador de archivo o lote contable final de liquidación en E3.1. |
| **57 (BE)** | `JustificacionPresupuesto` | Texto | Justificación completa ingresada por el solicitante en S2.1 para solicitudes que requirieron reevaluación extraordinaria fuera de presupuesto. |

---

### 6.4. Metadatos y Atributos del Diccionario de Datos

| Nombre de Atributo | Descripción / Significado Operativo |
| :--- | :--- |
| `app_label` | Etiqueta o texto con el que se identifica un campo visualmente en la interfaz de la Web App. |
| `db_label` | Nombre exacto del encabezado/columna con el que se identifica y guarda el campo en la tabla `DimTransaccional` (o tablas auxiliares). |
| `column_label` | Nombre de la columna en la tabla de catálogo maestro de la cual se extrae la información para poblar el campo de lectura. |
| `table_label` | Nombre de la tabla dimensional o catálogo del cual se extrae la información de lectura (ej. `DimUsuarios`, `DimGerencias`). |
| `sheet_label` | Nombre del archivo de Google Sheets o base de datos de origen (ej. `1 - DB_Maestro_Global`). |
| `data_type` | Tipo de dato admitido en el campo (`Texto`, `Número`, `Fecha`, `Fecha/Hora`, `JSON`, `Booleano`). |
| `html_element` | Tipo de control o elemento de interfaz web (`textbox`, `dropdown`, `textarea`, `file_uploader`, `badge`, `radio`). |
| `editable` | Define si el campo es editable por el usuario en esa pantalla (`Sí`, `No`, `Depende`). |
| `visible` | Define si el campo es visible para el usuario en la interfaz (`Sí`, `No`, `Depende`). |
| `required` | Define si el campo es obligatorio previo a ejecutar acciones como "Guardar", "Enviar" o "Confirmar" (`Sí`, `No`, `Depende`). |
| `possible_values` | Lista exhaustiva de valores permitidos para campos de selección o lista desplegable. |

> [!NOTE]
> **Reglas Técnicas Transversales**:
> 1. **Campos con atributo "Depende"**: Su disponibilidad, obligatoriedad o editabilidad se rige por las reglas de negocio descritas en la sección correspondiente (ej. `FechaFin` solo obligatoria en "Rango de días", `MontoReintegro` solo obligatorio si `TipoCierre == "Reintegro y cierre"`).
> 2. **Formato de "Código CC" en Tablas**: En todas las tablas operativas donde figure la columna `CODIGO CC` (E1, E2, E3, Solicitudes en curso, Histórico), se extrae y presenta exclusivamente el prefijo numérico del campo `CentroCosto` (ej. si `CentroCosto` es `"510-PROCESOS"`, se visualiza `"510"`).

---

## 7. Especificación Detallada de Módulos y Pantallas

---

### S1 — Nueva Solicitud

#### Referencia Visual de Diseño (UI & UX)
* **Plantilla Base**: `Diseño UI/Solicitantes/S1 Nueva Solicitud.html`.
* **Detalle Bancario**: Tabla estructurada según el estándar visual de `Diseño UI/Editores/E1.1 Provision de pago.html`.

#### Flujo Operativo y Contexto
El usuario ingresa desde la barra lateral: **Solicitantes >> Nueva Solicitud**. Al ingresar, se ejecuta la validación sincrónica de solicitudes sin liquidar (Control de 15 días). Si no posee bloqueos, se despliega el formulario compuesto por dos secciones:
1. **Datos del solicitante** (campos de solo lectura poblados desde `DimUsuarios`).
2. **Detalle del viático** (campos editables).

#### Comportamiento Visual de Campos:
* **Obligatorio sin completar**: Contorno rojo.
* **Mouse hover / Foco**: Contorno celeste.
* **Completado válidamente**: Contorno verde al perder el foco.
* **Opcional sin completar**: Sin color de contorno visible (celeste en hover).

#### Reglas de Campos en S1:
* **Duración de la actividad**: Dropdown obligatorio (`Día único` / `Rango de días`).
  * `Día único`: Habilita solo `Fecha inicio`.
  * `Rango de días`: Habilita `Fecha inicio` y `Fecha fin`. (Por defecto bloqueados hasta elegir opción).
* **Fecha inicio**: Formato `dd/mm/yyyy`. Obligatorio.
* **Fecha fin**: Formato `dd/mm/yyyy`. Obligatorio si está habilitado; no permite fechas iguales o anteriores a `Fecha inicio`.
* **Tipo de viático**: Dropdown obligatorio con las opciones: `Reunión/Trabajo fuera de horario laboral`, `Refrigerios por reuniones mayores a 4 horas`, `Alojamiento`, `Alimentación por visitas agencias`, `Transporte`, `Viático Movilidad (Operativos Móviles)`. La opción de `Viático Movilidad` solo aparece si el campo `EsMovil` en `DimUsuarios` es verdadero.
* **Hora del evento**: Dropdown habilitado y obligatorio **únicamente** si `Tipo de viático` es `Reunión/Trabajo fuera de horario laboral`. Opciones: `Antes de las 7:00am`, `Posterior a las 7:30pm`, `Posterior a las 2:00pm (Sábado)`. Bloqueado para cualquier otro tipo.
* **Tipo de solicitud**: Dropdown obligatorio (`Personal` / `Delegado`).
  * `Personal`: `Destinatario` se autocompleta con el nombre del solicitante y se cargan sus datos bancarios.
  * `Delegado`: Habilita dropdown en `Destinatario` filtrado exclusivamente con los usuarios de su mismo centro de costo.
* **Destinatario**: Bloqueado por defecto; se llena según `Tipo de solicitud`.
* **Monto**: Numérico obligatorio con hasta 2 decimales (usa punto `.` como separador decimal).
* **Banco, Tipo de cuenta, No. de cuenta**: Bloqueados por defecto y autorellenados según el destinatario.
* **Motivo del viático**: Área de texto obligatoria.
* **Añadir archivos**: Carga de múltiples archivos. Obligatorio si:
  $$\text{FechaSolicitud} - \text{FechaInicio} \le 2\text{ días}$$

#### Detalle Bancario y Modal de Edición Manual:
La información bancaria se presenta en una tabla titulada **"Detalle bancario"** con un botón **"Editar"** (icono de lápiz), habilitado solo cuando `Destinatario` esté seleccionado. Al hacer clic:
* Se muestra un pop-up modal corporativo de advertencia indicando que la edición corre bajo su responsabilidad.
* Al pulsar **"Cancelar"**, se cierra el modal.
* Al pulsar **"Proseguir"**, los campos `Banco`, `Tipo de cuenta` y `No. de cuenta` se vuelven editables, se fija `EsEditado = "Si"` y aparece un icono de flecha hacia atrás (**"Regresar"**) que permite revertir los valores originales del catálogo y bloquearlos nuevamente.

#### Diccionario de Campos de Formulario S1:

| app_label | db_label | column_label | table_label | sheet_label | Editable | Visible | Required |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Nombre | `NombreSolicitante` | `NombreUsuario` | `DimUsuarios` | `1 - DB_Maestro_Global` | No | Sí | No |
| Correo | `CorreoSolicitante` | `CorreoUsuario` | `DimUsuarios` | `1 - DB_Maestro_Global` | No | Sí | No |
| Cargo | `CargoSolicitante` | `Plaza` | `DimUsuarios` | `1 - DB_Maestro_Global` | No | Sí | No |
| Gerencia | `Gerencia` | `NombreGerencia` | `DimUsuarios` | `1 - DB_Maestro_Global` | No | Sí | No |
| Centro de costo | `CentroCosto` | `CentroCosto` | `DimUsuarios` | `1 - DB_Maestro_Global` | No | Sí | No |
| Agencia | `Agencia` | `NombreAgencia` | `DimUsuarios` | `1 - DB_Maestro_Global` | No | Sí | No |
| Duración de la actividad | `DuracionActividad` | | | | Sí | Sí | Sí |
| Fecha inicio | `FechaInicio` | | | | Sí | Sí | Sí |
| Fecha fin | `FechaFin` | | | | Depende | Sí | Depende |
| Tipo de viático | `TipoViatico` | | | | Sí | Sí | Sí |
| Hora del evento | `HoraEvento` | | | | Depende | Sí | Depende |
| Tipo de solicitud | `TipoSolicitud` | | | | Sí | Sí | Sí |
| Destinatario | `Destinatario` | `NombreUsuario` | `DimUsuarios` | `1 - DB_Maestro_Global` | Depende | Sí | Depende |
| Monto | `Monto` | | | | Sí | Sí | Sí |
| Banco | `Banco` | `NombreBanco` | `DimUsuarios` | `1 - DB_Maestro_Global` | Depende | Sí | Depende |
| Tipo de cuenta | `TipoCuenta` | `TipoCuenta` | `DimUsuarios` | `1 - DB_Maestro_Global` | Depende | Sí | Depende |
| No. de cuenta | `NumeroCuenta` | `NumeroCuenta` | `DimUsuarios` | `1 - DB_Maestro_Global` | Depende | Sí | Depende |
| Motivo del viático | `MotivoViatico` | | | | Sí | Sí | Sí |
| Añadir archivos | `ArchivosAdjuntos` | | | | Sí | Sí | Depende |

---

### S2 — Solicitudes Rechazadas

#### Referencia Visual de Diseño (UI & UX)
* **Plantilla Base**: `Diseño UI/Solicitantes/S2 Solicitudes Rechazadas.html`.
* **Adaptación Operativa**: La columna de acciones y los botones adoptan el diseño de `Diseño UI/Editores/E1 Provision de pagos.html` (botón interactivo **`[ Ver detalles ]`** con icono de ojo).

#### Flujo Operativo y Contexto
El solicitante ingresa desde la barra lateral a **Solicitudes Rechazadas**. En esta bandeja se visualizan exclusivamente las solicitudes del usuario que han sido rechazadas por presupuesto, por Compras en provisión (E1.1), por Tesorería en procesamiento de pagos (E2.1) o por Compras en cierre (E3.1).

#### Interfaz de Usuario (UI & UX)
* **Filtros**: ID Solicitud, Rango de Fechas (por `FechaSolicitud` en formato `DD/MM/YYYY`), Tipo de viático, Clasificación solicitud y Centro de Costo.
  > **Regla**: Se elimina el filtro y la columna de solicitante por ser la bandeja personal del usuario.
* **Botón "Limpiar filtros"**: Ubicado a la derecha de la barra de filtros.
* **Paginación**: Selector inferior de 10 (default), 20 y 30 registros por página.
* **Columna ACCIONES**: Botón interactivo **`[ Ver detalles ]`** para acceder a S2.1.

#### Estados Permitidos en S2:
* `RECHAZO-PRESUPUESTO`
* `RECHAZO-PROVISION 1`
* `RECHAZO-PROVISION 2`
* `RECHAZO-PAGO 1`
* `RECHAZO-CIERRE`

#### Diccionario de Columnas de la Tabla S2:

| column_label | db_label | db_label2 | Regla de Visualización |
| :--- | :--- | :--- | :--- |
| ID SOLICITUD | `ID_Solicitud` | | Formato correlativo (ej. `SOL-2026-0001`) |
| FECHAS | `FechaSolicitud` | `FechaModificacion` | Formato `DD/MM/YYYY` |
| TIPO DE VIÁTICO | `TipoViatico` | | Texto del catálogo |
| MONTO | `Monto` | | Formato `$XX.XX USD` (etiqueta del header `"Monto"`) |
| ESTADO SOLICITUD | `EstadoSolicitud` | | Badge de estado de rechazo |
| ACTOR ACTUAL | `ActorActual` | | `"Solicitante"` |
| CLASIFICACION SOLICITUD | `ClasificacionSolicitud` | | `"Anticipo"` o `"Reintegro"` |
| ACCIONES | | | Botón `[ Ver detalles ]` |

---

### S2.1 — Detalle y Solución de Solicitudes Rechazadas

#### Referencia Visual de Diseño (UI & UX)
* **Plantilla Base**: `Diseño UI/Solicitantes/S2.1 Justificacion de solicitud.html`.
* **Botones de Navegación**: Botones `[ Regresar ]` y `[ Enviar justificación ]` / `[ Guardar solicitud ]` / `[ Guardar ]`.

La apariencia, campos habilitados y comportamiento de S2.1 se adaptan según el estado actual de la solicitud:

---

#### A. S2.1 con Estado: `RECHAZO-PRESUPUESTO`
* **Flujo**: La solicitud fue rechazada por falta de saldo disponible en `DimDisponible`.
* **Estructura Visual**:
  * **Información del solicitante**: Modo solo lectura (`NombreSolicitante`, `CorreoSolicitante`, `CargoSolicitante`, `Gerencia`, `CentroCosto`, `Agencia`).
  * **Detalle del viático**: Modo **solo lectura** con los datos registrados en S1 (incluyendo Detalle bancario y Archivos adjuntos).
  * **Sección de rechazo previo**: No lleva tabla de rechazo previo.
  * **Campo editable inferior**: Campo obligatorio con etiqueta **"Justificación de viático fuera de presupuesto"** (`JustificacionPresupuesto`).
* **Botones**: `[ Regresar ]` y `[ Enviar justificación ]`.
* **Lógica al Guardar**:
  * Se registra la justificación en `JustificacionPresupuesto`.
  * `EstadoSolicitud` pasa a **`INICIADO`**.
  * `FechaModificacion` se actualiza.
  * Se activa la ruta autorizante extraordinaria para solicitudes sin presupuesto (Rutas 9 a 16 según plaza y ubicación) y se asigna el `ActorActual` correspondiente.
  * Se despacha la tarjeta HTML por correo al primer autorizador en turno.
  * Se muestra pop-up modal corporativo de confirmación de envío.

##### Columnas de Control Actualizadas en `DimTransaccional` (Caso A):
| db_label | Valor asignado |
| :--- | :--- |
| `EstadoSolicitud` | `INICIADO` |
| `ActorActual` | Primer nivel autorizante extraordinario asignado (`Autorizador 0` o `Autorizador 1`) |
| `FechaModificacion` | Fecha y hora actual del guardado |
| `JustificacionPresupuesto` | Texto de justificación ingresado por el solicitante |

---

#### B. S2.1 con Estado: `RECHAZO-PROVISION 1`
* **Flujo**: Compras dictaminó *"Rechazo y requiere reevaluación"*. El presupuesto fue liberado de inmediato en E1.1.
* **Estructura Visual**:
  * **Información del solicitante**: Modo solo lectura.
  * **Detalle del viático**: **Completamente editable** y precargado (fechas, motivo, tipo de viático, monto, destinatario, cuentas y archivos).
  * **Tabla informativa "Información de provisión de pago"** (lectura) con: `NombreProvision`, `FechaProvision` y `ComentarioProvision`.
  * **Campos editables inferiores**: No lleva campos adicionales (se edita en Detalle del viático).
* **Botones**: `[ Regresar ]` y `[ Guardar solicitud ]`.
* **Lógica al Guardar**:
  * Reinicia el historial en `DatosAutorizacion = []`.
  * Ejecuta nuevamente la validación presupuestaria en `DimDisponible`:
    * Con saldo: `EstadoSolicitud = "INICIADO"`, `DentroPresupuesto = "Si"`, reserva saldo en `DimConsumo`, recalcula niveles y pasa al primer autorizador.
    * Sin saldo: `EstadoSolicitud = "RECHAZO-PRESUPUESTO"`, `DentroPresupuesto = "No"`, `ActorActual = "Solicitante"`.
  * `FechaModificacion` se actualiza. Mantiene el mismo `ID_Solicitud`.
  * Si permanece 15 días inactiva, el trigger diario la cancela automáticamente (`CANCELADO`).

##### Columnas de Control Actualizadas en `DimTransaccional` (Caso B):
| db_label | Valor asignado |
| :--- | :--- |
| `EstadoSolicitud` | `INICIADO` (si hay saldo) o `RECHAZO-PRESUPUESTO` (si no hay saldo) |
| `ActorActual` | Primer nivel autorizante asignado (o `Solicitante` si cae en falta de presupuesto) |
| `FechaModificacion` | Fecha y hora actual del guardado |
| `DentroPresupuesto` | `Si` o `No` según resultado de validación presupuestaria |
| `AutorizacionesPendientes` | Cantidad total de niveles requeridos por la nueva ruta |
| `DatosAutorizacion` | Array JSON reiniciado `[]` |
| `EsEditado` | `Si` si se modificó la información bancaria manualmente; `No` en caso contrario |

---

#### C. S2.1 con Estado: `RECHAZO-PROVISION 2`
* **Flujo**: Compras dictaminó *"Rechazo por información faltante"*. El saldo y las firmas aprobadas se conservan intactos.
* **Estructura Visual**:
  * **Información del solicitante**: Modo solo lectura.
  * **Detalle del viático**: Editable y precargado para complementar observaciones.
  * **Tabla informativa "Información de provisión de pago"** (lectura) con: `NombreProvision`, `FechaProvision` y `ComentarioProvision`.
  * **Campos editables inferiores**: No lleva campos adicionales.
* **Botones**: `[ Regresar ]` y `[ Guardar solicitud ]`.
* **Lógica al Guardar**:
  * **No** pasa por presupuesto ni por rutas autorizantes.
  * `EstadoSolicitud` pasa directamente a **`AUTORIZADO`**.
  * `ActorActual` pasa a **`Compras`**.
  * `FechaModificacion` se actualiza y se notifica por correo a Compras.
  * Si permanece 15 días inactiva, se cancela automáticamente (`CANCELADO`) y se libera el presupuesto retenido.

##### Columnas de Control Actualizadas en `DimTransaccional` (Caso C):
| db_label | Valor asignado |
| :--- | :--- |
| `EstadoSolicitud` | `AUTORIZADO` |
| `ActorActual` | `Compras` |
| `FechaModificacion` | Fecha y hora actual del guardado |
| `EsEditado` | `Si` si editó información bancaria manualmente; mantiene su valor previo en caso contrario |

---

#### D. S2.1 con Estado: `RECHAZO-PAGO 1`
* **Flujo**: Tesorería dictaminó *"Rechazo hacia solicitante"*. El saldo y las firmas aprobadas se conservan intactos.
* **Estructura Visual**:
  * **Información del solicitante**: Modo solo lectura.
  * **Detalle del viático**: Editable y precargado.
  * **Tabla informativa "Información de procesamiento de pago"** (lectura) con: `NombreProcesamiento`, `FechaProcesamiento` y `ComentarioProcesamiento`.
  * **Campos editables inferiores**: No lleva campos adicionales.
* **Botones**: `[ Regresar ]` y `[ Guardar solicitud ]`.
* **Lógica al Guardar**:
  * Se **borran/limpian obligatoriamente** los contenidos previos de provisión en `DimTransaccional`: `ResolucionProvision = ""`, `ComentarioProvision = ""`, `FechaProvision = ""`, `NombreProvision = ""`, `AgrupableProvision = ""`.
  * `EstadoSolicitud` pasa a **`AUTORIZADO`**.
  * `ActorActual` pasa a **`Compras`** (para generar un nuevo asiento contable de provisión limpio).
  * `FechaModificacion` se actualiza y se notifica a Compras.
  * Si permanece 15 días inactiva, se cancela automáticamente (`CANCELADO`) y se libera el presupuesto retenido.

##### Columnas de Control Actualizadas en `DimTransaccional` (Caso D):
| db_label | Valor asignado |
| :--- | :--- |
| `EstadoSolicitud` | `AUTORIZADO` |
| `ActorActual` | `Compras` |
| `FechaModificacion` | Fecha y hora actual del guardado |
| `ResolucionProvision` | `""` (vaciado / reseteado) |
| `ComentarioProvision` | `""` (vaciado / reseteado) |
| `FechaProvision` | `""` (vaciado / reseteado) |
| `NombreProvision` | `""` (vaciado / reseteado) |
| `AgrupableProvision` | `""` (vaciado / reseteado) |
| `EsEditado` | `Si` si editó información bancaria; en caso contrario mantiene su valor previo |

---

#### E. S2.1 con Estado: `RECHAZO-CIERRE`
* **Flujo**: Compras rechazó la liquidación de viáticos en E3.1.
* **Estructura Visual**:
  * **Información del solicitante**, **Detalle del viático** e **Información de solicitud**: **Modo solo lectura inmutable** (el dinero ya fue pagado).
  * **Tabla informativa "Información de cierre de solicitud"** (lectura) con: `NombreCierreE`, `FechaCierreE` y `ComentarioCierreE`.
  * **Sección editable inferior "Acciones de cierre"**: Mismos campos que en S3.1 / E3.1:
    * `TipoCierre`: Dropdown obligatorio (`Solo cierre` / `Reintegro y cierre`).
    * `ArchivosAdjuntos`: Subida obligatoria de nuevos comprobantes.
    * `MontoReintegro`: Numérico obligatorio si `TipoCierre == "Reintegro y cierre"`.
    * `FechaReintegro`: Fecha obligatoria si `TipoCierre == "Reintegro y cierre"`.
* **Botones**: `[ Regresar ]` y `[ Guardar ]`.
* **Lógica al Guardar**:
  * `EstadoSolicitud` pasa a **`LIQUIDADO`**.
  * `ActorActual` pasa a **`Compras`**.
  * `FechaCierreS` y `FechaModificacion` se actualizan.
  * Se notifica a Compras.
  * **Regla de 15 días**: Esta solicitud **nunca se cancela automáticamente**; si supera 15 días de inactividad, bloquea la creación de nuevas solicitudes en S1 para el solicitante.

##### Columnas de Control Actualizadas en `DimTransaccional` (Caso E):
| db_label | Valor asignado |
| :--- | :--- |
| `EstadoSolicitud` | `LIQUIDADO` |
| `ActorActual` | `Compras` |
| `FechaCierreS` | Fecha y hora actual del reenvío (`DD/MM/YYYY HH:mm`) |
| `FechaModificacion` | Fecha y hora actual del guardado |
| `ArchivosAdjuntos` | Array JSON actualizado con los nuevos archivos de liquidación |

---

### S3 — Cierre de Solicitudes (Bandeja Solicitante)

#### Referencia Visual de Diseño (UI & UX)
* **Plantilla Base**: `Diseño UI/Solicitantes/S3 Cierre de solicitudes.html`.

#### Flujo Operativo y Contexto
El solicitante ingresa a **Cierre de solicitudes** para rendir cuentas de anticipos que le han sido desembolsados. En esta bandeja se visualizan únicamente sus solicitudes en estado **`PAGADO`**.

#### Interfaz de Usuario (UI & UX)
* **Filtros**: ID Solicitud, Fechas (por `FechaSolicitud` en formato `DD/MM/YYYY`), Tipo de viático, Clasificación solicitud y Centro de Costo.
  > **Regla**: Se elimina el filtro y la columna de solicitante por ser la bandeja personal del colaborador.
* **Botón "Limpiar filtros"**: Ubicado a la derecha de la barra de filtros.
* **Paginación**: Selector de 10 (default), 20 y 30 registros por página.
* **Columna ACCIONES**: Botón interactivo **`[ Ver detalles ]`** para ingresar a S3.1.

#### Diccionario de Columnas de la Tabla S3:

| column_label | db_label | db_label2 | Regla de Visualización |
| :--- | :--- | :--- | :--- |
| ID SOLICITUD | `ID_Solicitud` | | Correlativo |
| FECHAS | `FechaSolicitud` | `FechaModificacion` | Formato `DD/MM/YYYY` |
| TIPO DE VIÁTICO | `TipoViatico` | | Texto de catálogo |
| MONTO | `Monto` | | Formato `$XX.XX USD` (etiqueta del header `"Monto"`) |
| ESTADO SOLICITUD | `EstadoSolicitud` | | Badge `PAGADO` |
| ACTOR ACTUAL | `ActorActual` | | `"Solicitante"` |
| CLASIFICACION SOLICITUD | `ClasificacionSolicitud` | | `"Anticipo"` |
| ACCIONES | | | Botón `[ Ver detalles ]` |

---

### S3.1 — Cierre de Solicitud (Liquidación de Viático)

#### Referencia Visual de Diseño (UI & UX)
* **Plantilla Base**: `Diseño UI/Solicitantes/S3.1 Cierre de solicitud.html`.

#### Flujo Operativo y Contexto
Al entrar desde S3, el solicitante visualiza las secciones de lectura:
1. **Datos del solicitante** (Lectura).
2. **Detalle del viático** (Lectura).
3. **Información de solicitud** (Lectura): ID Solicitud, Fecha creación, Rubro contable, Clasificación solicitud, ¿Información editada? (`EsEditado`), Archivos adjuntos.
4. **Información autorización** (Lectura): Historial de firmas desde `DatosAutorizacion`.
5. **Información de provisión de pago** (Lectura): `NombreProvision`, `FechaProvision`, `ComentarioProvision`.
6. **Información de procesamiento de pago** (Lectura): `NombreProcesamiento`, `FechaProcesamiento`, `ComentarioProcesamiento`.

#### Barra Dinámica de Botones:
* **Estado inicial**: `[ Regresar ]`, `[ Imprimir ]` y `[ Responder ]`.
* **Al pulsar `[ Responder ]`**: Se habilita la sección editable **"Acciones de cierre"** y la barra de botones cambia a: `[ Regresar ]` y `[ Guardar ]`.

#### Diccionario de Campos de Lectura (S3.1):

| app_label | db_label | Origen |
| :--- | :--- | :--- |
| ID Solicitud | `ID_Solicitud` | `DimTransaccional` |
| Fecha creación | `FechaSolicitud` | `DimTransaccional` |
| Rubro contable | `RubroContable` | `DimTransaccional` |
| Clasificación solicitud | `ClasificacionSolicitud` | `DimTransaccional` |
| ¿Información editada? | `EsEditado` | `DimTransaccional` |
| Archivos adjuntos | `ArchivosAdjuntos` | `DimTransaccional` |
| Tabla "Información autorización" | `DatosAutorizacion` | `DimTransaccional` (JSON) |
| Tabla "Información provisión de pago" | `NombreProvision`, `FechaProvision`, `ComentarioProvision` | `DimTransaccional` |
| Tabla "Información procesamiento de pago" | `NombreProcesamiento`, `FechaProcesamiento`, `ComentarioProcesamiento` | `DimTransaccional` |

#### Diccionario de Campos de Formulario (Acciones de Cierre):

| app_label | db_label | Tipo / Elemento | Obligatorio |
| :--- | :--- | :--- | :--- |
| Tipo de cierre de solicitud | `TipoCierre` | Dropdown (`Solo cierre`, `Reintegro y cierre`) | Sí |
| Agregar archivo | `ArchivosAdjuntos` | File uploader | Sí |
| Monto a reintegrar | `MontoReintegro` | Numérico (2 decimales) | Depende (`Reintegro y cierre`) |
| Fecha de reintegro | `FechaReintegro` | Fecha (`DD/MM/YYYY`) | Depende (`Reintegro y cierre`) |

#### Lógica de Negocio al Guardar:
* `EstadoSolicitud` pasa a **`LIQUIDADO`**.
* `ActorActual` pasa a **`Compras`**.
* `FechaCierreS` registra la fecha y hora actual (`dd/mm/aaaa hh:mm`).
* `FechaModificacion` se actualiza con la fecha y hora actual.
* Se despliega pop-up modal corporativo de confirmación de cierre.

---

### A1 — Autorización de Solicitudes (Bandeja Autorizador)

#### Referencia Visual de Diseño (UI & UX)
* **Plantilla Base**: `Diseño UI/Autorizadores/A1 Autorizacion de Solicitudes.html`.

#### Flujo Operativo y Contexto
El usuario con rol **`AUTORIZADOR`** ingresa a **Autorizadores >> Autorización de Solicitudes**. Visualiza exclusivamente las solicitudes pendientes donde él es el autorizador en turno (`ActorActual` coincide con su nivel autorizante o correo).

#### Estados Visibles en A1:
* **`INICIADO`**: Solicitud dentro de presupuesto.
* **`RECHAZO-PRESUPUESTO`**: Solicitud fuera de presupuesto con justificación enviada.

#### Interfaz de Usuario (UI & UX):
* **Filtros**: ID Solicitud, Rango de Fechas (por `FechaSolicitud` en formato `DD/MM/YYYY`), Solicitante, Tipo de Viático, Monto y Centro de Costo / Gerencia.
* **Botón "Limpiar filtros"**: Ubicado a la derecha de la barra de filtros.
* **Paginación**: Selector de 10 (default), 20 y 30 registros por página.
* **Columna SOLICITANTE**: Debe mostrar **únicamente el nombre completo** del solicitante (no concatenar plaza/cargo).
* **Columna ACCIONES**: Botón interactivo **`[ Ver detalles ]`**.

#### Diccionario de Columnas de la Tabla A1:

| column_label | db_label | db_label2 | Regla de Visualización |
| :--- | :--- | :--- | :--- |
| ID SOLICITUD | `ID_Solicitud` | | Correlativo |
| SOLICITANTE | `NombreSolicitante` | | Nombre del colaborador |
| GERENCIA | `Gerencia` | | Gerencia del solicitante |
| MONTO | `Monto` | | Formato `$XX.XX USD` |
| FECHAS | `FechaSolicitud` | `FechaModificacion` | Formato `DD/MM/YYYY` |
| TIPO DE VIÁTICO | `TipoViatico` | | Texto del catálogo |
| ESTADO PRESUPUESTO | `DentroPresupuesto` | | Badge (`Si` / `No`) |
| ACCIONES | | | Botón `[ Ver detalles ]` |

---

### A1.1 — Detalle y Resolución de Autorización

#### Referencia Visual de Diseño (UI & UX)
* **Plantilla Base**: `Diseño UI/Autorizadores/A1.1 Autorizacion de Solicitud.html`.

#### Flujo Operativo y Vías de Acceso
Se puede ingresar mediante dos vías:
1. Desde la Web App pulsando `[ Ver detalles ]` en A1.
2. Desde el correo electrónico interactivo pulsando el botón **`[ Revisar Solicitud ]`** (Deep Link: `${WebAppURL}?view=a1_1&id=SOL-XXX`).

#### Interfaz de Usuario (UI & UX)
1. **Información del Solicitante** (Lectura):
   * `Nombre`, `Correo institucional`, `Cargo / Plaza`, `Gerencia`, `Centro de Costo`, `Agencia`.
2. **Detalle del Viático** (Lectura):
   * `Duración de la actividad`, `Fecha inicio`, `Fecha fin`, `Tipo de viático`, `Hora del evento`, `Tipo de solicitud`, `Detalle bancario` (`Destinatario`, `Monto`, `Banco`, `Tipo de cuenta`, `No. de cuenta`), `Motivo del viático`, `Archivos Adjuntos`.
3. **Información de Presupuesto y Justificación** (Lectura):
   * Badge visual `✓ Dentro de Presupuesto` (verde) / `⚠ Fuera de Presupuesto` (rojo).
   * Campo *Justificación de viático fuera de presupuesto* (`JustificacionPresupuesto`) visible si `DentroPresupuesto == "No"`.
4. **Información autorización** (Lectura): Tabla con el historial de firmas acumuladas de `DatosAutorizacion`.
5. **Sección "Acciones de Autorización"** (Campos Editables):
   * **Resolución de Autorización**: Selector (`Aprobado`, `Rechazado`).
   * **Comentario**: Área de texto. **Opcional** al Aprobar; **Obligatorio** al Rechazar.
6. **Botones de Acción**:
   * **`[ Regresar ]`**: Vuelve a la bandeja A1.
   * **`[ Guardar ]`** / **`[ Confirmar Decisión ]`**: Ejecuta la resolución mostrando un pop-up modal corporativo de confirmación de autorización (sin pop-ups nativos `alert`).

#### Diccionario de Campos de Lectura (A1.1):

| app_label | db_label | Origen |
| :--- | :--- | :--- |
| Nombre | `NombreSolicitante` | `DimUsuarios` / `DimTransaccional` |
| Correo institucional | `CorreoSolicitante` | `DimUsuarios` / `DimTransaccional` |
| Cargo / Plaza | `CargoSolicitante` | `DimUsuarios` / `DimTransaccional` |
| Gerencia | `Gerencia` | `DimUsuarios` / `DimTransaccional` |
| Centro de Costo | `CentroCosto` | `DimUsuarios` / `DimTransaccional` |
| Agencia | `Agencia` | `DimUsuarios` / `DimTransaccional` |
| Duración de la actividad | `DuracionActividad` | `DimTransaccional` |
| Fecha Inicio | `FechaInicio` | `DimTransaccional` |
| Fecha Fin | `FechaFin` | `DimTransaccional` |
| Tipo de viático | `TipoViatico` | `DimTransaccional` |
| Hora del evento | `HoraEvento` | `DimTransaccional` |
| Tipo de solicitud | `TipoSolicitud` | `DimTransaccional` |
| Destinatario | `Destinatario` | `DimTransaccional` |
| Monto | `Monto` | `DimTransaccional` |
| Banco | `Banco` | `DimTransaccional` |
| Tipo de cuenta | `TipoCuenta` | `DimTransaccional` |
| No. de cuenta | `NumeroCuenta` | `DimTransaccional` |
| Motivo del viático | `MotivoViatico` | `DimTransaccional` |
| Archivos Adjuntos | `ArchivosAdjuntos` | `DimTransaccional` |
| Estado del presupuesto | `DentroPresupuesto` | `DimTransaccional` |
| Justificación fuera de presupuesto | `JustificacionPresupuesto` | `DimTransaccional` |
| Historial de firmas | `DatosAutorizacion` | `DimTransaccional` (JSON) |

#### Diccionario de Campos de Formulario (Acciones de Autorización):

| app_label | Destino en Base de Datos | Tipo / Regla |
| :--- | :--- | :--- |
| Resolución de Autorización | Actualiza `EstadoSolicitud`, `AutorizacionesPendientes`, `ActorActual` y `DatosAutorizacion` | Selector (`Aprobado`, `Rechazado`) - Obligatorio |
| Comentario | Se integra dentro del objeto JSON en `DatosAutorizacion` | Textarea - Opcional al Aprobar / Obligatorio al Rechazar |

#### Lógica de Negocio:
* **Al Aprobar**:
  * Se registra la firma en `DatosAutorizacion`.
  * `AutorizacionesPendientes = AutorizacionesPendientes - 1`.
  * Si $\text{AutorizacionesPendientes} > 0$: Se asigna `ActorActual` al siguiente nivel y se le despacha correo.
  * Si $\text{AutorizacionesPendientes} == 0$: `EstadoSolicitud = "AUTORIZADO"`, `ActorActual = "Compras"` y se notifica a Compras.
* **Al Rechazar**:
  * Se registra el rechazo en `DatosAutorizacion`.
  * `EstadoSolicitud = "RECHAZO-AUTORIZACION"`, `ActorActual = ""`.
  * Se libera el presupuesto reservado en `DimDisponible` / `DimConsumo` y se notifica al solicitante.
* **Control de Concurrencia**: Si la solicitud ya fue resuelta, la pantalla se bloquea impidiendo votos duplicados.

---

### E1 — Provisión de Pagos (Bandeja Compras)

#### Referencia Visual de Diseño (UI & UX)
* **Plantilla Base**: `Diseño UI/Editores/E1 Provision de pagos.html`.

#### Flujo Operativo y Contexto
El usuario con rol **`EDITOR-COMPRAS`** ingresa a **Operaciones >> Provisión de pagos**. Visualiza solicitudes autorizadas pendientes de provisión contable.

#### Estados Visibles en E1:
* `AUTORIZADO`
* `RECHAZO-PAGO 2`

#### Interfaz de Usuario y Agrupación:
* **Filtros**: ID Solicitud, Fechas (por `FechaSolicitud`), Solicitante, Tipo de viático, Clasificación solicitud y Código CC.
* **Botón "Agrupar"**: Ubicado a la misma altura del título de la página hacia la derecha.
* **Botón "Limpiar filtros"**: Ubicado a la derecha del botón "Agrupar".
* **Paginación**: Selector inferior de 10 (default), 20 y 30 registros por página.
* **Checkbox de Agrupación**: Aparece a la par de `[ Ver detalles ]` **únicamente** en aquellas solicitudes que tengan `ResolucionProvision == "Aprobado"`.
* **Modal de Agrupación Contable**: Al pulsar *"Agrupar"*, se despliega un pop-up modal con los campos del asiento contable:
  * **Fecha contable** (Formato `DD/MM/YYYY`, Obligatorio).
  * **Fecha valor** (Formato `DD/MM/YYYY`, Obligatorio).
  * **Módulo** (Obligatorio).
  * **Transacción** (Obligatorio).
  * **Código de relación** (Obligatorio).
  * **CR / FSE** (Opcional).
  * **Agregar archivo** (Obligatorio, se añade en modo *append* a `ArchivosAdjuntos`).
* **Lógica al Guardar Agrupación**:
  * Los datos contables se guardan como JSON en `AgrupableProvision`.
  * `EstadoSolicitud` pasa a **`ENVIADO A PAGO`**.
  * `ActorActual` pasa a **`Tesorería`**.
  * `FechaProvision` y `NombreProvision` se registran.
  * `FechaModificacion` se actualiza.

#### Diccionario de Columnas de la Tabla E1:

| column_label | db_label | db_label2 | Regla de Visualización |
| :--- | :--- | :--- | :--- |
| ID SOLICITUD | `ID_Solicitud` | | Correlativo |
| SOLICITANTE | `NombreSolicitante` | | Nombre del colaborador |
| MONTO | `Monto` | | Formato `$XX.XX USD` |
| CODIGO CC | `CentroCosto` | | Prefijo numérico (ej. `510`) |
| FECHAS | `FechaSolicitud` | `FechaModificacion` | Formato `DD/MM/YYYY` |
| ESTADO SOLICITUD | `EstadoSolicitud` | | Badge de estado |
| TIPO DE VIATICO | `TipoViatico` | | Texto del catálogo |
| CLASIFICACION SOLICITUD | `ClasificacionSolicitud` | | `"Anticipo"` o `"Reintegro"` |
| ACCIONES | | | Checkbox + Botón `[ Ver detalles ]` |

---

### E1.1 — Detalle de Provisión de Pago

#### Referencia Visual de Diseño (UI & UX)
* **Plantilla Base**: `Diseño UI/Editores/E1.1 Provision de pago.html`.

#### Flujo Operativo y Contexto
Al entrar desde E1, el analista de Compras visualiza:
1. **Datos del solicitante** (Lectura).
2. **Detalle del viático** (Lectura, datos bancarios bloqueados).
3. **Información de solicitud** (Lectura): ID Solicitud, Fecha creación, Rubro contable, Clasificación solicitud, ¿Información editada? (`EsEditado` con badge `⚠ Modificado manualmente` o `Normal`), Archivos adjuntos.
4. **Información autorización** (Lectura): Historial de firmas desde `DatosAutorizacion`.
5. **Información procesamiento de pago** (Lectura): Visible si la solicitud viene de `RECHAZO-PAGO 2` (`NombreProcesamiento`, `FechaProcesamiento`, `ComentarioProcesamiento`).

#### Barra Dinámica de Botones:
* **Estado inicial**: `[ Regresar ]`, `[ Imprimir ]` y `[ Responder ]`.
* **Al pulsar `[ Responder ]`**: Se habilita la sección editable **"Acciones de provisión"** y la barra de botones cambia a: `[ Regresar ]` y `[ Guardar ]`.

#### Diccionario de Campos de Lectura (E1.1):

| app_label | db_label | Origen |
| :--- | :--- | :--- |
| ID Solicitud | `ID_Solicitud` | `DimTransaccional` |
| Fecha creación | `FechaSolicitud` | `DimTransaccional` |
| Rubro contable | `RubroContable` | `DimTransaccional` |
| Clasificación solicitud | `ClasificacionSolicitud` | `DimTransaccional` |
| ¿Información editada? | `EsEditado` | `DimTransaccional` |
| Archivos adjuntos | `ArchivosAdjuntos` | `DimTransaccional` |
| Tabla "Información autorización" | `DatosAutorizacion` | `DimTransaccional` (JSON) |
| Tabla "Información procesamiento de pago" | `NombreProcesamiento`, `FechaProcesamiento`, `ComentarioProcesamiento` | `DimTransaccional` (visible en `RECHAZO-PAGO 2`) |

#### Diccionario de Campos de Formulario (Acciones de Provisión):

| app_label | db_label | Tipo / Elemento | Obligatorio |
| :--- | :--- | :--- | :--- |
| Resolución de provisión | `ResolucionProvision` | Dropdown (`Aprobado`, `Rechazo y requiere reevaluación`, `Rechazo por información faltante`) | Sí |
| Comentario | `ComentarioProvision` | Textarea | Obligatorio si no es `Aprobado` |

#### Lógica al Guardar:
* Si es `Aprobado`: No se alteran `EstadoSolicitud`, `ActorActual` ni `FechaModificacion` (se mantiene en `AUTORIZADO` para permitir su posterior agrupación y emisión de lote en E1).
* Si es `Rechazo y requiere reevaluación`: `EstadoSolicitud = "RECHAZO-PROVISION 1"`, `ActorActual = "Solicitante"`, libera el presupuesto en `DimDisponible` y actualiza `FechaProvision` y `NombreProvision`.
* Si es `Rechazo por información faltante`: `EstadoSolicitud = "RECHAZO-PROVISION 2"`, `ActorActual = "Solicitante"`, conserva el presupuesto reservado y actualiza `FechaProvision` y `NombreProvision`.

---

### E2 — Procesamiento de Pagos (Bandeja Tesorería)

#### Referencia Visual de Diseño (UI & UX)
* **Plantilla Base**: `Diseño UI/Editores/E2 Procesamiento de pagos.html`.

#### Flujo Operativo y Contexto
El usuario con rol **`EDITOR-TESORERIA`** ingresa a **Operaciones >> Procesamiento de pagos**. Visualiza solicitudes aprobadas en provisión (`EstadoSolicitud == "ENVIADO A PAGO"`).

#### Interfaz de Usuario y Agrupación:
* **Filtros**: ID Solicitud, Fechas (por `FechaSolicitud`), Solicitante, Tipo de viático, Clasificación solicitud y Código CC.
* **Botón "Agrupar"**: Ubicado a la misma altura del título de la página hacia la derecha.
* **Botón "Limpiar filtros"**: Ubicado a la derecha del botón "Agrupar".
* **Checkbox de Agrupación**: Aparece a la par de `[ Ver detalles ]` **únicamente** en aquellas solicitudes que tengan `ResolucionProcesamiento == "Aprobado"`.
* **Modal de Agrupación Contable**: Abre el modal contable (Fecha contable, Fecha valor, Módulo, Transacción, Código de relación, CR / FSE, Agregar comprobante de transferencia bancaria).
* **Lógica al Guardar Agrupación**:
  * Los datos contables se guardan como JSON en `AgrupableProcesamiento`.
  * `FechaProcesamiento` y `NombreProcesamiento` se registran.
  * `FechaModificacion` se actualiza.
  * **Transición según Clasificación**:
    * Si `ClasificacionSolicitud == "Anticipo"`: `EstadoSolicitud` pasa a **`PAGADO`** y `ActorActual` pasa a **`Solicitante`** (iniciando el control de 15 días para liquidación).
    * Si `ClasificacionSolicitud == "Reintegro"`: `EstadoSolicitud` pasa a **`FINALIZADO`** y `ActorActual` queda vacío `""`.

#### Diccionario de Columnas de la Tabla E2:

| column_label | db_label | db_label2 | Regla de Visualización |
| :--- | :--- | :--- | :--- |
| ID SOLICITUD | `ID_Solicitud` | | Correlativo |
| SOLICITANTE | `NombreSolicitante` | | Nombre del colaborador |
| MONTO | `Monto` | | Formato `$XX.XX USD` |
| CODIGO CC | `CentroCosto` | | Prefijo numérico (ej. `510`) |
| FECHAS | `FechaSolicitud` | `FechaModificacion` | Formato `DD/MM/YYYY` |
| ESTADO SOLICITUD | `EstadoSolicitud` | | Badge `ENVIADO A PAGO` |
| TIPO DE VIATICO | `TipoViatico` | | Texto del catálogo |
| CLASIFICACION SOLICITUD | `ClasificacionSolicitud` | | `"Anticipo"` o `"Reintegro"` |
| ACCIONES | | | Checkbox + Botón `[ Ver detalles ]` |

---

### E2.1 — Detalle de Procesamiento de Pago

#### Referencia Visual de Diseño (UI & UX)
* **Plantilla Base**: `Diseño UI/Editores/E2.1 Procesamiento de pago.html`.

#### Flujo Operativo y Contexto
Al entrar desde E2, el analista de Tesorería visualiza:
1. **Datos del solicitante** y **Detalle del viático** (Lectura).
2. **Información de solicitud** (Lectura): ID Solicitud, Fecha creación, Rubro contable, Clasificación solicitud, ¿Información editada? (`EsEditado`), Archivos adjuntos y los datos del asiento contable de provisión extraídos de `AgrupableProvision`.
3. **Información autorización** (Lectura): Historial de firmas.
4. **Información de provisión** (Lectura): `NombreProvision`, `FechaProvision`, `ComentarioProvision`.

#### Barra Dinámica de Botones:
* **Estado inicial**: `[ Regresar ]`, `[ Imprimir ]` y `[ Responder ]`.
* **Al pulsar `[ Responder ]`**: Se habilita la sección editable **"Acciones de procesamiento"** y la barra de botones cambia a: `[ Regresar ]` y `[ Guardar ]`.

#### Diccionario de Campos de Lectura (E2.1):

| app_label | db_label | Origen |
| :--- | :--- | :--- |
| ID Solicitud | `ID_Solicitud` | `DimTransaccional` |
| Fecha creación | `FechaSolicitud` | `DimTransaccional` |
| Rubro contable | `RubroContable` | `DimTransaccional` |
| Clasificación solicitud | `ClasificacionSolicitud` | `DimTransaccional` |
| ¿Información editada? | `EsEditado` | `DimTransaccional` |
| Archivos adjuntos | `ArchivosAdjuntos` | `DimTransaccional` |
| Fecha contable (Provisión) | `FechaContable` | `AgrupableProvision` (JSON) |
| Fecha valor (Provisión) | `FechaValor` | `AgrupableProvision` (JSON) |
| Módulo (Provisión) | `Modulo` | `AgrupableProvision` (JSON) |
| Transacción (Provisión) | `Transaccion` | `AgrupableProvision` (JSON) |
| Código de relación (Provisión) | `CodigoRelacion` | `AgrupableProvision` (JSON) |
| CR / FSE (Provisión) | `CR_FSE` | `AgrupableProvision` (JSON) |
| Tabla "Información autorización" | `DatosAutorizacion` | `DimTransaccional` (JSON) |
| Tabla "Información de provisión" | `NombreProvision`, `FechaProvision`, `ComentarioProvision` | `DimTransaccional` |

#### Diccionario de Campos de Formulario (Acciones de Procesamiento):

| app_label | db_label | Tipo / Elemento | Obligatorio |
| :--- | :--- | :--- | :--- |
| Resolución de procesamiento | `ResolucionProcesamiento` | Dropdown (`Aprobado`, `Rechazo hacia solicitante`, `Rechazo hacia compras`) | Sí |
| Comentario | `ComentarioProcesamiento` | Textarea | Obligatorio si no es `Aprobado` |

> [!NOTE]
> **Regla de Sobreescritura en E2.1**: Si la solicitud provenía de `RECHAZO-PAGO 2` y fue reevaluada por Compras en E1.1, al resolverse nuevamente en E2.1 los campos `NombreProcesamiento`, `FechaProcesamiento` y `ComentarioProcesamiento` se sobreescriben con la nueva resolución.

#### Lógica al Guardar:
* Si es `Aprobado`: No se alteran `EstadoSolicitud` ni `ActorActual` en este punto (se procesa al agrupar en E2).
* Si es `Rechazo hacia solicitante`: `EstadoSolicitud = "RECHAZO-PAGO 1"`, `ActorActual = "Solicitante"`, actualiza `FechaProcesamiento` y `NombreProcesamiento`.
* Si es `Rechazo hacia compras`: `EstadoSolicitud = "RECHAZO-PAGO 2"`, `ActorActual = "Compras"`, actualiza `FechaProcesamiento` y `NombreProcesamiento`.

---

### E3 — Cierre de Solicitudes (Bandeja Compras)

#### Referencia Visual de Diseño (UI & UX)
* **Plantilla Base**: `Diseño UI/Editores/E3 Cierre de solicitudes.html`.

#### Flujo Operativo y Contexto
El usuario con rol **`EDITOR-COMPRAS`** ingresa a **Operaciones >> Cierre de solicitudes**. Visualiza solicitudes liquidadas por solicitantes (`EstadoSolicitud == "LIQUIDADO"`).

#### Interfaz de Usuario y Agrupación:
* **Filtros**: ID Solicitud, Fechas (por `FechaSolicitud`), Solicitante, Tipo de viático, Clasificación solicitud y Código CC.
* **Botón "Agrupar"**: Ubicado a la misma altura del título de la página hacia la derecha.
* **Botón "Limpiar filtros"**: Ubicado a la derecha del botón "Agrupar".
* **Checkbox de Agrupación**: Aparece a la par de `[ Ver detalles ]` **únicamente** en aquellas solicitudes que cumplan simultáneamente:
  $$\text{ResolucionCierreE} == \text{"Aprobado"} \quad \text{Y} \quad \text{TipoCierre} == \text{"Reintegro y cierre"}$$
* **Modal de Agrupación Contable**: Abre el modal contable (Fecha contable, Fecha valor, Módulo, Transacción, Código de relación, CR / FSE, Agregar archivo de liquidación).
* **Lógica al Guardar Agrupación**:
  * Los datos contables se guardan como JSON en `AgrupableCierreE`.
  * `EstadoSolicitud` pasa a **`FINALIZADO`**.
  * `ActorActual` pasa a **`""`** (vacío).
  * `FechaCierreE`, `NombreCierreE` y `FechaModificacion` se actualizan.

#### Diccionario de Columnas de la Tabla E3:

| column_label | db_label | db_label2 | Regla de Visualización |
| :--- | :--- | :--- | :--- |
| ID SOLICITUD | `ID_Solicitud` | | Correlativo |
| SOLICITANTE | `NombreSolicitante` | | Nombre del colaborador |
| MONTO | `Monto` | | Formato `$XX.XX USD` |
| CODIGO CC | `CentroCosto` | | Prefijo numérico (ej. `510`) |
| FECHAS | `FechaSolicitud` | `FechaModificacion` | Formato `DD/MM/YYYY` |
| ESTADO SOLICITUD | `EstadoSolicitud` | | Badge `LIQUIDADO` |
| TIPO DE VIATICO | `TipoViatico` | | Texto del catálogo |
| CLASIFICACION SOLICITUD | `ClasificacionSolicitud` | | `"Anticipo"` |
| ACCIONES | | | Checkbox + Botón `[ Ver detalles ]` |

---

### E3.1 — Detalle y Auditoría de Cierre de Solicitudes

#### Referencia Visual de Diseño (UI & UX)
* **Plantilla Base**: `Diseño UI/Editores/E3.1 Cierre de solicitud.html`.

#### Flujo Operativo y Contexto
Al entrar desde E3, el analista de Compras audita la liquidación:
1. **Datos del solicitante**, **Detalle del viático** e **Información de solicitud** (Lectura).
2. **Información autorización** (Lectura).
3. **Información de provisión de pago** (Lectura).
4. **Información de procesamiento de pago** (Lectura).

#### Barra Dinámica de Botones:
* **Estado inicial**: `[ Regresar ]`, `[ Imprimir ]` y `[ Responder ]`.
* **Al pulsar `[ Responder ]`**: Se habilita la sección editable **"Acciones de cierre"** y la barra de botones cambia a: `[ Regresar ]` y `[ Guardar ]`.

#### Diccionario de Campos de Lectura (E3.1):

| app_label | db_label | Origen |
| :--- | :--- | :--- |
| ID Solicitud | `ID_Solicitud` | `DimTransaccional` |
| Fecha creación | `FechaSolicitud` | `DimTransaccional` |
| Rubro contable | `RubroContable` | `DimTransaccional` |
| Clasificación solicitud | `ClasificacionSolicitud` | `DimTransaccional` |
| Tipo de Cierre | `TipoCierre` | `DimTransaccional` |
| Monto a Reintegrar | `MontoReintegro` | `DimTransaccional` |
| Fecha de Reintegro | `FechaReintegro` | `DimTransaccional` |
| Fecha de Cierre (Solicitante) | `FechaCierreS` | `DimTransaccional` |
| ¿Información editada? | `EsEditado` | `DimTransaccional` |
| Archivos adjuntos | `ArchivosAdjuntos` | `DimTransaccional` |
| Tabla "Información autorización" | `DatosAutorizacion` | `DimTransaccional` (JSON) |
| Tabla "Información de provisión de pago" | `NombreProvision`, `FechaProvision`, `ComentarioProvision` | `DimTransaccional` |
| Tabla "Información de procesamiento de pago" | `NombreProcesamiento`, `FechaProcesamiento`, `ComentarioProcesamiento` | `DimTransaccional` |

#### Diccionario de Campos de Formulario (Acciones de Cierre Compras):

| app_label | db_label | Tipo / Elemento | Obligatorio |
| :--- | :--- | :--- | :--- |
| Resolución de cierre | `ResolucionCierreE` | Dropdown (`Aprobado`, `Rechazado`) | Sí |
| Comentario | `ComentarioCierreE` | Textarea | Obligatorio si es `Rechazado` |

#### Lógica al Guardar:
* Si la resolución es `Aprobado` y `TipoCierre == "Solo cierre"`: `EstadoSolicitud` pasa a **`FINALIZADO`**, `ActorActual = ""` y se actualiza `FechaModificacion`.
* Si la resolución es `Aprobado` y `TipoCierre == "Reintegro y cierre"`:
  * No se cambian `EstadoSolicitud` ni `ActorActual` en este punto (permanece en `LIQUIDADO` para ser agrupada en E3).
  * **Devolución Presupuestaria**: Se devuelve de inmediato el `MontoReintegro` sumándolo en `DimDisponible` y restándolo en `DimConsumo` para el mes de `FechaCierreE`.
* Si la resolución es `Rechazado`: `EstadoSolicitud = "RECHAZO-CIERRE"`, `ActorActual = "Solicitante"`, `FechaCierreE` y `NombreCierreE` se registran, y `FechaModificacion` se actualiza.

---

### Solicitudes en curso

#### Referencia Visual de Diseño (UI & UX)
* **Bandeja Principal**: `Diseño UI/Solicitudes en curso.html`.
* **Vista de Detalle**: `Diseño UI/Detalles de solicitud (Solicitud en curso).html`.

#### Flujo Operativo y Contexto
Accesible para todos los roles (**`SOLICITANTE`**, **`EDITOR-COMPRAS`**, **`EDITOR-TESORERIA`**, **`AUTORIZADOR`**, **`ADMINISTRADOR`**). Funciona como el centro de monitoreo de solicitudes activas.

#### Alcance de Visibilidad por Rol (Filtro Fijo de Seguridad):
* **`SOLICITANTE`** y **`AUTORIZADOR`**: Poseen un filtro automático en segundo plano que restringe la tabla para que **únicamente visualicen sus propias solicitudes** (`CorreoSolicitante == UsuarioLogueado`).
* **`EDITOR-COMPRAS`**, **`EDITOR-TESORERIA`** y **`ADMINISTRADOR`**: Tienen visibilidad global para consultar solicitudes de cualquier colaborador a nivel institucional.

#### Estados Visibles:
Incluye **todos los estados en trámite**, excluyendo estrictamente los terminales (`FINALIZADO`, `CANCELADO`, `RECHAZO-AUTORIZACION`):
* `INICIADO`
* `RECHAZO-PRESUPUESTO`
* `AUTORIZADO`
* `ENVIADO A PAGO`
* `RECHAZO-PROVISION 1`
* `RECHAZO-PROVISION 2`
* `PAGADO`
* `RECHAZO-PAGO 1`
* `RECHAZO-PAGO 2`
* `LIQUIDADO`
* `RECHAZO-CIERRE`

#### Interfaz de Usuario y Filtros:
* **Filtros Disponibles**: ID Solicitud, Rango de Fechas (por `FechaSolicitud` en formato `DD/MM/YYYY`), Solicitante (fijo/oculto para Solicitantes y Autorizadores), Estado Solicitud, Actor Actual, Tipo de Viático, Clasificación (`Anticipo` / `Reintegro`) y Centro de Costo / Gerencia.
  > **Regla**: Se elimina la columna y el filtro `"TIPO"`.
* **Botón "Limpiar filtros"** y selector de paginación (10, 20, 30).
* **Columna ACCIONES**: Botón interactivo **`[ Ver detalles ]`**.

#### Vista de Detalle (Expediente Progresivo Acumulativo):
Al pulsar `[ Ver detalles ]`, se despliega una vista integral que sigue la estructura y diseño de **S3.1** con renderizado condicional progresivo de las siguientes secciones:
1. **Información del Solicitante** (Lectura): Nombre, Correo, Cargo, Gerencia, Centro de Costo, Agencia.
2. **Detalle del Viático** (Lectura): Duración, Fechas, Tipo de Viático, Franja Horaria, Tipo de Solicitud, Destinatario, Monto, Motivo y Detalle Bancario con badge `¿Información editada?` (`EsEditado`).
3. **Información de la Solicitud** (Lectura): ID Solicitud, Fecha Creación, Rubro Contable, Clasificación Solicitud, Estado Actual, Actor Actual y lista/enlaces a todos los **Archivos Adjuntos**.
4. **Información de Presupuesto y Justificación** (Lectura): Badge `✓ Dentro de Presupuesto` / `⚠ Fuera de Presupuesto` y justificación fuera de presupuesto (si aplicó).
5. **Tabla "Información autorización"** (Lectura): Historial de firmas de `DatosAutorizacion`.
6. **Tabla "Información provisión de pagos"** (Lectura): Datos de revisión de Compras (`NombreProvision`, `FechaProvision`, `ResolucionProvision`, `ComentarioProvision`) y Asiento Contable extraído de `AgrupableProvision` (si pasó por E1).
7. **Tabla "Información procesamiento de pagos"** (Lectura): Datos de pago de Tesorería (`NombreProcesamiento`, `FechaProcesamiento`, `ResolucionProcesamiento`, `ComentarioProcesamiento`) y Asiento Contable extraído de `AgrupableProcesamiento` (si pasó por E2).
8. **Tabla "Información Cierre (Solicitante)"** (Lectura): Modalidad de cierre (`TipoCierre`), Monto devuelto (`MontoReintegro`), Fecha de depósito (`FechaReintegro`), Fecha de envío (`FechaCierreS`) y comprobantes/facturas de liquidación adjuntos.
9. **Tabla "Información Cierre (Compras)"** (Lectura): Dictamen de Compras (`NombreCierreE`, `FechaCierreE`, `ResolucionCierreE`, `ComentarioCierreE`) y Asiento Contable extraído de `AgrupableCierreE` (si aplicó reintegro y fue agrupado en E3).

#### Diccionario de Columnas de la Tabla Principal:

| column_label | db_label | db_label2 | Regla de Visualización |
| :--- | :--- | :--- | :--- |
| ID SOLICITUD | `ID_Solicitud` | | Correlativo |
| SOLICITANTE | `NombreSolicitante` | | Nombre del colaborador |
| MONTO | `Monto` | | Formato `$XX.XX USD` |
| CODIGO CC | `CentroCosto` | | Prefijo numérico (ej. `510`) |
| FECHAS | `FechaSolicitud` | `FechaModificacion` | Formato `DD/MM/YYYY` |
| ESTADO SOLICITUD | `EstadoSolicitud` | | Badge de estado actual |
| ACTOR ACTUAL | `ActorActual` | | Rol o usuario responsable |
| TIPO DE VIÁTICO | `TipoViatico` | | Texto del catálogo |
| CLASIFICACIÓN | `ClasificacionSolicitud` | | `"Anticipo"` o `"Reintegro"` |
| ACCIONES | | | Botón `[ Ver detalles ]` |

---

### Histórico

#### Referencia Visual de Diseño (UI & UX)
* **Bandeja Principal**: `Diseño UI/Historico.html`.
* **Vista de Detalle**: `Diseño UI/Detalles de solicitud (Historico).html`.

#### Flujo Operativo y Contexto
Accesible para todos los roles. Funciona como el **repositorio central inmutable de auditoría** para solicitudes que han concluido de forma definitiva su ciclo de vida.

#### Alcance de Visibilidad por Rol:
* **`SOLICITANTE`** y **`AUTORIZADOR`**: Visualizan exclusivamente sus solicitudes cerradas (`CorreoSolicitante == UsuarioLogueado`).
* **`EDITOR-COMPRAS`**, **`EDITOR-TESORERIA`** y **`ADMINISTRADOR`**: Visualizan el archivo histórico completo a nivel institucional.

#### Estados Visibles (Exclusivamente Terminales):
1. **`FINALIZADO`**: Reintegros pagados en E2 o Anticipos liquidados y aprobados en E3.
2. **`CANCELADO`**: Solicitudes pre-pago canceladas automáticamente por inactividad a los 15 días.
3. **`RECHAZO-AUTORIZACION`**: Solicitudes rechazadas por niveles autorizantes en A1.1.

#### Vista de Detalle (Expediente Histórico Final Auditado):
Sigue la misma estructura progresiva de Solicitudes en curso / S3.1, presentando la trazabilidad completa, inmutable y lista para impresión formal (**`[ Imprimir ]`**):
* **Para `RECHAZO-AUTORIZACION`**: Datos completos, justificación y registro de firma con el motivo de rechazo.
* **Para `CANCELADO`**: Datos completos y constancia de caducidad automática por 15 días con liberación de fondos.
* **Para `FINALIZADO` (Reintegro)**: Ciclo completo (Creación $\to$ Autorizaciones $\to$ Provisión E1 $\to$ Pago Tesorería E2).
* **Para `FINALIZADO` (Anticipo)**: Ciclo completo de 4 etapas (Creación $\to$ Autorizaciones $\to$ Provisión E1 $\to$ Pago Tesorería E2 $\to$ Liquidación Solicitante S3.1 $\to$ Cierre Compras E3).

#### Diccionario de Columnas de la Tabla Histórico:

| column_label | db_label | db_label2 | Regla de Visualización |
| :--- | :--- | :--- | :--- |
| ID SOLICITUD | `ID_Solicitud` | | Correlativo |
| SOLICITANTE | `NombreSolicitante` | | Nombre del colaborador |
| MONTO | `Monto` | | Formato `$XX.XX USD` |
| CODIGO CC | `CentroCosto` | | Prefijo numérico (ej. `510`) |
| FECHAS | `FechaSolicitud` | `FechaModificacion` | Formato `DD/MM/YYYY` |
| ESTADO TERMINAL | `EstadoSolicitud` | | Badge del estado terminal |
| TIPO DE VIÁTICO | `TipoViatico` | | Texto del catálogo |
| CLASIFICACIÓN | `ClasificacionSolicitud` | | `"Anticipo"` o `"Reintegro"` |
| ACCIONES | | | Botón `[ Ver detalles ]` |

