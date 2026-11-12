import os
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

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
        # Evitar división de filas en saltos de página
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        # Repetir encabezado en cada página
        if i == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            for cell in row.cells:
                set_cell_background(cell, "002B49")
                set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
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
                set_cell_margins(cell, top=100, bottom=100, left=160, right=160)
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.font.size = Pt(9)
                        run.font.color.rgb = RGBColor(30, 41, 59)
        
        if col_widths:
            for c_idx, width in enumerate(col_widths):
                if c_idx < len(row.cells):
                    row.cells[c_idx].width = Inches(width)

doc = Document()

# Configuración de márgenes
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Color primario
COLOR_PRIMARY = RGBColor(0, 43, 73)      # #002B49
COLOR_SECONDARY = RGBColor(180, 83, 9)   # Amber dark
COLOR_DANGER = RGBColor(185, 28, 28)     # Red
COLOR_TEXT = RGBColor(30, 41, 59)        # Slate 800

# ==================== PORTADA / ENCABEZADO ====================
p_top = doc.add_paragraph()
r_badge = p_top.add_run("BANCO PICHINCHA / TCS (TATA CONSULTANCY SERVICES)")
r_badge.font.bold = True
r_badge.font.size = Pt(11)
r_badge.font.color.rgb = RGBColor(0, 75, 122)

title_p = doc.add_paragraph()
title_run = title_p.add_run("INFORME DE ANÁLISIS DE RESULTADOS\nPRUEBAS DE CARGA Y ESTRÉS")
title_run.font.size = Pt(20)
title_run.font.bold = True
title_run.font.color.rgb = COLOR_PRIMARY

sub_p = doc.add_paragraph()
sub_run = sub_p.add_run("Evaluación del Servicio: App Transaction Balance\nAnálisis de Desempeño, Causa Raíz de Degradación y Recomendaciones")
sub_run.font.size = Pt(12)
sub_run.font.italic = True
sub_run.font.color.rgb = RGBColor(100, 116, 139)

meta_table = doc.add_table(rows=4, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Aplicación / Servicio:", "App Transaction Balance"),
    ("Rol Responsable:", "QA Automation & Performance Engineer"),
    ("Candidato Evaluado:", "Ronald Berrones"),
    ("Fecha de Evaluación:", "Noviembre 2026")
]
for idx, (k, v) in enumerate(meta_data):
    cell_k = meta_table.cell(idx, 0)
    cell_v = meta_table.cell(idx, 1)
    cell_k.text = k
    cell_v.text = v
    cell_k.paragraphs[0].runs[0].font.bold = True
    cell_k.paragraphs[0].runs[0].font.size = Pt(9.5)
    cell_v.paragraphs[0].runs[0].font.size = Pt(9.5)
style_table(meta_table, [2.0, 4.5])

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# ==================== 1. RESUMEN EJECUTIVO ====================
h1 = doc.add_heading(level=1)
r_h1 = h1.add_run("1. Resumen Ejecutivo")
r_h1.font.color.rgb = COLOR_PRIMARY
r_h1.font.bold = True

p_desc = doc.add_paragraph()
p_desc.add_run(
    "El presente informe expone la evaluación exhaustiva de desempeño realizada sobre el servicio transaccional "
    "'App Transaction Balance'. La prueba se ejecutó con una carga sostenida de 140 Usuarios Virtuales (VUs) "
    "durante un intervalo de aproximadamente 65 minutos (276,650 transacciones procesadas).\n\n"
    "A nivel macro, el servicio arrojó una tasa global de fallos del 2.44% y un 97.55% de checks exitosos, valores que "
    "aparentan cumplir los límites contractuales estándar (< 3% de error). No obstante, el análisis temporal "
    "revela un incidente crítico de degradación que compromete severamente la operación bancaria."
)

# Tabla de Métricas Clave
t_metricas = doc.add_table(rows=9, cols=4)
headers = ["Métrica Evaluada", "Valor Obtenido", "Límite / SLA", "Evaluación Técnica"]
for c_idx, h in enumerate(headers):
    t_metricas.cell(0, c_idx).text = h

data_metricas = [
    ("Transacciones Totales (http_reqs)", "276,650 peticiones", "N/A", "Alto volumen"),
    ("Rendimiento Promedio (Throughput)", "73.18 req/s", "> 70 req/s", "Satisfactorio en régimen"),
    ("Tiempo Promedio (http_req_duration avg)", "861.68 ms", "< 1,000 ms", "Aceptable en promedio"),
    ("Mediana de Respuesta (med)", "613.42 ms", "< 1,000 ms", "Óptimo en operación normal"),
    ("Percentil 90 (p90)", "1.28 s (1,280 ms)", "< 1,500 ms", "Aceptable"),
    ("Percentil 95 (p95)", "1.57 s (1,570 ms)", "< 1,500 ms", "⚠️ INCUMPLE SLA (> 1.5s)"),
    ("Tiempo Máximo (max)", "29.93 s (29,930 ms)", "< 5.0 s", "🚨 CRÍTICO (Timeout de 30s)"),
    ("Tasa de Fallos (http_req_failed)", "2.44% (6,759 fallos)", "< 3.00%", "Cumple globalmente")
]

for r_idx, row in enumerate(data_metricas):
    for c_idx, val in enumerate(row):
        t_metricas.cell(r_idx + 1, c_idx).text = val

style_table(t_metricas, [2.2, 1.6, 1.4, 1.8])

# Llamado de atención
p_alert = doc.add_paragraph()
p_alert.paragraph_format.space_before = Pt(8)
r_alert = p_alert.add_run("⚠️ CONCLUSIÓN DEL RESUMEN EJECUTIVO: ")
r_alert.font.bold = True
r_alert.font.color.rgb = COLOR_DANGER
p_alert.add_run(
    "El servicio NO se considera apto para paso a producción en su estado actual. Aunque el promedio global enmascara "
    "los fallos, existió una ventana de 7 minutos con indisponibilidad del 80% y tiempos de espera de 30 segundos."
)

doc.add_paragraph().paragraph_format.space_after = Pt(10)

# ==================== 2. ANÁLISIS DEL DIAGRAMA DE MONITOREO ====================
h2 = doc.add_heading(level=1)
r_h2 = h2.add_run("2. Análisis del Diagrama de Monitoreo: VUs vs Throughput")
r_h2.font.color.rgb = COLOR_PRIMARY
r_h2.font.bold = True

p_diag = doc.add_paragraph()
p_diag.add_run(
    "El gráfico de monitoreo generado durante la prueba registra la interacción entre los Usuarios Virtuales "
    "(línea verde) y las peticiones completadas por segundo (línea azul):"
)

# Insertar imagen del diagrama
img_grafica = r"D:\Prueba_tecnica_tata\reto_tecnico_qa_tcs\Ejercicio_Performance\Ejercicio_2_Analisis_Resultados\insumos\grafica_monitoreo_vus_vs_rps.png"
if os.path.exists(img_grafica):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(6)
    run_img = p_img.add_run()
    run_img.add_picture(img_grafica, width=Inches(5.8))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figura 1: Diagrama de Monitoreo temporal de Usuarios Virtuales (VUs) vs Throughput (http_reqs).")
    r_cap.font.italic = True
    r_cap.font.size = Pt(8.5)
    r_cap.font.color.rgb = RGBColor(100, 116, 139)

p_fases = doc.add_paragraph()
p_fases.add_run(
    "Del análisis temporal se identifican cuatro fases operativas determinantes:\n\n"
    "• Fase 1: Régimen Estable (01:36:00 - 01:50:00):\n"
    "  Con 140 VUs constantes, el sistema entregó un throughput oscilante entre 75 y 90 req/s con tiempos "
    "  cercanos a la mediana (613 ms).\n\n"
    "• Fase 2: Incidente Crítico y Desplome (01:51:00 - 01:58:00) [ANOMALÍA PRINCIPAL]:\n"
    "  A las 01:51:00, el throughput se desploma vertiginosamente de 82 req/s a menos de 10-15 req/s. "
    "  Nótese que la línea de VUs se mantiene estrictamente en 140. La explicación matemática radica en la ley de rendimiento:\n"
    "      Throughput = VUs / (Tiempo de Respuesta + Think Time)\n"
    "  Al elevarse la latencia del servidor a 29.93 segundos, cada hilo de VU queda bloqueado esperando respuesta. "
    "  Con 140 VUs esperando 30 segundos, el throughput cae automáticamente a 140 / 30s ≈ 4.67 req/s.\n\n"
    "• Fase 3: Recuperación Abrupta en Escalón (01:59:00 - 02:02:00):\n"
    "  A las 02:00:00 el rendimiento rebota verticalmente a ~82.6 req/s (tooltip: 2025-04-24 02:02:00, VUs: 140, http_reqs: 82.6/s). "
    "  Esta recuperación instantánea en escalón evidencia un reinicio de servicio (Kubernetes Pod Restart / OOMKilled) "
    "  o el reciclaje forzado de conexiones bloqueadas en la base de datos.\n\n"
    "• Fase 4: Régimen Post-Incidente (02:02:00 - 02:36:00):\n"
    "  El sistema retoma la estabilidad en ~80 req/s hasta la finalización de la prueba."
)

doc.add_paragraph().paragraph_format.space_after = Pt(10)

# ==================== 3. ANÁLISIS DE ERRORES Y TEXTSUMMARY ====================
h3 = doc.add_heading(level=1)
r_h3 = h3.add_run("3. Análisis Cuantitativo de Errores y Tiempos (textSummary.txt)")
r_h3.font.color.rgb = COLOR_PRIMARY
r_h3.font.bold = True

p_err_desc = doc.add_paragraph()
p_err_desc.add_run(
    "La captura detallada de K6 (textSummary.txt) aporta la distribución exacta de las peticiones fallidas por etapa de ejecución:"
)

# Insertar imagen de textSummary
img_summary = r"D:\Prueba_tecnica_tata\reto_tecnico_qa_tcs\Ejercicio_Performance\Ejercicio_2_Analisis_Resultados\insumos\textSummary_captura.png"
if os.path.exists(img_summary):
    p_img2 = doc.add_paragraph()
    p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img2.paragraph_format.space_before = Pt(6)
    p_img2.paragraph_format.space_after = Pt(6)
    run_img2 = p_img2.add_run()
    run_img2.add_picture(img_summary, width=Inches(5.8))
    p_cap2 = doc.add_paragraph()
    p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap2 = p_cap2.add_run("Figura 2: Resumen oficial de métricas K6 extraído de textSummary.txt.")
    r_cap2.font.italic = True
    r_cap2.font.size = Pt(8.5)
    r_cap2.font.color.rgb = RGBColor(100, 116, 139)

# Tabla de Errores por Etapa
t_stages = doc.add_table(rows=5, cols=5)
h_stages = ["Etapa de Carga", "Tipo de Error", "Total Fallos", "Tasa / Seg", "% del Total de Errores"]
for c_idx, h in enumerate(h_stages):
    t_stages.cell(0, c_idx).text = h

data_stages = [
    ("Stage 0 (Warm-up)", "HTTP 5xx", "1", "0.000265/s", "0.01%"),
    ("Stage 1 (Carga Sostenida)", "HTTP 4xx", "769", "0.203409/s", "11.38% (Throttling / 429)"),
    ("Stage 1 (Carga Sostenida)", "HTTP 5xx", "5,987", "1.583625/s", "88.58% (🚨 INCIDENTE)"),
    ("Stage 2 (Ramp-down)", "HTTP 5xx", "2", "0.000529/s", "0.03%"),
]
for r_idx, row in enumerate(data_stages):
    for c_idx, val in enumerate(row):
        t_stages.cell(r_idx + 1, c_idx).text = val
style_table(t_stages, [1.6, 1.2, 1.0, 1.2, 1.8])

p_stages_exp = doc.add_paragraph()
p_stages_exp.paragraph_format.space_before = Pt(6)
p_stages_exp.add_run(
    "Hallazgos Cruciales de la Distribución de Errores:\n"
    "1. El 88.58% de todos los errores (5,987 peticiones) correspondieron a fallos de servidor HTTP 5xx "
    "concentrados exclusivamente en Stage 1 durante la ventana 01:51 a 01:58.\n"
    "2. En esa ventana temporal de 7 minutos, la tasa local de fallo rondó el 80% (indisponibilidad temporal).\n"
    "3. Los 769 errores HTTP 4xx evidencian rechazo de peticiones por rate-limiting o concurrencia no serializada "
    "en balance de cuentas."
)

# Desglose de Latencias de Red vs Servidor
p_net_title = doc.add_paragraph()
r_net_t = p_net_title.add_run("Aislamiento del Cuello de Botella (Red vs Backend):")
r_net_t.font.bold = True

t_net = doc.add_table(rows=6, cols=4)
h_net = ["Métrica de Red / Protocolo", "Promedio", "Máximo", "Evaluación de Causa"]
for c_idx, h in enumerate(h_net):
    t_net.cell(0, c_idx).text = h

data_net = [
    ("Bloqueo Local (http_req_blocked)", "10.97 µs", "35.02 ms", "Despreciable (sin saturación de sockets)"),
    ("Conexión TCP (http_req_connecting)", "3.30 µs", "11.82 ms", "Instantánea (reutilización keep-alive)"),
    ("Handshake TLS (http_req_tls_handshaking)", "7.36 µs", "27.02 ms", "Negociación óptima"),
    ("Envío de Payload (http_req_sending)", "43.22 µs", "31.25 ms", "Ancho de banda suficiente"),
    ("ESPERA EN SERVIDOR (http_req_waiting)", "861.21 ms", "29.93 s", "🚨 99.9% DEL TIEMPO: DEMORA EN BACKEND")
]
for r_idx, row in enumerate(data_net):
    for c_idx, val in enumerate(row):
        t_net.cell(r_idx + 1, c_idx).text = val
style_table(t_net, [2.2, 1.2, 1.2, 2.2])

doc.add_paragraph().paragraph_format.space_after = Pt(10)

# ==================== 4. ANÁLISIS DE CAUSA RAÍZ ====================
h4 = doc.add_heading(level=1)
r_h4 = h4.add_run("4. Análisis de Causa Raíz (RCA)")
r_h4.font.color.rgb = COLOR_PRIMARY
r_h4.font.bold = True

p_rca = doc.add_paragraph()
p_rca.add_run(
    "La correlación entre el tiempo máximo de 29.93s, la caída de throughput y los 5,987 errores 5xx sustenta "
    "las siguientes causas raíz directas:\n\n"
    "1. Agotamiento del Connection Pool hacia la Base de Datos:\n"
    "   Bajo 140 VUs concurrentes consultando saldos, el pool de conexiones (ej. HikariCP / Tomcat) se agotó. "
    "   Las solicitudes entrantes esperaron en cola hasta que expiró el connection timeout estándar de 30 segundos.\n\n"
    "2. Contención por Bloqueos Transaccionales (Row Locks / Deadlocks):\n"
    "   La consulta de saldos transaccionales suele involucrar bloqueos sobre tablas de cuentas y movimientos. "
    "   Múltiples transacciones concurrentes sobre registros interdependientes generaron cascadas de bloqueo.\n\n"
    "3. Expiración de Timeout en Balanceador de Carga (HTTP 504 Gateway Timeout):\n"
    "   La cifra de 29.93 segundos es el patrón inequívoco de un timeout de 30 segundos configurado en el API Gateway "
    "   o Balanceador (Nginx / AWS ALB). Al cumplirse 30s sin respuesta del backend, el gateway corta y responde HTTP 504.\n\n"
    "4. Reinicio por Consumo de Memoria (Kubernetes OOMKilled / CrashLoop):\n"
    "   La acumulación de peticiones encoladas saturó la memoria del contenedor. El orquestador reinició el pod, "
    "   lo que explica la recuperación abrupta observada a las 02:00:00."
)

doc.add_paragraph().paragraph_format.space_after = Pt(10)

# ==================== 5. CONCLUSIONES ====================
h5 = doc.add_heading(level=1)
r_h5 = h5.add_run("5. Conclusiones")
r_h5.font.color.rgb = COLOR_PRIMARY
r_h5.font.bold = True

p_conc = doc.add_paragraph()
p_conc.add_run(
    "1. El servicio App Transaction Balance no es apto para producción en su estado actual, a pesar de que el indicador "
    "global de error (2.44%) se encuentre bajo el 3%.\n\n"
    "2. El Percentil 95 (1.57 segundos) y el Tiempo Máximo (29.93 segundos) violan frontalmente los estándares de "
    "experiencia de usuario y SLAs bancarios de Banco Pichincha.\n\n"
    "3. El sistema carece de mecanismos de 'Fail-Fast' y Circuit Breaker, permitiendo que peticiones se retengan 30 segundos "
    "degradando toda la infraestructura compartida."
)

doc.add_paragraph().paragraph_format.space_after = Pt(10)

# ==================== 6. RECOMENDACIONES TÉCNICAS ====================
h6 = doc.add_heading(level=1)
r_h6 = h6.add_run("6. Recomendaciones Técnicas y Plan de Acción")
r_h6.font.color.rgb = COLOR_PRIMARY
r_h6.font.bold = True

p_rec = doc.add_paragraph()
p_rec.add_run(
    "Se recomienda al equipo de arquitectura y desarrollo implementar con carácter prioritario:\n\n"
    "1. Capa de Persistencia y Base de Datos:\n"
    "   • Dimensionar el pool de conexiones (HikariCP) e implementar timeout de conexión agresivo (máximo 3,000 ms).\n"
    "   • Desviar el tráfico de consulta de saldo hacia Réplicas de Lectura (Read-Only Replicas) para aislarlo de transacciones de escritura.\n"
    "   • Optimizar índices en tablas de balances y movimientos de cuenta.\n\n"
    "2. Resiliencia de Microservicios:\n"
    "   • Implementar Circuit Breaker (Resilience4j / Spring Cloud) para abrir el circuito ante latencias superiores a 2s.\n"
    "   • Reducir el proxy read timeout del API Gateway de 30 segundos a un máximo de 5 segundos.\n"
    "   • Configurar Auto-escalado Horizontal (HPA) en Kubernetes basado en tasa de peticiones y latencia.\n\n"
    "3. Almacenamiento en Caché Distribuida:\n"
    "   • Incorporar Redis Cache con TTL de 15 a 30 segundos para balances frecuentes, absorbiendo hasta el 70% de la carga.\n\n"
    "4. Prueba de Re-certificación:\n"
    "   • Ejecutar una nueva prueba de carga de 140 VUs por 60 minutos con criterios de aceptación estrictos: "
    "error < 0.5%, P95 < 1.0s, tiempo máximo < 3.0s y cero caídas de throughput."
)

# Guardar documento docx
out_docx = r"D:\Prueba_tecnica_tata\reto_tecnico_qa_tcs\Ejercicio_Performance\Ejercicio_2_Analisis_Resultados\InformeResultados.docx"
out_doc = r"D:\Prueba_tecnica_tata\reto_tecnico_qa_tcs\Ejercicio_Performance\Ejercicio_2_Analisis_Resultados\InformeResultados.doc"

doc.save(out_docx)
shutil.copyfile(out_docx, out_doc)
print(f"Documento DOCX generado: {out_docx}")
print(f"Documento DOC generado: {out_doc}")

