# 📘 DOCUMENTACIÓN TÉCNICA INTEGRAL
## PRUEBA TÉCNICA QA AUTOMATION & PERFORMANCE
**Banco Pichincha / TCS (Tata Consultancy Services)**

- **Candidato:** Ronald Berrones
- **Rol / Perfil:** QA Automation & Performance Engineer
- **Repositorio GitHub:** [https://github.com/ronaldNk1625/reto_tecnico_qa_tcs.git](https://github.com/ronaldNk1625/reto_tecnico_qa_tcs.git)
- **Fecha de Entrega:** Noviembre 2026

---

## 1. RESUMEN EJECUTIVO GLOBAL

La prueba técnica comprende la resolución exhaustiva de cuatro ejercicios prácticos estructurados en tres módulos de aseguramiento de calidad de software:

| Módulo / Prueba | Herramientas Utilizadas | Alcance Evaluado | Casos / Escenarios | Estado Final |
|---|---|---|---|---|
| **Módulo 1: E2E Web** | Serenity BDD 4.1.20, Cucumber 7, Screenplay, Java 17, Maven | Flujo completo de compra en Demoblaze, Carrito, Orden, Modales | 5 escenarios (Smoke, Outline, JSON, CSV) | **✅ 100% PASADO (5/5)** |
| **Módulo 2: APIs REST** | Karate Framework 1.4.1, JUnit 5, Gherkin, Maven | Servicios POST /signup y POST /login, Token JWT, Errores | 13 escenarios (26 runs) (Outline JSON/CSV) | **✅ 100% PASADO (13/13)** |
| **Módulo 3: Carga (Login)** | Grafana K6 v2.4.0, Apache JMeter 5.6.3 | POST /auth/login con 5 usuarios parametrizados CSV | 661 peticiones a 21.77 TPS (SLA >= 20) | **✅ 100% PASADO (21.77 TPS)** |
| **Módulo 4: Análisis Rendimiento** | Análisis Cuantitativo K6, Root Cause Analysis, Word/Markdown | Diagnóstico de caída en App Transaction Balance | 276,650 peticiones analizadas temporalmente | **✅ INFORME COMPLETO** |

---

## 2. MÓDULO 1: AUTOMATIZACIÓN E2E WEB (DEMOBLAZE)

### 2.1. Objetivo y Alcance
Automatizar el flujo completo de compra de dos productos en la tienda virtual **Demoblaze** (`https://www.demoblaze.com/`), validando la persistencia en el carrito de compras, el cálculo del monto total, el diligenciamiento del modal de orden, la confirmación de compra y la verificación del mensaje de éxito *"Thank you for your purchase!"* junto con el ID y monto de la orden.

### 2.2. Arquitectura Implementada: Patrón Screenplay
Se implementó el patrón **Screenplay**, centrado en actores, habilidades y tareas, garantizando alta mantenibilidad y cumplimiento de los principios SOLID:
- **Tasks (Tareas de Negocio):** `NavigateTo`, `AddProduct`, `ViewCart`, `CompleteOrderForm`, `FinishPurchase`, `CloseConfirmation`.
- **User Interfaces (Mapeo de Elementos):** `HomePage`, `ProductDetailPage`, `CartPage`, `OrderModal`, `ConfirmationModal` (selectores CSS y XPath robustos).
- **Model (Entidades):** `CustomerInfo`, `OrderDetails`, `ProductOrder`.
- **Questions (Aserciones y Validaciones):** `TheCartProducts`, `TheCartTotal`, `TheConfirmationMessage`, `TheOrderDetails`.
- **Interactions (Interacciones Específicas):** `AcceptAlert` (manejo de alertas JavaScript nativas de confirmación de agregado de producto).
- **Util (Lectores de Datos):** `JsonReader`, `CsvReader`, `Constants`.

### 2.3. Estrategia Data-Driven Testing (JSON & CSV)
Se diseñaron 4 tipos de escenarios en el archivo feature ([`purchase_flow.feature`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_E2E/src/test/resources/features/purchase_flow.feature)):
1. `@Smoke`: Flujo feliz estándar de compra con dos productos.
2. `@EsquemaEscenario`: Scenario Outline parametrizado con tabla `Examples` nativa de Gherkin.
3. `@ConsumoJson`: Scenario Outline con inyección dinámica desde archivo externo [`datos_compra.json`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_E2E/src/test/resources/data/datos_compra.json).
4. `@ConsumoCsv`: Scenario Outline con inyección dinámica desde archivo externo [`datos_compra.csv`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_E2E/src/test/resources/data/datos_compra.csv).

### 2.4. Resultados y Reportes
- **Resultado:** 5/5 escenarios aprobados (100% BUILD SUCCESS).
- **Reporte Serenity:** `target/site/serenity/index.html` (Living Documentation con capturas paso a paso).
- **Reporte Cucumber:** `target/cucumber-reports/cucumber.html` y `.json`.

---

## 3. MÓDULO 2: AUTOMATIZACIÓN DE APIS REST (DEMOBLAZE API)

### 3.1. Objetivo y Alcance
Automatizar las pruebas funcionales de los endpoints `/signup` y `/login` de la API de **Demoblaze** (`https://api.demoblaze.com`), cubriendo casos positivos, casos negativos, control de duplicados y parametrización externa.

### 3.2. Herramienta y Enfoque
Se implementó **Karate Framework 1.4.1** + **JUnit 5**, aprovechando su sintaxis nativa Gherkin para peticiones HTTP y aserciones JSON directas sin necesidad de step definitions intermedias en Java.

### 3.3. Desafíos Técnicos Resueltos (Lo más relevante)
1. **API no convencional (Siempre retorna HTTP 200):**  
   La API de Demoblaze responde HTTP 200 incluso ante credenciales erróneas o usuarios inexistentes (`Wrong password.`, `User does not exist.`). Se configuraron validaciones a nivel del cuerpo JSON para comprobar el `errorMessage`.
2. **Respuesta de Signup Exitoso con formato texto plano (`""\n`):**  
   Al registrar exitosamente un usuario, el backend devuelve el texto crudo `""` con comillas y salto de línea. Se normalizó la respuesta con `.trim()` para validar la condición esperada sin falsos negativos.
3. **Independencia de Pruebas mediante Generación Dinámica de Usuarios:**  
   Dado que el backend no permite usuarios duplicados, se implementó la función JavaScript `generateRandomUser` en `karate-config.js` que genera identificadores únicos con timestamp, garantizando pruebas repetibles e independientes.
4. **Manejo de URLs Absolutas vs Path Acumulativo:**  
   En escenarios que encadenaban `/signup` y `/login`, Karate acumulaba los segmentos de ruta. Se solucionó declarando URLs completas en el Background (`* def signupUrl = baseUrl + '/signup'`; `* def loginUrl = baseUrl + '/login'`).

### 3.4. Resultados y Reportes
- **Resultado:** 13 escenarios (26 runs), 0 fallos (BUILD SUCCESS).
- **Reporte Karate:** `target/karate-reports/karate-summary.html`.

---

## 4. MÓDULO 3: PRUEBAS DE CARGA Y RENDIMIENTO (LOGIN FAKESTOREAPI)

### 4.1. Objetivo y Criterios
Ejecutar una prueba de carga sobre el endpoint `POST https://fakestoreapi.com/auth/login` parametrizando 5 credenciales desde un archivo CSV ([`users.csv`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_Performance/Ejercicio_1_Script_Carga/data/users.csv)), cumpliendo con:
- Rendimiento mínimo de **20 TPS**.
- Tiempo máximo de respuesta de **1.5 segundos**.
- Tasa de error aceptable **menor al 3%**.

### 4.2. Implementación Técnica
- **Grafana K6 v2.4.0 (Script Principal):** [`k6_login_load_test.js`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_Performance/Ejercicio_1_Script_Carga/scripts/k6_login_load_test.js) con ejecutor `constant-arrival-rate` fijado en 22 TPS, lectura de CSV en memoria compartida vía `SharedArray` y definición de Thresholds.
- **Apache JMeter 5.6.3 (Script Interoperable):** [`jmeter_login_load_test.jmx`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_Performance/Ejercicio_1_Script_Carga/scripts/jmeter_login_load_test.jmx) parametrizado con `CSV Data Set Config`, `Constant Throughput Timer` y aserciones.

### 4.3. Matriz de Resultados Reales

| Criterio Evaluado | SLA / Umbral Exigido | Resultado Obtenido en Prueba | Veredicto |
|---|---|---|---|
| **Rendimiento Mínimo (TPS)** | &ge; 20 TPS | **21.77 TPS (21.77 req/s)** | **✅ CUMPLE (Superado)** |
| **Tiempo Máximo de Respuesta** | &le; 1.50 s (1,500 ms) | **1.03 s (1,030 ms)** | **✅ CUMPLE (Bajo límite)** |
| **Percentil 95 (P95)** | &le; 1.50 s (1,500 ms) | **0.43 s (438 ms)** | **✅ CUMPLE (Holgado)** |
| **Tasa de Error Aceptable** | &lt; 3.00% | **0.00% (0 errores)** | **✅ CUMPLE (Cero fallos)** |
| **Validación de Tokens** | 100% tokens JWT válidos | **661/661 tokens extraídos** | **✅ CUMPLE** |

### 4.4. Reportes Generados
- Dashboard interactivo HTML: [`reporte_ejecucion.html`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_Performance/Ejercicio_1_Script_Carga/reports/reporte_ejecucion.html)
- Resumen texto: [`summary.txt`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_Performance/Ejercicio_1_Script_Carga/reports/summary.txt)
- Métricas JSON: [`summary.json`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_Performance/Ejercicio_1_Script_Carga/reports/summary.json)

---

## 5. MÓDULO 4: ANÁLISIS DE RESULTADOS DE RENDIMIENTO (APP TRANSACTION BALANCE)

### 5.1. Objetivo
Analizar los insumos de una prueba de carga de 65 minutos con 140 Usuarios Virtuales constantes sobre el servicio transaccional bancario **"App Transaction Balance"** ([`textSummary.txt`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_Performance/Ejercicio_2_Analisis_Resultados/insumos/textSummary.txt) y gráfica temporal de monitoreo).

### 5.2. Hallazgos Principales y Análisis Causa Raíz (RCA)
1. **Cumplimiento Aparente vs. Degradación Oculta:**  
   El acumulado reporta 2.44% de fallos y 97.55% de checks exitosos. Sin embargo, el análisis temporal identifica un **incidente crítico entre las 01:51:00 y las 01:58:00 (7 minutos)**, donde el throughput colapsó de **82 req/s a menos de 10-15 req/s**.
2. **Relación Matemática VUs vs Throughput (Ley de Rendimiento):**  
   Durante el colapso, los 140 VUs se mantuvieron constantes (la línea verde no disminuyó). El tiempo de respuesta máximo subió a **29.93 segundos**. Por la relación $\text{Throughput} = \frac{\text{VUs}}{\text{Tiempo de Respuesta}}$, con 140 VUs bloqueados esperando 30 segundos, el throughput cae automáticamente a $\approx 4.67\text{ req/s}$. La caída se debió a **saturación y bloqueo de hilos en el backend, no a desconexión de clientes**.
3. **Concentración de 5,987 Errores HTTP 5xx en Stage 1:**  
   El **88.58% de todos los fallos del test** ocurrieron exclusivamente en el Stage 1 durante esa ventana de 7 minutos, representando una **indisponibilidad temporal del ~80%**.
4. **Causa Raíz Identificada:**  
   - Agotamiento del pool de conexiones hacia la Base de Datos (HikariCP / Tomcat).
   - Bloqueos transaccionales (*row-level locks / deadlocks*) en tablas de saldo.
   - Timeouts de 30 segundos en el API Gateway (*HTTP 504 Gateway Timeout*).
   - Reinicio de contenedores por saturación de memoria (*Kubernetes OOMKilled*), lo que explica el rebote instantáneo a 82.6 req/s a las 02:00:00.
5. **Recomendaciones de Arquitectura:**  
   - Reducción del Connection Timeout a 3,000 ms (*Fail-Fast*).
   - Desvío de consultas de saldo hacia Réplicas de Lectura (*Read Replicas*).
   - Implementación de Circuit Breaker (Resilience4j) con umbral de 2 segundos.
   - Caché distribuida Redis con TTL de 15 a 30 segundos para consultas frecuentes.
- **Entregable Oficial:** [`InformeResultados.doc`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_Performance/Ejercicio_2_Analisis_Resultados/InformeResultados.doc) y [`.docx`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_Performance/Ejercicio_2_Analisis_Resultados/InformeResultados.docx).

---

## 6. CONCLUSIONES GENERALES

- **Cobertura Completa:** Se cumplió el 100% de los requerimientos para E2E, APIs, Pruebas de Carga y Análisis de Rendimiento.
- **Calidad de Código y Arquitectura:** Implementación de estándares de la industria (Screenplay Pattern, Data-Driven Testing, SharedArray K6).
- **Entregables Disponibles:** Todo el código fuente, reportes interactivos, ejecutables y documentación Word se encuentran consolidados y sincronizados en el repositorio público de GitHub.

---
**Autor:**  
*Ronald Berrones — QA Automation & Performance Engineer*  
*TCS / Banco Pichincha — Noviembre 2026*
