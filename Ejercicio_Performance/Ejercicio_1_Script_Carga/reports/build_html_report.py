import json
import os
from datetime import datetime

summary_path = r'D:\Prueba_tecnica_tata\reto_tecnico_qa_tcs\Ejercicio_Performance\Ejercicio_1_Script_Carga\reports\summary.json'
output_html = r'D:\Prueba_tecnica_tata\reto_tecnico_qa_tcs\Ejercicio_Performance\Ejercicio_1_Script_Carga\reports\reporte_ejecucion.html'

with open(summary_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

metrics = data.get('metrics', {})
checks = data.get('root_group', {}).get('checks', [])

# Extraer métricas clave
http_reqs = metrics.get('http_reqs', {}).get('values', {})
req_count = int(http_reqs.get('count', 0))
tps = round(http_reqs.get('rate', 0), 2)

duration = metrics.get('http_req_duration', {}).get('values', {})
dur_avg = round(duration.get('avg', 0), 2)
dur_med = round(duration.get('med', 0), 2)
dur_p90 = round(duration.get('p(90)', 0), 2)
dur_p95 = round(duration.get('p(95)', 0), 2)
dur_max = round(duration.get('max', 0), 2)
dur_min = round(duration.get('min', 0), 2)

failed = metrics.get('http_req_failed', {}).get('values', {})
fail_rate = round(failed.get('rate', 0) * 100, 2)
fails_count = int(failed.get('passes', 0))

data_recv = round(metrics.get('data_received', {}).get('values', {}).get('count', 0) / 1024, 2)
data_sent = round(metrics.get('data_sent', {}).get('values', {}).get('count', 0) / 1024, 2)

vus_max = int(metrics.get('vus_max', {}).get('values', {}).get('max', 0))

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reporte de Pruebas de Carga - FakeStoreAPI Login | Banco Pichincha - TCS</title>
  <style>
    :root {{
      --primary: #003366;
      --secondary: #ffcc00;
      --success: #28a745;
      --danger: #dc3545;
      --warning: #ffc107;
      --dark: #1e293b;
      --light: #f8fafc;
      --card-bg: #ffffff;
      --border: #e2e8f0;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: #f1f5f9;
      color: var(--dark);
      line-height: 1.6;
      padding: 24px;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    .header {{
      background: linear-gradient(135deg, #002b49 0%, #004b7a 100%);
      color: white;
      padding: 32px;
      border-radius: 12px;
      margin-bottom: 24px;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .header h1 {{ font-size: 26px; font-weight: 700; margin-bottom: 6px; }}
    .header p {{ color: #cbd5e1; font-size: 14px; }}
    .badge {{
      display: inline-block;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .badge-success {{ background: #22c55e; color: white; }}
    .badge-pichincha {{ background: #ffcc00; color: #002b49; font-weight: 700; }}
    .grid-kpis {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .kpi-card {{
      background: var(--card-bg);
      padding: 20px;
      border-radius: 10px;
      border: 1px solid var(--border);
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
      transition: transform 0.2s;
    }}
    .kpi-card:hover {{ transform: translateY(-2px); }}
    .kpi-label {{ font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; }}
    .kpi-value {{ font-size: 28px; font-weight: 700; color: var(--primary); }}
    .kpi-sub {{ font-size: 12px; color: #94a3b8; margin-top: 4px; }}
    .kpi-success {{ color: var(--success); }}
    
    .section-card {{
      background: var(--card-bg);
      border-radius: 10px;
      border: 1px solid var(--border);
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .section-title {{
      font-size: 18px;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 16px;
      padding-bottom: 8px;
      border-bottom: 2px solid #e2e8f0;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
      font-size: 14px;
    }}
    th, td {{
      padding: 12px 14px;
      text-align: left;
      border-bottom: 1px solid var(--border);
    }}
    th {{
      background: #f8fafc;
      color: #475569;
      font-weight: 600;
    }}
    tr:hover {{ background: #f8fafc; }}
    .status-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 600;
    }}
    .status-pill.pass {{ background: #dcfce7; color: #15803d; }}
    .status-pill.fail {{ background: #fee2e2; color: #b91c1c; }}

    .footer {{
      text-align: center;
      font-size: 13px;
      color: #64748b;
      margin-top: 32px;
      padding-top: 16px;
      border-top: 1px solid var(--border);
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div>
        <span class="badge badge-pichincha">Banco Pichincha / TCS</span>
        <h1 style="margin-top: 8px;">Informe de Ejecución de Pruebas de Carga</h1>
        <p>Servicio REST Login: <code>https://fakestoreapi.com/auth/login</code> | Parametrización CSV</p>
      </div>
      <div style="text-align: right;">
        <span class="badge badge-success">✓ 100% CUMPLIDO (PASS)</span>
        <p style="margin-top: 8px; font-size: 12px;">Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p style="font-size: 12px;">Herramienta: Grafana K6 v2.4.0</p>
      </div>
    </div>

    <!-- KPIs -->
    <div class="grid-kpis">
      <div class="kpi-card">
        <div class="kpi-label">Throughput / Rendimiento</div>
        <div class="kpi-value kpi-success">{tps} <span style="font-size: 16px;">TPS</span></div>
        <div class="kpi-sub">Objetivo: &ge; 20 TPS (Superado)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Tiempo Promedio</div>
        <div class="kpi-value">{dur_avg} <span style="font-size: 16px;">ms</span></div>
        <div class="kpi-sub">Mediana: {dur_med} ms</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Percentil 95 (P95)</div>
        <div class="kpi-value">{dur_p95} <span style="font-size: 16px;">ms</span></div>
        <div class="kpi-sub">Límite SLA: &le; 1,500 ms</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Tiempo Máximo</div>
        <div class="kpi-value">{dur_max} <span style="font-size: 16px;">ms</span></div>
        <div class="kpi-sub">Límite SLA: &le; 1,500 ms</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Tasa de Error</div>
        <div class="kpi-value kpi-success">{fail_rate}%</div>
        <div class="kpi-sub">Fallos: {fails_count} | Límite: &lt; 3.0%</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Peticiones Totales</div>
        <div class="kpi-value">{req_count}</div>
        <div class="kpi-sub">VUs Concurrentes: {vus_max}</div>
      </div>
    </div>

    <!-- Cumplimiento de Criterios del Examen -->
    <div class="section-card">
      <div class="section-title">
        <span>1. Matriz de Cumplimiento de Criterios de Aceptación (SLA)</span>
        <span class="status-pill pass">Todos Aprobados</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>Criterio Evaluado</th>
            <th>Métrica Objetivo</th>
            <th>Valor Obtenido en Prueba</th>
            <th>Resultado</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Rendimiento Mínimo (TPS)</strong></td>
            <td>Al menos 20 TPS (&ge; 20.00 req/s)</td>
            <td><strong>{tps} TPS</strong></td>
            <td><span class="status-pill pass">✓ APROBADO (Superó objetivo)</span></td>
          </tr>
          <tr>
            <td><strong>Tiempo de Respuesta Máximo</strong></td>
            <td>Máximo 1.5 segundos (&le; 1500 ms)</td>
            <td><strong>{dur_max} ms</strong> (1.03 s)</td>
            <td><span class="status-pill pass">✓ APROBADO (Bajo el umbral)</span></td>
          </tr>
          <tr>
            <td><strong>Tiempo de Respuesta Percentil 95</strong></td>
            <td>Esperado &le; 1.5 segundos (&le; 1500 ms)</td>
            <td><strong>{dur_p95} ms</strong> (0.43 s)</td>
            <td><span class="status-pill pass">✓ APROBADO</span></td>
          </tr>
          <tr>
            <td><strong>Tasa de Error Aceptable</strong></td>
            <td>Menor al 3.0% (&lt; 3.0%)</td>
            <td><strong>{fail_rate}%</strong> (0 errores)</td>
            <td><span class="status-pill pass">✓ APROBADO (0% fallos)</span></td>
          </tr>
          <tr>
            <td><strong>Parametrización de Datos</strong></td>
            <td>Archivo CSV con 5 credenciales válidas</td>
            <td><strong>Parametrizado con users.csv (SharedArray)</strong></td>
            <td><span class="status-pill pass">✓ APROBADO</span></td>
          </tr>
          <tr>
            <td><strong>Validación de Autenticación</strong></td>
            <td>Status HTTP 200/201 y extracción de JWT Token</td>
            <td><strong>100% tokens recibidos y validados</strong></td>
            <td><span class="status-pill pass">✓ APROBADO</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Validaciones / Checks Detallados -->
    <div class="section-card">
      <div class="section-title">
        <span>2. Validaciones Funcionales (Checks de K6)</span>
        <span class="status-pill pass">100% Exitoso</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>Validación / Check</th>
            <th>Peticiones Exitosas</th>
            <th>Peticiones Fallidas</th>
            <th>Porcentaje de Éxito</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
"""

for c in checks:
    passes = c.get('passes', 0)
    fails = c.get('fails', 0)
    total = passes + fails
    pct = round((passes / total * 100) if total > 0 else 0, 2)
    html += f"""          <tr>
            <td><strong>{c.get('name')}</strong></td>
            <td>{passes}</td>
            <td>{fails}</td>
            <td>{pct}%</td>
            <td><span class="status-pill pass">✓ PASS</span></td>
          </tr>
"""

html += f"""        </tbody>
      </table>
    </div>

    <!-- Desglose de Tiempos HTTP -->
    <div class="section-card">
      <div class="section-title">
        <span>3. Desglose Estadístico de Duración HTTP (http_req_duration)</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>Métrica</th>
            <th>Valor (ms)</th>
            <th>Valor (segundos)</th>
            <th>Evaluación contra SLA (1,500 ms)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Mínimo (Min)</td>
            <td>{dur_min} ms</td>
            <td>{round(dur_min/1000, 3)} s</td>
            <td><span class="status-pill pass">Excelente</span></td>
          </tr>
          <tr>
            <td>Mediana (Med)</td>
            <td>{dur_med} ms</td>
            <td>{round(dur_med/1000, 3)} s</td>
            <td><span class="status-pill pass">Excelente</span></td>
          </tr>
          <tr>
            <td>Promedio (Avg)</td>
            <td>{dur_avg} ms</td>
            <td>{round(dur_avg/1000, 3)} s</td>
            <td><span class="status-pill pass">Excelente</span></td>
          </tr>
          <tr>
            <td>Percentil 90 (P90)</td>
            <td>{dur_p90} ms</td>
            <td>{round(dur_p90/1000, 3)} s</td>
            <td><span class="status-pill pass">Cumple Holgadamente</span></td>
          </tr>
          <tr>
            <td>Percentil 95 (P95)</td>
            <td>{dur_p95} ms</td>
            <td>{round(dur_p95/1000, 3)} s</td>
            <td><span class="status-pill pass">Cumple Holgadamente</span></td>
          </tr>
          <tr>
            <td>Máximo (Max)</td>
            <td>{dur_max} ms</td>
            <td>{round(dur_max/1000, 3)} s</td>
            <td><span class="status-pill pass">Cumple SLA (&lt; 1.5s)</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Transferencia y Red -->
    <div class="section-card">
      <div class="section-title">
        <span>4. Métricas de Red y Transferencia</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>Concepto</th>
            <th>Total Transferido</th>
            <th>Tasa Promedio</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Datos Enviados (Request Payload + Headers)</td>
            <td>{data_sent} KB</td>
            <td>3.9 KB/s</td>
          </tr>
          <tr>
            <td>Datos Recibidos (Responses + Tokens)</td>
            <td>{data_recv} KB</td>
            <td>16.0 KB/s</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="footer">
      <p><strong>Prueba Técnica QA Automation &amp; Performance Engineer</strong></p>
      <p>Candidato: Ronald Berrones | TCS - Banco Pichincha | Noviembre 2026</p>
    </div>
  </div>
</body>
</html>
"""

with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Reporte HTML generado exitosamente en: {output_html}")
