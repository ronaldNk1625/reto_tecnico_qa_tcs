# ⚡ Módulo de Performance & Pruebas de Carga - Banco Pichincha / TCS

Este directorio contiene la solución completa de la sección de **Performance Testing** de la prueba técnica para el rol de **QA Automation & Performance Engineer** (Banco Pichincha / TCS).

---

## 📁 Estructura del Módulo

```text
Ejercicio_Performance/
│
├── Ejercicio_1_Script_Carga/               # Ejercicio 1: Script y ejecución de carga (Login)
│   ├── data/
│   │   └── users.csv                       # Archivo CSV con 5 credenciales parametrizadas
│   ├── scripts/
│   │   ├── k6_login_load_test.js           # Script de carga en Grafana K6 (SharedArray + Thresholds)
│   │   └── jmeter_login_load_test.jmx      # Script de carga en Apache JMeter 5.6.3
│   ├── reports/
│   │   ├── reporte_ejecucion.html          # Dashboard interactivo HTML generado
│   │   ├── summary.txt                     # Resumen de métricas en texto plano
│   │   ├── summary.json                    # Datos crudos de métricas en formato JSON
│   │   └── build_html_report.py            # Generador del dashboard HTML
│   ├── readme.txt                          # Instrucciones paso a paso de ejecución (Requerido)
│   └── conclusiones.txt                    # Hallazgos y conclusiones de la prueba de carga (Requerido)
│
├── Ejercicio_2_Analisis_Resultados/        # Ejercicio 2: Análisis técnico de resultados de carga
│   ├── InformeResultados.doc               # Documento oficial en formato Word (Requerido)
│   ├── InformeResultados.docx              # Copia Word DOCX con formato enriquecido
│   ├── InformeResultados.md                # Versión en Markdown para lectura en GitHub / IDE
│   ├── generate_word_report.py             # Script de automatización generador del documento Word
│   └── insumos/
│       ├── textSummary.txt                 # Resumen de resultados K6 del ejercicio
│       ├── textSummary_captura.png         # Captura de pantalla del textSummary provisto
│       └── grafica_monitoreo_vus_vs_rps.png # Captura del diagrama de monitoreo (VUs vs Throughput)
│
├── readme.txt                              # Instrucciones generales de la sección de Performance
├── conclusiones.txt                        # Conclusiones consolidadas del módulo
└── README.md                               # Documentación detallada en Markdown
```

---

## 🚀 Ejercicio 1: Script de Pruebas de Carga (Login)

### 1.1. Especificación del Servicio Bajo Prueba
- **Endpoint:** `POST https://fakestoreapi.com/auth/login`
- **Headers:** `Content-Type: application/json`
- **Payload:**
  ```json
  {
    "username": "user",
    "password": "passwd"
  }
  ```
- **Parametrización:** Archivo CSV [`data/users.csv`](Ejercicio_1_Script_Carga/data/users.csv) con 5 cuentas provistas en el examen.

### 1.2. Herramientas Utilizadas
- **Grafana K6 v2.4.0** (Script principal automatizado con reportes exportables).
- **Apache JMeter 5.6.3** (Script `.jmx` interoperable con CSV Data Set Config y Aserciones).

### 1.3. Resultados de la Ejecución Real

| Criterio Exigido por el Examen | SLA / Umbral | Resultado Obtenido | Estado |
|---|---|---|---|
| **Rendimiento Mínimo (TPS)** | &ge; 20 TPS | **21.77 TPS** | ✅ CUMPLE (Superado) |
| **Tiempo Máximo de Respuesta** | &le; 1.50 s (1500 ms) | **1.03 s (1030 ms)** | ✅ CUMPLE |
| **Percentil 95 (P95)** | &le; 1.50 s (1500 ms) | **0.43 s (438 ms)** | ✅ CUMPLE |
| **Tasa de Error Aceptable** | &lt; 3.00% | **0.00% (0 errores)** | ✅ CUMPLE |
| **Peticiones Totales** | N/A | **661 peticiones** | ✅ EXITOSO |
| **Checks Funcionales (Status + Token)** | &ge; 97% | **100.00% (1,983 checks)** | ✅ EXITOSO |

### 1.4. Cómo Ejecutar la Prueba con K6
```bash
cd Ejercicio_Performance/Ejercicio_1_Script_Carga/scripts
k6 run k6_login_load_test.js
```
Los reportes se actualizarán automáticamente en [`Ejercicio_1_Script_Carga/reports/`](Ejercicio_1_Script_Carga/reports/).

---

## 📊 Ejercicio 2: Análisis de Resultados de Prueba de Carga

### 2.1. Entregable Oficial
El documento oficial solicitado es **[`InformeResultados.doc`](Ejercicio_2_Analisis_Resultados/InformeResultados.doc)** (también disponible en [`.docx`](Ejercicio_2_Analisis_Resultados/InformeResultados.docx) y [`.md`](Ejercicio_2_Analisis_Resultados/InformeResultados.md)).

### 2.2. Resumen de Hallazgos y Causa Raíz

1. **Cumplimiento Aparente vs. Falla Oculta:**
   - La prueba reporta un error global del **2.44%** y checks del **97.55%**, lo que formalmente aparenta cumplir con SLAs estándar (< 3%).
   - Sin embargo, el **diagrama de monitoreo temporal** revela una **caída crítica de throughput entre las 01:51:00 y las 01:58:00 (duración de 7 minutos)**, donde las peticiones cayeron de **82 req/s a menos de 10-15 req/s**.

2. **Relación Matemática entre VUs y Throughput:**
   - Durante la caída, la cantidad de Usuarios Virtuales (VUs) se mantuvo fija en **140 VUs** (línea verde plana).
   - El tiempo de respuesta máximo subió a **29.93 segundos** (`http_req_duration max`).
   - Aplicando la ley de rendimiento:
     $$\text{Throughput} = \frac{\text{VUs}}{\text{Tiempo de Respuesta}} \approx \frac{140}{30\text{ s}} \approx 4.67\text{ req/s}$$
   - Esto demuestra que la caída de TPS se originó por el **bloqueo masivo de VUs esperando respuesta del servidor (tiempo de espera activo)**.

3. **Concentración de Errores en Stage 1:**
   - El desglose de `textSummary.txt` demuestra que **5,987 errores HTTP 5xx (el 88.58% de todos los fallos)** ocurrieron exclusivamente en el **Stage 1** durante esa ventana temporal.
   - En esa ventana de 7 minutos, la tasa local de falla fue del **~80%**, representando una indisponibilidad severa.

4. **Causa Raíz Identificada:**
   - Agotamiento del Connection Pool hacia la base de datos (HikariCP / Tomcat).
   - Bloqueos transaccionales (Row-level lock contention) en el servicio de balance.
   - Timeouts de 30 segundos en el API Gateway / Balanceador de carga (HTTP 504 Gateway Timeout).
   - Reinicio forzado del pod por consumo de memoria (Kubernetes OOMKilled), lo cual explica el rebote abrupto de throughput a las 02:00:00.

5. **Recomendaciones Clave:**
   - Reducción del Connection Timeout del pool a 3,000 ms.
   - Separación de tráfico de lectura a Read-Only Replicas de base de datos.
   - Implementación de Circuit Breaker (Resilience4j) con umbral de 2 segundos.
   - Implementación de capa de caché distribuida (Redis) con TTL corto para consultas de saldo.
   - Reducción del timeout del API Gateway a 5 segundos.

---

**Autor:** Ronald Berrones — QA Automation & Performance Engineer  
**Entidad:** Banco Pichincha / TCS — Noviembre 2026

