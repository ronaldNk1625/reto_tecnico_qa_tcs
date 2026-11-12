# 🚀 Prueba Técnica QA Automation & Performance - Banco Pichincha / TCS

Repositorio que contiene la solución completa de la prueba técnica práctica para el rol de **QA Automation & Performance Engineer** para **Banco Pichincha** a través de **TCS (Tata Consultancy Services)**.

---

## 📂 Estructura General del Repositorio

El examen técnico práctico está compuesto por 3 módulos completos:

```text
reto_tecnico_qa_tcs/
│
├── Ejercicio_E2E/                  # Módulo 1: Automatización E2E en Demoblaze
│   ├── src/test/java/...           # Screenplay Pattern (Tasks, UI, Model, Questions, Steps)
│   ├── src/test/resources/...      # Features en Gherkin, serenity.conf y datos JSON/CSV
│   ├── pom.xml                     # Configuración de Maven y Serenity BDD 4.1.20
│   ├── readme.txt                  # Instrucciones paso a paso de ejecución (Requerido)
│   ├── README.md                   # Documentación detallada en Markdown con diagramas
│   ├── conclusiones.txt            # Hallazgos y conclusiones técnicas (Requerido)
│   └── conclusiones.md             # Informe técnico detallado
│
├── Ejercicio_API/                  # Módulo 2: Automatización de APIs con Karate Framework
│   ├── src/test/java/...           # karate-config.js, features, ApiRunner.java
│   ├── src/test/resources/...      # Datos JSON y CSV para Scenario Outline
│   ├── pom.xml                     # Karate 1.4.1 + JUnit 5 + Maven
│   ├── readme.txt                  # Instrucciones paso a paso de ejecución (Requerido)
│   ├── README.md                   # Documentación detallada en Markdown
│   ├── conclusiones.txt            # Hallazgos y conclusiones técnicas (Requerido)
│   └── conclusiones.md             # Informe técnico detallado
│
├── Ejercicio_Performance/          # Módulo 3: Pruebas de Carga y Análisis de Rendimiento
│   ├── Ejercicio_1_Script_Carga/   # Script de Carga (Login FakeStoreAPI) en K6 y JMeter
│   │   ├── data/users.csv          # Parametrización con credenciales CSV
│   │   ├── scripts/...             # k6_login_load_test.js y jmeter_login_load_test.jmx
│   │   ├── reports/...             # reporte_ejecucion.html, summary.txt, summary.json
│   │   ├── readme.txt              # Instrucciones paso a paso con versiones
│   │   └── conclusiones.txt        # Hallazgos y conclusiones del ejercicio de carga
│   ├── Ejercicio_2_Analisis_Resultados/ # Análisis de Resultados (App Transaction Balance)
│   │   ├── InformeResultados.doc   # Informe oficial en Word (Requerido)
│   │   ├── InformeResultados.docx  # Documento Word enriquecido con imágenes
│   │   ├── InformeResultados.md    # Versión Markdown para lectura directa
│   │   └── insumos/...             # textSummary.txt y gráficas de monitoreo
│   ├── readme.txt                  # Instrucciones consolidadas
│   ├── conclusiones.txt            # Conclusiones consolidadas
│   └── README.md                   # Documentación detallada en Markdown
│
├── Ejercicio_E2E.zip               # Zip del módulo E2E (entregable)
├── Ejercicio_API.zip               # Zip del módulo API (entregable)
├── Ejercicio_Performance.zip       # Zip del módulo Performance (entregable)
├── .gitignore                      # Archivos y directorios excluidos de Git
└── README.md                       # Documentación general de la prueba técnica
```

---

## 📌 Módulo 1 - Automatización E2E (Demoblaze)

- **Sitio Bajo Prueba:** [Demoblaze Store](https://www.demoblaze.com/)
- **Framework Implementado:** **Serenity BDD 4.1.20 + Cucumber 7 + Screenplay Pattern + Java 17 + Maven**
- **Navegador Soportado:** Google Chrome (Headless y modo interactivo)
- **Estrategia de Datos:** Data-Driven Testing (Gherkin Scenario Outline, JSON y CSV)
- **Estado de Ejecución:** ✅ **100% Exitoso (5/5 tests passing)**
- **Reportes:** 
  - Serenity Living Documentation con capturas de pantalla automáticas (`target/site/serenity/index.html`).
  - Cucumber Reports HTML y JSON (`target/cucumber-reports/`).

👉 Consulte el directorio [`Ejercicio_E2E/`](Ejercicio_E2E/) para las instrucciones detalladas.

---

## 📌 Módulo 2 - Automatización de APIs (Demoblaze API)

- **API Bajo Prueba:** [api.demoblaze.com](https://api.demoblaze.com) — endpoints `/signup` y `/login`
- **Framework Implementado:** **Karate Framework 1.4.1 + JUnit 5 + Maven**
- **Métodos Cubiertos:** POST `/signup` y POST `/login`
- **Estrategia de Datos:** Data-Driven Testing (Scenario Outline, JSON y CSV)
- **Estado de Ejecución:** ✅ **100% Exitoso (13/13 escenarios, 26 runs)**
- **Reporte:** Karate HTML report (`target/karate-reports/karate-summary.html`)

| Feature | Escenarios | Estado |
|---|---|---|
| signup.feature | 6 | ✅ Todos pasaron |
| login.feature | 7 | ✅ Todos pasaron |

👉 Consulte el directorio [`Ejercicio_API/`](Ejercicio_API/) para las instrucciones detalladas.

---

## 📌 Módulo 3 - Pruebas de Carga y Rendimiento (Performance Testing)

### 3.1. Ejercicio 1: Script de Pruebas de Carga (Login)
- **Endpoint:** `POST https://fakestoreapi.com/auth/login`
- **Herramientas Implementadas:** **Grafana K6 v2.4.0** (script automatizado) y **Apache JMeter 5.6.3** (`.jmx`).
- **Parametrización:** Archivo CSV con 5 cuentas de usuario.
- **Resultados Obtenidos:**
  - **Throughput:** **21.77 TPS** (SLA: &ge; 20 TPS) ✅
  - **Tiempo de Respuesta Máximo:** **1.03 s** (SLA: &le; 1.50 s) ✅
  - **Percentil 95 (P95):** **0.43 s (438 ms)** (SLA: &le; 1.50 s) ✅
  - **Tasa de Error:** **0.00% con 0 fallos** (SLA: &lt; 3.00%) ✅
  - **Checks de Validación:** **100% tokens extraídos exitosamente** ✅
- **Reportes Generados:** Dashboard HTML interactivo, texto plano y JSON.

### 3.2. Ejercicio 2: Análisis de Resultados (App Transaction Balance)
- **Entregable Oficial:** [`InformeResultados.doc`](Ejercicio_Performance/Ejercicio_2_Analisis_Resultados/InformeResultados.doc) (también disponible en [`.docx`](Ejercicio_Performance/Ejercicio_2_Analisis_Resultados/InformeResultados.docx) y [`.md`](Ejercicio_Performance/Ejercicio_2_Analisis_Resultados/InformeResultados.md)).
- **Hallazgos Clave:**
  - Identificación del incidente crítico de caída de rendimiento entre las **01:51:00 y las 01:58:00 (7 minutos de duración)**.
  - Relación matemática de VUs vs TPS: los 140 VUs se mantuvieron constantes mientras el tiempo de respuesta subió a **29.93 segundos**, provocando el colapso del throughput a **10-15 req/s**.
  - Concentración del **88.58% de todos los errores (5,987 fallos HTTP 5xx)** en Stage 1 durante la ventana crítica (~80% de indisponibilidad temporal).
  - Causa Raíz: Agotamiento de pool de conexiones a BD, contención de bloqueos transaccionales en tablas de saldo, timeout de 30s en API Gateway y reinicio de pods.
  - Recomendaciones: Circuit Breaker (Resilience4j), réplicas de lectura de BD, caché Redis con TTL corto y reducción de timeouts.

👉 Consulte el directorio [`Ejercicio_Performance/`](Ejercicio_Performance/) para las instrucciones detalladas y acceso a los reportes.

---

## 👤 Información del Candidato

- **Nombre:** Ronald Berrones
- **Rol:** QA Automation & Performance Engineer
- **Empresa Contratante:** Banco Pichincha / TCS (Tata Consultancy Services)
- **Fecha:** Noviembre 2026
