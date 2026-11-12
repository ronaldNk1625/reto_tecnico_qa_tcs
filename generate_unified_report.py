import os
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=110, bottom=110, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def style_table(table, col_widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        if i == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            for cell in row.cells:
                set_cell_background(cell, "002B49")
                set_cell_margins(cell, top=130, bottom=130, left=160, right=160)
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for run in p.runs:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)
                        run.font.size = Pt(9.5)
        else:
            bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
            for cell in row.cells:
                set_cell_background(cell, bg)
                set_cell_margins(cell, top=95, bottom=95, left=140, right=140)
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.font.size = Pt(9)
                        run.font.color.rgb = RGBColor(30, 41, 59)
        
        if col_widths:
            for c_idx, width in enumerate(col_widths):
                if c_idx < len(row.cells):
                    row.cells[c_idx].width = Inches(width)

doc = Document()

# Configuración de márgenes de página
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

COLOR_PRIMARY = RGBColor(0, 43, 73)      # #002B49 (Azul Pichincha)
COLOR_SECONDARY = RGBColor(0, 102, 178)  # Azul medio
COLOR_ACCENT = RGBColor(217, 119, 6)     # Ámbar
COLOR_SUCCESS = RGBColor(22, 163, 74)    # Verde
COLOR_DANGER = RGBColor(220, 38, 38)     # Rojo

# ==================== ENCABEZADO / PORTADA ====================
p_sup = doc.add_paragraph()
r_sup = p_sup.add_run("BANCO PICHINCHA / TCS (TATA CONSULTANCY SERVICES)")
r_sup.font.bold = True
r_sup.font.size = Pt(11)
r_sup.font.color.rgb = COLOR_SECONDARY

p_tit = doc.add_paragraph()
r_tit = p_tit.add_run("INFORME GENERAL CONSOLIDADO DE PRUEBAS TÉCNICAS\nQA AUTOMATION & PERFORMANCE")
r_tit.font.size = Pt(21)
r_tit.font.bold = True
r_tit.font.color.rgb = COLOR_PRIMARY

p_sub = doc.add_paragraph()
r_sub = p_sub.add_run("Documentación Unificada de Resultados: Automatización E2E, Automatización de APIs y Pruebas de Performance")
r_sub.font.size = Pt(12)
r_sub.font.italic = True
r_sub.font.color.rgb = RGBColor(100, 116, 139)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Tabla de Metadatos
meta_table = doc.add_table(rows=5, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Candidato Evaluado:", "Ronald Berrones"),
    ("Rol / Perfil:", "QA Automation & Performance Engineer"),
    ("Cliente / Entidad:", "Banco Pichincha / TCS"),
    ("Repositorio Oficial GitHub:", "https://github.com/ronaldNk1625/reto_tecnico_qa_tcs.git"),
    ("Fecha de Emisión:", "Noviembre 2026")
]
for idx, (k, v) in enumerate(meta_data):
    c0 = meta_table.cell(idx, 0)
    c1 = meta_table.cell(idx, 1)
    c0.text = k
    c1.text = v
    c0.paragraphs[0].runs[0].font.bold = True
    c0.paragraphs[0].runs[0].font.size = Pt(9.5)
    c1.paragraphs[0].runs[0].font.size = Pt(9.5)
style_table(meta_table, [2.3, 4.4])

doc.add_paragraph().paragraph_format.space_after = Pt(14)

# ==================== SECCIÓN 1: RESUMEN EJECUTIVO ====================
h1 = doc.add_heading(level=1)
r_h1 = h1.add_run("1. Resumen Ejecutivo y Matriz Consolidada de Pruebas")
r_h1.font.color.rgb = COLOR_PRIMARY
r_h1.font.bold = True

p_res = doc.add_paragraph()
p_res.add_run(
    "El presente informe consolida los resultados técnicos, arquitecturas, metodologías y hallazgos obtenidos en la ejecución "
    "de los tres componentes evaluados en la prueba técnica práctica para el rol de QA Automation & Performance Engineer:\n\n"
    "1. Prueba E2E (End-to-End): Automatización de flujo de compra en la tienda virtual Demoblaze con Serenity BDD y Screenplay Pattern.\n"
    "2. Prueba de APIs REST: Automatización funcional de los servicios de registro y autenticación (/signup y /login) de Demoblaze con Karate Framework.\n"
    "3. Prueba de Performance (Carga y Análisis): Prueba de carga del servicio de login de FakeStoreAPI (K6 y JMeter) junto con el análisis "
    "técnico profundo y diagnóstico de causa raíz de la prueba de carga del servicio transaccional bancario App Transaction Balance."
)

t_matriz = doc.add_table(rows=4, cols=5)
h_matriz = ["Módulo de Prueba", "Tecnologías y Frameworks", "Alcance y Servicios", "Escenarios / Métricas", "Veredicto"]
for c_idx, h in enumerate(h_matriz):
    t_matriz.cell(0, c_idx).text = h

data_matriz = [
    ("Módulo 1: E2E Web", "Serenity BDD 4.1.20, Cucumber 7, Screenplay, Java 17, Maven", "Demoblaze (https://www.demoblaze.com/): Carrito, Total, Modal Orden y Confirmación", "5 escenarios (Smoke, Outline, JSON, CSV)", "✅ 100% APROBADO (5/5)"),
    ("Módulo 2: APIs REST", "Karate Framework 1.4.1, JUnit 5, Gherkin, Maven", "Demoblaze API (https://api.demoblaze.com): POST /signup y POST /login", "13 escenarios (26 runs) (Data-Driven JSON/CSV)", "✅ 100% APROBADO (13/13)"),
    ("Módulo 3: Performance", "Grafana K6 v2.4.0, Apache JMeter 5.6.3, Python", "FakeStoreAPI (POST /auth/login) y Análisis App Transaction Balance", "21.77 TPS (SLA >= 20), 0% error, Informe RCA", "✅ 100% APROBADO (Todos SLAs)")
]
for r_idx, row in enumerate(data_matriz):
    for c_idx, val in enumerate(row):
        t_matriz.cell(r_idx + 1, c_idx).text = val
style_table(t_matriz, [1.5, 1.8, 1.6, 1.3, 1.0])

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# ==================== SECCIÓN 2: PRUEBA E2E ====================
h2 = doc.add_heading(level=1)
r_h2 = h2.add_run("2. Informe de la Prueba E2E (Web Demoblaze)")
r_h2.font.color.rgb = COLOR_PRIMARY
r_h2.font.bold = True

p_e2e = doc.add_paragraph()
p_e2e.add_run(
    "2.1. Objetivo y Alcance:\n"
    "Automatizar el flujo integral de compra en el aplicativo Demoblaze, que consiste en navegar al catálogo, seleccionar dos productos "
    "(ej. 'Samsung galaxy s6' y 'Nokia lumia 1520'), agregarlos al carrito de compras aceptando las alertas nativas de confirmación, verificar "
    "que ambos artículos figuren en la tabla del carrito con sus respectivos precios, comprobar la sumatoria del total, completar el formulario "
    "de compra (Place Order) y validar que se genere el mensaje 'Thank you for your purchase!' junto con el ID de la orden y el monto cobrado.\n\n"
    "2.2. Arquitectura Implementada: Patrón Screenplay:\n"
    "Se estructuró el código bajo el patrón Screenplay, garantizando separación de responsabilidades y alta legibilidad:\n"
    "• Tasks: NavigateTo (apertura de URL), AddProduct (selección y clic en 'Add to cart'), ViewCart (acceso al carrito), CompleteOrderForm (llenado de modal), FinishPurchase (confirmación), CloseConfirmation (cierre).\n"
    "• User Interfaces: Mapeo de selectores (HomePage, ProductDetailPage, CartPage, OrderModal, ConfirmationModal) con estrategias CSS y XPath resilientes.\n"
    "• Interactions: AcceptAlert para la captura y aceptación síncrona de las alertas nativas de JavaScript que emite Demoblaze.\n"
    "• Questions: TheCartProducts (lista de productos en carrito), TheCartTotal (monto total numérico), TheConfirmationMessage (texto de éxito), TheOrderDetails (extracción de Id y Amount).\n"
    "• Model: Entidades fuertemente tipadas (CustomerInfo, OrderDetails, ProductOrder).\n"
    "• Util: Clases utilitarias JsonReader y CsvReader para el consumo desacoplado de datos externos."
)

p_e2e_data = doc.add_paragraph()
r_edata = p_e2e_data.add_run("2.3. Estrategia Data-Driven Testing (Gherkin, JSON y CSV):\n")
r_edata.font.bold = True
p_e2e_data.add_run(
    "El archivo feature (purchase_flow.feature) fue optimizado para soportar cuatro enfoques de ejecución:\n"
    "1. @Smoke: Flujo feliz estándar de compra.\n"
    "2. @EsquemaEscenario: Scenario Outline parametrizado con tabla Examples nativa de Gherkin.\n"
    "3. @ConsumoJson: Scenario Outline que lee dinámicamente el archivo externo datos_compra.json.\n"
    "4. @ConsumoCsv: Scenario Outline que lee dinámicamente el archivo externo datos_compra.csv."
)

# Tabla Resultados E2E
t_e2e = doc.add_table(rows=6, cols=4)
h_e2e = ["Escenario / Tag", "Parámetros y Productos", "Validaciones Realizadas", "Estado"]
for c_idx, h in enumerate(h_e2e):
    t_e2e.cell(0, c_idx).text = h

data_e2e = [
    ("@Smoke: Compra Exitosa", "Samsung galaxy s6 + Nokia lumia 1520", "Carrito, Total $1180, Modal Orden, 'Thank you for your purchase!'", "✅ PASÓ"),
    ("@EsquemaEscenario: Fila 1", "Nexus 6 + HTC One M9 (Cliente: Ronald)", "Verificación de orden, ID y fecha generada", "✅ PASÓ"),
    ("@EsquemaEscenario: Fila 2", "Sony xperia z5 + Samsung galaxy s7", "Verificación de orden, ID y fecha generada", "✅ PASÓ"),
    ("@ConsumoJson: Compra JSON", "Datos desde datos_compra.json", "Validación completa con CustomerInfo desacoplado", "✅ PASÓ"),
    ("@ConsumoCsv: Compra CSV", "Datos desde datos_compra.csv", "Validación completa con CustomerInfo desacoplado", "✅ PASÓ")
]
for r_idx, row in enumerate(data_e2e):
    for c_idx, val in enumerate(row):
        t_e2e.cell(r_idx + 1, c_idx).text = val
style_table(t_e2e, [1.8, 2.0, 2.0, 0.9])

p_e2e_hallazgos = doc.add_paragraph()
p_e2e_hallazgos.paragraph_format.space_before = Pt(6)
p_e2e_hallazgos.add_run(
    "2.4. Hallazgos y Consideraciones Técnicas:\n"
    "• Demoblaze presenta renderizado asíncrono dinámico tras agregar productos: fue indispensable sincronizar la espera explícita del alert antes de cambiar de página para evitar StaleElementReferenceException.\n"
    "• El botón 'Place Order' requiere que la tabla del carrito haya terminado de poblarse vía AJAX para computar el total; de lo contrario el modal abre con monto 0.\n"
    "• Reportes generados: Serenity Living Documentation (target/site/serenity/index.html) con evidencia gráfica de cada paso y Cucumber Reports en HTML y JSON."
)

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# ==================== SECCIÓN 3: PRUEBA DE APIS ====================
h3 = doc.add_heading(level=1)
r_h3 = h3.add_run("3. Informe de la Prueba de APIs REST (Demoblaze API)")
r_h3.font.color.rgb = COLOR_PRIMARY
r_h3.font.bold = True

p_api = doc.add_paragraph()
p_api.add_run(
    "3.1. Objetivo y Alcance:\n"
    "Automatizar y verificar los endpoints REST de autenticación y registro de Demoblaze (https://api.demoblaze.com):\n"
    "• POST /signup: Registro de usuarios y control de duplicados.\n"
    "• POST /login: Autenticación de usuarios válidos, extracción de token de sesión y manejo de credenciales erróneas.\n\n"
    "3.2. Herramienta: Karate Framework 1.4.1 + JUnit 5:\n"
    "Karate Framework permitió redactar los contratos de prueba directamente en sintaxis Gherkin (BDD), combinando peticiones HTTP, "
    "aserciones sobre payloads JSON y funciones utilitarias en JavaScript en un solo archivo feature."
)

p_api_chall = doc.add_paragraph()
r_achall = p_api_chall.add_run("3.3. Desafíos Técnicos Resueltos (Aspectos Más Relevantes):\n")
r_achall.font.bold = True
p_api_chall.add_run(
    "1. API no estándar (Retorno permanente de HTTP 200):\n"
    "   La API evaluada retorna código HTTP 200 incluso ante credenciales incorrectas ('Wrong password.') o usuarios inexistentes "
    "   ('User does not exist.'). Se implementaron aserciones sobre el objeto JSON de respuesta (response.errorMessage) para certificar el negocio.\n\n"
    "2. Respuesta de Signup Exitoso con comillas y salto de línea (''\\n):\n"
    "   Al crear un usuario nuevo, el endpoint devuelve el texto plano '' (dos comillas) seguido de un salto de línea. Se normalizó la "
    "   cadena aplicando .trim() para validar la respuesta exacta sin inducir falsos negativos.\n\n"
    "3. Independencia y Repetibilidad mediante Generación Dinámica de Usuarios:\n"
    "   Dado que el backend rechaza registros con usernames repetidos, se implementó en karate-config.js la función generateRandomUser "
    "   (timestamp + número aleatorio), asegurando que cada escenario cree un usuario único y los tests se puedan ejecutar indefinidamente.\n\n"
    "4. Desacoplamiento de Rutas (Evitar acumulación de paths en Karate):\n"
    "   En escenarios que ejecutan un /signup inicial y luego un /login, Karate acumula los paths. Se declaró en el Background la URL "
    "   completa (* def signupUrl = baseUrl + '/signup'; * def loginUrl = baseUrl + '/login') garantizando llamadas exactas."
)

# Tabla Resultados API
t_api = doc.add_table(rows=8, cols=4)
h_api = ["Feature / Escenario", "Endpoint & Método", "Validación Realizada", "Estado"]
for c_idx, h in enumerate(h_api):
    t_api.cell(0, c_idx).text = h

data_api = [
    ("signup: Caso 1 (Crear Usuario)", "POST /signup", "HTTP 200, respuesta ''", "✅ PASÓ"),
    ("signup: Caso 2 (Usuario Duplicado)", "POST /signup", "errorMessage: 'This user already exist.'", "✅ PASÓ"),
    ("signup: Outline Data-Driven JSON", "POST /signup (x2)", "Validación de duplicados desde signup_cases.json", "✅ PASÓ"),
    ("signup: Outline Data-Driven CSV", "POST /signup (x2)", "Validación de duplicados desde signup_cases.csv", "✅ PASÓ"),
    ("login: Caso 3 (Login Exitoso)", "POST /login", "HTTP 200, contiene 'Auth_token: <token>'", "✅ PASÓ"),
    ("login: Caso 4A (Password Erróneo)", "POST /login", "errorMessage: 'Wrong password.'", "✅ PASÓ"),
    ("login: Caso 4B (Usuario Inexistente)", "POST /login", "errorMessage: 'User does not exist.'", "✅ PASÓ")
]
for r_idx, row in enumerate(data_api):
    for c_idx, val in enumerate(row):
        t_api.cell(r_idx + 1, c_idx).text = val
style_table(t_api, [1.8, 1.4, 2.6, 0.9])

p_api_res = doc.add_paragraph()
p_api_res.paragraph_format.space_before = Pt(6)
p_api_res.add_run(
    "Resultado Total API: 13 escenarios ejecutados (26 runs por política de reintento de Surefire), 0 fallos (BUILD SUCCESS). "
    "Reporte Karate HTML generado en target/karate-reports/karate-summary.html."
)

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# ==================== SECCIÓN 4: PRUEBA DE PERFORMANCE ====================
h4 = doc.add_heading(level=1)
r_h4 = h4.add_run("4. Informe de la Prueba de Performance & Carga")
r_h4.font.color.rgb = COLOR_PRIMARY
r_h4.font.bold = True

p_perf_intro = doc.add_paragraph()
p_perf_intro.add_run(
    "El módulo de rendimiento abarca dos componentes complementarios: la automatización y ejecución de una prueba de carga real "
    "sobre el endpoint de login de FakeStoreAPI, y el análisis técnico exhaustivo del informe de resultados y monitoreo de la prueba "
    "de carga del servicio bancario App Transaction Balance."
)

p_perf_ej1 = doc.add_paragraph()
r_pej1 = p_perf_ej1.add_run("4.1. Ejercicio 1: Script y Ejecución de Prueba de Carga (Login FakeStoreAPI)\n")
r_pej1.font.bold = True
p_perf_ej1.add_run(
    "• Endpoint Evaluado: POST https://fakestoreapi.com/auth/login\n"
    "• Parametrización: Archivo CSV (users.csv) con 5 cuentas de usuario cargadas eficientemente en memoria mediante SharedArray de K6.\n"
    "• Herramientas Implementadas: Grafana K6 v2.4.0 (script principal k6_login_load_test.js) con ejecutor constant-arrival-rate, "
    "y Apache JMeter 5.6.3 (script jmeter_login_load_test.jmx) con CSV Data Set Config y temporizador de throughput (22 TPS).\n"
    "• Criterios de Aceptación Exigidos: Al menos 20 TPS, tiempo de respuesta máximo <= 1.5s y tasa de error < 3%."
)

# Tabla Resultados Carga K6
t_perf_k6 = doc.add_table(rows=6, cols=4)
h_perf_k6 = ["Criterio Evaluado", "SLA / Umbral Exigido", "Resultado Real en Prueba", "Veredicto"]
for c_idx, h in enumerate(h_perf_k6):
    t_perf_k6.cell(0, c_idx).text = h

data_perf_k6 = [
    ("Rendimiento Mínimo (Throughput)", ">= 20 TPS", "21.77 TPS (21.77 req/s)", "✅ CUMPLE (Superado)"),
    ("Tiempo Máximo de Respuesta", "<= 1.50 s (1,500 ms)", "1.03 s (1,030 ms)", "✅ CUMPLE (Bajo límite)"),
    ("Percentil 95 (P95)", "<= 1.50 s (1,500 ms)", "0.43 s (438 ms)", "✅ CUMPLE (Holgado)"),
    ("Tasa de Error Aceptable", "< 3.00%", "0.00% (0 errores en 661 peticiones)", "✅ CUMPLE (Cero fallos)"),
    ("Integridad de Autenticación", "100% tokens válidos", "661/661 tokens extraídos (100%)", "✅ CUMPLE")
]
for r_idx, row in enumerate(data_perf_k6):
    for c_idx, val in enumerate(row):
        t_perf_k6.cell(r_idx + 1, c_idx).text = val
style_table(t_perf_k6, [2.0, 1.8, 1.8, 1.1])

p_perf_ej2 = doc.add_paragraph()
p_perf_ej2.paragraph_format.space_before = Pt(8)
r_pej2 = p_perf_ej2.add_run("4.2. Ejercicio 2: Análisis de Resultados de Carga (App Transaction Balance)\n")
r_pej2.font.bold = True
p_perf_ej2.add_run(
    "A partir del archivo textSummary.txt y del diagrama temporal de monitoreo proporcionados, se realizó una evaluación "
    "técnica profunda de la prueba de carga ejecutada con 140 Usuarios Virtuales constantes durante 65 minutos (276,650 transacciones)."
)

# Insertar imagen de monitoreo si existe
img_mon = r"D:\Prueba_tecnica_tata\reto_tecnico_qa_tcs\Ejercicio_Performance\Ejercicio_2_Analisis_Resultados\insumos\grafica_monitoreo_vus_vs_rps.png"
if os.path.exists(img_mon):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(4)
    run_img = p_img.add_run()
    run_img.add_picture(img_mon, width=Inches(5.5))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figura: Diagrama de monitoreo temporal de Usuarios Virtuales (VUs) vs Throughput (http_reqs/s).")
    r_cap.font.italic = True
    r_cap.font.size = Pt(8.5)
    r_cap.font.color.rgb = RGBColor(100, 116, 139)

p_perf_findings = doc.add_paragraph()
p_perf_findings.add_run(
    "Hallazgos Críticos del Análisis de Rendimiento:\n"
    "1. Cumplimiento Aparente vs Degradación Oculta:\n"
    "   El acumulado reporta 2.44% de fallos y 97.55% de checks exitosos. No obstante, el monitoreo temporal revela una caída "
    "   catastrófica de rendimiento entre las 01:51:00 y las 01:58:00 (7 minutos), donde las peticiones cayeron de 82 req/s a 10-15 req/s.\n\n"
    "2. Relación VUs vs Throughput (Ley de Rendimiento):\n"
    "   Los 140 VUs se mantuvieron constantes (la línea verde fue plana). El tiempo máximo de respuesta alcanzó 29.93 segundos. "
    "   Por la relación Throughput = VUs / (Tiempo de Respuesta), al elevarse la latencia a 30s cada hilo quedó bloqueado esperando, "
    "   produciendo la caída matemática del throughput a 140 / 30s ≈ 4.67 req/s. La caída se debió a saturación en el servidor, no a desconexión de clientes.\n\n"
    "3. Concentración de 5,987 Errores HTTP 5xx en Stage 1:\n"
    "   El 88.58% de todos los fallos del test se concentraron exclusivamente en Stage 1 durante esa ventana de 7 minutos, "
    "   representando una indisponibilidad localizada cercana al 80%.\n\n"
    "4. Causa Raíz Identificada:\n"
    "   • Agotamiento del pool de conexiones hacia la Base de Datos (HikariCP / Tomcat JDBC).\n"
    "   • Bloqueos transaccionales (row-level lock contention / deadlocks) en tablas de saldos de cuenta.\n"
    "   • Timeouts de 30 segundos en el API Gateway o Balanceador de Carga (HTTP 504 Gateway Timeout).\n"
    "   • Reinicio forzado de contenedores por memoria (Kubernetes OOMKilled), explicando el rebote instantáneo a 82.6 req/s a las 02:00:00.\n\n"
    "5. Recomendaciones de Arquitectura:\n"
    "   • Reducción de Connection Timeout a 3,000 ms (Fail-Fast).\n"
    "   • Desvío de consultas de saldo hacia Réplicas de Lectura (Read Replicas).\n"
    "   • Implementación de Circuit Breaker (Resilience4j) con umbral de 2 segundos.\n"
    "   • Caché distribuida Redis con TTL de 15 a 30 segundos para balances frecuentes."
)

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# ==================== SECCIÓN 5: CONCLUSIONES Y ENTREGA ====================
h5 = doc.add_heading(level=1)
r_h5 = h5.add_run("5. Conclusiones Generales y Estado de los Entregables")
r_h5.font.color.rgb = COLOR_PRIMARY
r_h5.font.bold = True

p_conc = doc.add_paragraph()
p_conc.add_run(
    "La solución entregada demuestra solvencia técnica integral en aseguramiento de calidad automatizado y rendimiento:\n"
    "• Cumplimiento del 100% de los criterios y especificaciones técnicas de Banco Pichincha y TCS.\n"
    "• Arquitectura limpia, desacoplada y escalable (Screenplay Pattern en E2E, contratos declarativos en Karate, scripts optimizados K6/JMeter).\n"
    "• Capacidad de análisis crítico y cuantitativo en performance para diagnosticar fallas de infraestructura en sistemas bancarios.\n"
    "• Código fuente completamente versionado en GitHub con instrucciones paso a paso, reportes enriquecidos y paquetes zip listos para reproducción."
)

p_sign = doc.add_paragraph()
p_sign.paragraph_format.space_before = Pt(16)
r_sign = p_sign.add_run("Ronald Berrones\nQA Automation & Performance Engineer\nTCS / Banco Pichincha — Noviembre 2026")
r_sign.font.bold = True
r_sign.font.color.rgb = COLOR_PRIMARY

# Guardar documentos unificados
out_docx = r"D:\Prueba_tecnica_tata\reto_tecnico_qa_tcs\Informe_General_Prueba_Tecnica_QA.docx"
out_doc = r"D:\Prueba_tecnica_tata\reto_tecnico_qa_tcs\Informe_General_Prueba_Tecnica_QA.doc"

doc.save(out_docx)
shutil.copyfile(out_docx, out_doc)
print(f"Informe General DOCX generado: {out_docx}")
print(f"Informe General DOC generado: {out_doc}")
