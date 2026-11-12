import os
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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
                set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
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
                set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.font.size = Pt(9)
                        run.font.color.rgb = RGBColor(30, 41, 59)
        
        if col_widths:
            for c_idx, width in enumerate(col_widths):
                if c_idx < len(row.cells):
                    row.cells[c_idx].width = Inches(width)

doc = Document()

# Márgenes
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Colores corporativos
COLOR_PRIMARY = RGBColor(0, 43, 73)      # #002B49 (Azul Pichincha)
COLOR_SECONDARY = RGBColor(0, 102, 178)  # Azul claro
COLOR_ACCENT = RGBColor(217, 119, 6)     # Ámbar
COLOR_SUCCESS = RGBColor(22, 163, 74)    # Verde
COLOR_DANGER = RGBColor(220, 38, 38)     # Rojo

# ==================== PORTADA ====================
p_sup = doc.add_paragraph()
r_sup = p_sup.add_run("BANCO PICHINCHA / TCS (TATA CONSULTANCY SERVICES)")
r_sup.font.bold = True
r_sup.font.size = Pt(11)
r_sup.font.color.rgb = COLOR_SECONDARY

p_tit = doc.add_paragraph()
r_tit = p_tit.add_run("DOCUMENTACIÓN TÉCNICA INTEGRAL\nPRUEBA TÉCNICA QA AUTOMATION & PERFORMANCE")
r_tit.font.size = Pt(20)
r_tit.font.bold = True
r_tit.font.color.rgb = COLOR_PRIMARY

p_sub = doc.add_paragraph()
r_sub = p_sub.add_run("Resumen Ejecutivo, Arquitectura, Hallazgos y Resultados de las Pruebas E2E, APIs y Performance")
r_sub.font.size = Pt(11.5)
r_sub.font.italic = True
r_sub.font.color.rgb = RGBColor(100, 116, 139)

doc.add_paragraph().paragraph_format.space_after = Pt(6)

meta_table = doc.add_table(rows=5, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Candidato Evaluado:", "Ronald Berrones"),
    ("Rol / Perfil:", "QA Automation & Performance Engineer"),
    ("Cliente / Entidad:", "Banco Pichincha / TCS"),
    ("Repositorio GitHub:", "https://github.com/ronaldNk1625/reto_tecnico_qa_tcs.git"),
    ("Fecha de Entrega:", "Noviembre 2026")
]
for idx, (k, v) in enumerate(meta_data):
    c0 = meta_table.cell(idx, 0)
    c1 = meta_table.cell(idx, 1)
    c0.text = k
    c1.text = v
    c0.paragraphs[0].runs[0].font.bold = True
    c0.paragraphs[0].runs[0].font.size = Pt(9.5)
    c1.paragraphs[0].runs[0].font.size = Pt(9.5)
style_table(meta_table, [2.2, 4.5])

doc.add_paragraph().paragraph_format.space_after = Pt(14)

# ==================== 1. RESUMEN EJECUTIVO GLOBAL ====================
h1 = doc.add_heading(level=1)
r_h1 = h1.add_run("1. Resumen Ejecutivo Global de la Evaluación")
r_h1.font.color.rgb = COLOR_PRIMARY
r_h1.font.bold = True

p_res = doc.add_paragraph()
p_res.add_run(
    "La presente prueba técnica integral para el rol de QA Automation & Performance Engineer abarca la resolución de cuatro "
    "ejercicios prácticos organizados en tres módulos clave de aseguramiento de calidad:\n"
    "1. Automatización E2E Web en Demoblaze con Serenity BDD y Screenplay Pattern.\n"
    "2. Automatización de APIs REST en Demoblaze con Karate Framework.\n"
    "3. Pruebas de Carga al servicio de Login de FakeStoreAPI con K6 y JMeter.\n"
    "4. Análisis Técnico de Resultados de Rendimiento del servicio App Transaction Balance."
)

t_global = doc.add_table(rows=5, cols=5)
h_global = ["Módulo / Prueba", "Herramientas Clave", "Alcance Evaluado", "Casos / Escenarios", "Resultado Final"]
for c_idx, h in enumerate(h_global):
    t_global.cell(0, c_idx).text = h

data_global = [
    ("Módulo 1: E2E Web", "Serenity BDD 4.1.20, Cucumber 7, Screenplay, Java 17", "Flujo completo de compra, Carrito, Orden, Modales", "5 escenarios (Smoke, Outline, JSON, CSV)", "✅ 100% PASADO (5/5)"),
    ("Módulo 2: APIs REST", "Karate Framework 1.4.1, JUnit 5, Gherkin", "Servicios POST /signup y POST /login, Token, Errores", "13 escenarios (26 runs) (Outline JSON/CSV)", "✅ 100% PASADO (13/13)"),
    ("Módulo 3: Carga (Login)", "Grafana K6 v2.4.0, Apache JMeter 5.6.3", "POST /auth/login con 5 usuarios parametrizados CSV", "661 peticiones a 21.77 TPS (SLA >= 20)", "✅ 100% PASADO (21.77 TPS)"),
    ("Módulo 4: Análisis Rendimiento", "Análisis Cuantitativo K6, RCA, Word / Markdown", "Diagnóstico de caída en App Transaction Balance", "276,650 peticiones analizadas temporalmente", "✅ INFORME COMPLETO")
]

for r_idx, row in enumerate(data_global):
    for c_idx, val in enumerate(row):
        t_global.cell(r_idx + 1, c_idx).text = val
style_table(t_global, [1.5, 1.8, 1.6, 1.2, 1.1])

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# ==================== 2. MÓDULO 1: AUTOMATIZACIÓN E2E ====================
h2 = doc.add_heading(level=1)
r_h2 = h2.add_run("2. Módulo 1: Automatización E2E Web (Demoblaze)")
r_h2.font.color.rgb = COLOR_PRIMARY
r_h2.font.bold = True

p_e2e_intro = doc.add_paragraph()
p_e2e_intro.add_run(
    "Objetivo: Automatizar el flujo completo de compra de dos productos en la tienda virtual Demoblaze (https://www.demoblaze.com/), "
    "validando la persistencia en el carrito, cálculo del total, diligenciamiento del modal de orden, confirmación de compra y mensaje final."
)

p_e2e_arch = doc.add_paragraph()
r_arch_t = p_e2e_arch.add_run("Arquitectura Implementada: Patrón Screenplay\n")
r_arch_t.font.bold = True
p_e2e_arch.add_run(
    "A diferencia del tradicional Page Object Model (POM), se implementó el patrón Screenplay (orientado a actores, habilidades y tareas), "
    "garantizando máxima mantenibilidad, desacoplamiento y cumplimiento del principio de responsabilidad única (SOLID):\n"
    "• Tasks (Tareas de Negocio): NavigateTo, AddProduct, ViewCart, CompleteOrderForm, FinishPurchase, CloseConfirmation.\n"
    "• User Interfaces (Mapeo de Elementos): HomePage, ProductDetailPage, CartPage, OrderModal, ConfirmationModal (con selectores robustos CSS y XPath).\n"
    "• Model (Entidades): CustomerInfo, OrderDetails, ProductOrder.\n"
    "• Questions (Aserciones y Validaciones): TheCartProducts, TheCartTotal, TheConfirmationMessage, TheOrderDetails.\n"
    "• Interactions (Interacciones Específicas): AcceptAlert (manejo de alertas JavaScript nativas de confirmación de agregado).\n"
    "• Util (Lectores de Datos): JsonReader, CsvReader, Constants."
)

p_e2e_data = doc.add_paragraph()
r_data_t = p_e2e_data.add_run("Estrategia Data-Driven Testing (JSON & CSV):\n")
r_data_t.font.bold = True
p_e2e_data.add_run(
    "Se diseñaron 4 tipos de escenarios en el archivo feature (purchase_flow.feature):\n"
    "1. @Smoke: Flujo feliz estándar de compra.\n"
    "2. @EsquemaEscenario: Scenario Outline parametrizado con tabla Examples nativa de Gherkin.\n"
    "3. @ConsumoJson: Scenario Outline con inyección dinámica desde archivo externo datos_compra.json.\n"
    "4. @ConsumoCsv: Scenario Outline con inyección dinámica desde archivo externo datos_compra.csv."
)

# Resultados E2E
t_e2e_res = doc.add_table(rows=6, cols=4)
h_e2e_res = ["Escenario / Tag", "Datos / Parámetros", "Validaciones Clave", "Estado"]
for c_idx, h in enumerate(h_e2e_res):
    t_e2e_res.cell(0, c_idx).text = h

data_e2e_res = [
    ("@Smoke: Compra Exitosa", "Samsung galaxy s6 + Nokia lumia 1520", "Carrito, Total $1180, Modal Orden, 'Thank you for your purchase!'", "✅ PASÓ"),
    ("@EsquemaEscenario: Fila 1", "Nexus 6 + HTC One M9 (Cliente: Ronald)", "Verificación de orden, ID y fecha generada", "✅ PASÓ"),
    ("@EsquemaEscenario: Fila 2", "Sony xperia z5 + Samsung galaxy s7", "Verificación de orden, ID y fecha generada", "✅ PASÓ"),
    ("@ConsumoJson: Compra JSON", "Datos cargados desde datos_compra.json", "Validación completa con CustomerInfo desacoplado", "✅ PASÓ"),
    ("@ConsumoCsv: Compra CSV", "Datos cargados desde datos_compra.csv", "Validación completa con CustomerInfo desacoplado", "✅ PASÓ")
]
for r_idx, row in enumerate(data_e2e_res):
    for c_idx, val in enumerate(row):
        t_e2e_res.cell(r_idx + 1, c_idx).text = val
style_table(t_e2e_res, [1.8, 2.0, 2.0, 0.9])

p_e2e_rep = doc.add_paragraph()
p_e2e_rep.paragraph_format.space_before = Pt(6)
p_e2e_rep.add_run(
    "Reportes Generados en E2E:\n"
    "• Serenity Living Documentation (target/site/serenity/index.html): Documentación viva con capturas de pantalla automáticas paso a paso.\n"
    "• Cucumber HTML & JSON Reports (target/cucumber-reports/): Reporte estándar para integración continua."
)

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# ==================== 3. MÓDULO 2: AUTOMATIZACIÓN DE APIS ====================
h3 = doc.add_heading(level=1)
r_h3 = h3.add_run("3. Módulo 2: Automatización de APIs REST (Demoblaze API)")
r_h3.font.color.rgb = COLOR_PRIMARY
r_h3.font.bold = True

p_api_intro = doc.add_paragraph()
p_api_intro.add_run(
    "Objetivo: Automatizar los endpoints de registro (/signup) y autenticación (/login) de Demoblaze (https://api.demoblaze.com), "
    "cubriendo casos de éxito, validaciones negativas, control de duplicados y parametrización externa."
)

p_api_tool = doc.add_paragraph()
r_tool_t = p_api_tool.add_run("Herramienta y Enfoque: Karate Framework 1.4.1 + JUnit 5\n")
r_tool_t.font.bold = True
p_api_tool.add_run(
    "Se seleccionó Karate Framework por su capacidad nativa de escribir pruebas de API en lenguaje Gherkin sin requerir "
    "código de pegamento (glue code o step definitions en Java), permitiendo ejecutar requests HTTP, aserciones JSON y scripts JavaScript inline."
)

p_api_diff = doc.add_paragraph()
r_diff_t = p_api_diff.add_run("Desafíos Técnicos Resueltos (Lo más relevante):\n")
r_diff_t.font.bold = True
p_api_diff.add_run(
    "1. API no estándar (Siempre retorna HTTP 200):\n"
    "   La API de Demoblaze devuelve HTTP 200 tanto para operaciones exitosas como para errores de negocio (ej. 'Wrong password.', 'User does not exist.'). "
    "   Por tanto, las validaciones no pudieron basarse únicamente en el código de estado, sino en la estructura y contenido del payload JSON de respuesta.\n\n"
    "2. Respuesta de Signup Exitoso con formato texto plano (''\\n):\n"
    "   Al crear un usuario, el backend devuelve el texto crudo '' con comillas y salto de línea. Se normalizó la respuesta con `.trim()` "
    "   para validar exactamente la condición esperada sin falsos negativos.\n\n"
    "3. Independencia y Repetibilidad mediante Usuarios Únicos:\n"
    "   Dado que el backend no permite reutilizar nombres de usuario en /signup, se implementó una función JavaScript generadora "
    "   (generateRandomUser) en karate-config.js que produce identificadores únicos (timestamp + aleatorio), garantizando que las pruebas "
    "   puedan ejecutarse infinitas veces sin colisión de datos.\n\n"
    "4. Manejo de URLs Absolutas vs Path Acumulativo:\n"
    "   En escenarios que encadenaban /signup seguido de /login, Karate acumulaba los segmentos de ruta. Se solucionó declarando URLs completas "
    "   en el Background (* def signupUrl = baseUrl + '/signup'; * def loginUrl = baseUrl + '/login') garantizando rutas exactas."
)

# Resultados API
t_api_res = doc.add_table(rows=8, cols=4)
h_api_res = ["Feature / Escenario", "Método & Endpoint", "Validación Esperada", "Resultado"]
for c_idx, h in enumerate(h_api_res):
    t_api_res.cell(0, c_idx).text = h

data_api_res = [
    ("signup: Caso 1 (Nuevo Usuario)", "POST /signup", "HTTP 200, respuesta ''", "✅ PASÓ"),
    ("signup: Caso 2 (Usuario Duplicado)", "POST /signup", "errorMessage: 'This user already exist.'", "✅ PASÓ"),
    ("signup: Outline Data-Driven JSON", "POST /signup (x2)", "Validación duplicados desde signup_cases.json", "✅ PASÓ"),
    ("signup: Outline Data-Driven CSV", "POST /signup (x2)", "Validación duplicados desde signup_cases.csv", "✅ PASÓ"),
    ("login: Caso 3 (Login Exitoso)", "POST /login", "HTTP 200, contiene 'Auth_token: <token>'", "✅ PASÓ"),
    ("login: Caso 4A (Password Incorrecto)", "POST /login", "errorMessage: 'Wrong password.'", "✅ PASÓ"),
    ("login: Caso 4B (Usuario Inexistente)", "POST /login", "errorMessage: 'User does not exist.'", "✅ PASÓ")
]
for r_idx, row in enumerate(data_api_res):
    for c_idx, val in enumerate(row):
        t_api_res.cell(r_idx + 1, c_idx).text = val
style_table(t_api_res, [1.8, 1.4, 2.6, 0.9])

p_api_rep = doc.add_paragraph()
p_api_rep.paragraph_format.space_before = Pt(6)
p_api_rep.add_run(
    "Resultado Total API: 13 escenarios ejecutados (26 runs por Surefire re-run policy), 0 fallos. "
    "Reporte Karate HTML generado en target/karate-reports/karate-summary.html."
)

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# ==================== 4. MÓDULO 3: PRUEBAS DE CARGA ====================
h4 = doc.add_heading(level=1)
r_h4 = h4.add_run("4. Módulo 3: Pruebas de Carga y Rendimiento (Login FakeStoreAPI)")
r_h4.font.color.rgb = COLOR_PRIMARY
r_h4.font.bold = True

p_load_intro = doc.add_paragraph()
p_load_intro.add_run(
    "Objetivo: Ejecutar una prueba de carga sobre el servicio de autenticación POST https://fakestoreapi.com/auth/login "
    "parametrizando 5 credenciales desde un archivo CSV (users.csv), exigiendo alcanzar al menos 20 TPS, un tiempo máximo de 1.5s "
    "y una tasa de error menor al 3%."
)

p_load_tools = doc.add_paragraph()
r_ltool_t = p_load_tools.add_run("Herramientas Utilizadas:\n")
r_ltool_t.font.bold = True
p_load_tools.add_run(
    "• Grafana K6 v2.4.0 (Script Principal): k6_login_load_test.js, con ejecutor constant-arrival-rate (22 TPS garantizados), "
    "lectura de CSV con SharedArray para bajo consumo de memoria, y definición de Thresholds.\n"
    "• Apache JMeter 5.6.3 (Script Complementario): jmeter_login_load_test.jmx, parametrizado con CSV Data Set Config, "
    "Constant Throughput Timer (1320 req/min = 22 TPS) y aserciones de código y tiempo."
)

# Matriz de Cumplimiento de Carga
t_load_res = doc.add_table(rows=6, cols=4)
h_load_res = ["Criterio Evaluado", "SLA / Umbral Exigido", "Resultado Real en Prueba", "Veredicto"]
for c_idx, h in enumerate(h_load_res):
    t_load_res.cell(0, c_idx).text = h

data_load_res = [
    ("Rendimiento Mínimo (TPS)", ">= 20 TPS", "21.77 TPS (21.77 req/s)", "✅ CUMPLE (Superado)"),
    ("Tiempo Máximo de Respuesta", "<= 1.50 s (1,500 ms)", "1.03 s (1,030 ms)", "✅ CUMPLE (Bajo límite)"),
    ("Percentil 95 (P95)", "<= 1.50 s (1,500 ms)", "0.43 s (438 ms)", "✅ CUMPLE (Holgado)"),
    ("Tasa de Error Aceptable", "< 3.00%", "0.00% (0 errores)", "✅ CUMPLE (Cero fallos)"),
    ("Validación de Tokens", "100% tokens JWT válidos", "661/661 tokens extraídos", "✅ CUMPLE")
]
for r_idx, row in enumerate(data_load_res):
    for c_idx, val in enumerate(row):
        t_load_res.cell(r_idx + 1, c_idx).text = val
style_table(t_load_res, [2.0, 1.8, 1.8, 1.1])

p_load_rep = doc.add_paragraph()
p_load_rep.paragraph_format.space_before = Pt(6)
p_load_rep.add_run(
    "Reportes de Carga Generados:\n"
    "• Dashboard HTML Interactivo: Ejercicio_Performance/Ejercicio_1_Script_Carga/reports/reporte_ejecucion.html\n"
    "• Resumen en Texto Plano: Ejercicio_Performance/Ejercicio_1_Script_Carga/reports/summary.txt\n"
    "• Métricas Crudas JSON: Ejercicio_Performance/Ejercicio_1_Script_Carga/reports/summary.json"
)

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# ==================== 5. MÓDULO 4: ANÁLISIS DE RESULTADOS ====================
h5 = doc.add_heading(level=1)
r_h5 = h5.add_run("5. Módulo 4: Análisis de Resultados de Carga (App Transaction Balance)")
r_h5.font.color.rgb = COLOR_PRIMARY
r_h5.font.bold = True

p_ana_intro = doc.add_paragraph()
p_ana_intro.add_run(
    "Objetivo: Analizar en profundidad el archivo textSummary.txt y la gráfica de monitoreo temporal (VUs vs Throughput) de una prueba "
    "de carga ejecutada con 140 Usuarios Virtuales durante 65 minutos sobre el servicio App Transaction Balance."
)

# Insertar gráfica de monitoreo si existe
img_monitoreo = r"D:\Prueba_tecnica_tata\reto_tecnico_qa_tcs\Ejercicio_Performance\Ejercicio_2_Analisis_Resultados\insumos\grafica_monitoreo_vus_vs_rps.png"
if os.path.exists(img_monitoreo):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(4)
    run_img = p_img.add_run()
    run_img.add_picture(img_monitoreo, width=Inches(5.6))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figura: Gráfica de Monitoreo temporal de VUs (verde) vs Throughput http_reqs/s (azul).")
    r_cap.font.italic = True
    r_cap.font.size = Pt(8.5)
    r_cap.font.color.rgb = RGBColor(100, 116, 139)

p_ana_findings = doc.add_paragraph()
r_find_t = p_ana_findings.add_run("Hallazgos Principales y Análisis Causa Raíz (RCA):\n")
r_find_t.font.bold = True
p_ana_findings.add_run(
    "1. Cumplimiento Aparente vs Falla Oculta Severa:\n"
    "   El acumulado reporta 2.44% de fallos y 97.55% de checks exitosos. Sin embargo, el análisis temporal revela un incidente crítico "
    "   entre las 01:51:00 y las 01:58:00 (duración de 7 minutos), donde el rendimiento colapsó de ~82 req/s a menos de 10-15 req/s.\n\n"
    "2. Relación VUs vs Throughput (Ley de Rendimiento):\n"
    "   Durante el desplome, los 140 VUs se mantuvieron constantes (la línea verde no cayó). El tiempo máximo de respuesta alcanzó "
    "   29.93 segundos. Por la relación Throughput = VUs / (Tiempo de Respuesta), con 140 VUs bloqueados esperando 30 segundos, "
    "   el throughput cae automáticamente a 140 / 30s ≈ 4.67 req/s. La caída no fue por desconexión de clientes, sino por saturación del backend.\n\n"
    "3. Concentración de 5,987 Errores HTTP 5xx en Stage 1:\n"
    "   El 88.58% de todos los fallos del test se concentraron exclusivamente en Stage 1 durante esa ventana de 7 minutos, "
    "   representando una indisponibilidad local cercana al 80%.\n\n"
    "4. Causa Raíz Técnica:\n"
    "   • Agotamiento del pool de conexiones a Base de Datos (HikariCP / Tomcat).\n"
    "   • Bloqueos transaccionales (row locks / deadlocks) en tablas de saldo y transacciones.\n"
    "   • Timeouts de 30 segundos en el API Gateway (HTTP 504 Gateway Timeout).\n"
    "   • Reinicio de contenedores por memoria (Kubernetes OOMKilled), lo cual explica el rebote instantáneo a 82.6 req/s a las 02:00:00.\n\n"
    "5. Recomendaciones de Arquitectura:\n"
    "   • Reducción de Connection Timeout a 3,000 ms (Fail-Fast).\n"
    "   • Enrutamiento de consultas de saldo a Réplicas de Lectura (Read Replicas).\n"
    "   • Implementación de Circuit Breaker (Resilience4j) con umbral de 2 segundos.\n"
    "   • Caché distribuida Redis con TTL de 15 a 30 segundos para balances frecuentes."
)

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# ==================== 6. CONCLUSIONES ====================
h6 = doc.add_heading(level=1)
r_h6 = h6.add_run("6. Conclusiones Generales y Valor Agregado")
r_h6.font.color.rgb = COLOR_PRIMARY
r_h6.font.bold = True

p_fin = doc.add_paragraph()
p_fin.add_run(
    "La solución entregada demuestra un dominio técnico integral y maduro en automatización de pruebas y aseguramiento de rendimiento:\n"
    "• Dominio de múltiples lenguajes y frameworks: Java 17, Serenity BDD, Cucumber, Karate, JavaScript, K6, JMeter y Python.\n"
    "• Arquitectura limpia y escalable: Aplicación rigurosa del patrón Screenplay en E2E y modularización data-driven con JSON y CSV.\n"
    "• Criterio analítico sénior: Capacidad para ir más allá de los números promedio en performance, detectando anomalías temporales, "
    "cuellos de botella en infraestructura y proponiendo soluciones de arquitectura bancaria resiliente.\n"
    "• Entrega completa y reproducible: Código versionado en GitHub con instrucciones paso a paso, reportes enriquecidos y paquetes zip listos para evaluación."
)

p_sign = doc.add_paragraph()
p_sign.paragraph_format.space_before = Pt(16)
r_sign = p_sign.add_run("Ronald Berrones\nQA Automation & Performance Engineer\nTCS / Banco Pichincha")
r_sign.font.bold = True
r_sign.font.color.rgb = COLOR_PRIMARY

# Guardar archivos DOCX y DOC
out_docx = r"D:\Prueba_tecnica_tata\reto_tecnico_qa_tcs\Documentacion_Prueba_Tecnica_QA.docx"
out_doc = r"D:\Prueba_tecnica_tata\reto_tecnico_qa_tcs\Documentacion_Prueba_Tecnica_QA.doc"

doc.save(out_docx)
shutil.copyfile(out_docx, out_doc)
print(f"Documento DOCX generado: {out_docx}")
print(f"Documento DOC generado: {out_doc}")

