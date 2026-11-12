# 📑 INFORME GENERAL CONSOLIDADO DE PRUEBAS TÉCNICAS
## QA AUTOMATION & PERFORMANCE
**Banco Pichincha / TCS (Tata Consultancy Services)**

- **Candidato:** Ronald Berrones
- **Rol / Perfil:** QA Automation & Performance Engineer
- **Repositorio Oficial GitHub:** [https://github.com/ronaldNk1625/reto_tecnico_qa_tcs.git](https://github.com/ronaldNk1625/reto_tecnico_qa_tcs.git)
- **Fecha:** Noviembre 2026

---

## 1. RESUMEN EJECUTIVO Y MATRIZ CONSOLIDADA

El presente informe consolida los resultados técnicos, arquitecturas, metodologías y hallazgos obtenidos en la ejecución de los tres componentes evaluados en la prueba técnica práctica para el rol de QA Automation & Performance Engineer:

| Módulo de Prueba | Tecnologías y Frameworks | Alcance y Servicios | Escenarios / Métricas | Veredicto |
|---|---|---|---|---|
| **Módulo 1: E2E Web** | Serenity BDD 4.1.20, Cucumber 7, Screenplay, Java 17, Maven | Demoblaze (https://www.demoblaze.com/): Carrito, Total, Modal Orden y Confirmación | 5 escenarios (Smoke, Outline, JSON, CSV) | **✅ 100% APROBADO (5/5)** |
| **Módulo 2: APIs REST** | Karate Framework 1.4.1, JUnit 5, Gherkin, Maven | Demoblaze API (https://api.demoblaze.com): POST /signup y POST /login | 13 escenarios (26 runs) (Data-Driven JSON/CSV) | **✅ 100% APROBADO (13/13)** |
| **Módulo 3: Performance** | Grafana K6 v2.4.0, Apache JMeter 5.6.3, Python | FakeStoreAPI (POST /auth/login) y Análisis App Transaction Balance | 21.77 TPS (SLA >= 20), 0% error, Informe RCA | **✅ 100% APROBADO (Todos SLAs)** |

---

## 2. INFORME DE LA PRUEBA E2E (WEB DEMOBLAZE)

### 2.1. Objetivo y Alcance
Automatizar el flujo integral de compra en el aplicativo **Demoblaze** (`https://www.demoblaze.com/`), consistente en:
- Navegar al catálogo y seleccionar dos productos (*Samsung galaxy s6* y *Nokia lumia 1520*).
- Agregarlos al carrito de compras aceptando las alertas nativas de confirmación.
- Verificar que ambos artículos figuren en la tabla del carrito con sus respectivos precios.
- Comprobar la sumatoria del total acumulado ($1180).
- Completar el formulario de compra (*Place Order*) y validar el mensaje de éxito *"Thank you for your purchase!"* junto con el ID de la orden y monto cobrado.

### 2.2. Arquitectura Implementada: Patrón Screenplay
Se implementó el patrón **Screenplay**, centrado en actores, habilidades y tareas, garantizando alta mantenibilidad y cumplimiento de los principios SOLID:
- **Tasks (Tareas de Negocio):** `NavigateTo`, `AddProduct`, `ViewCart`, `CompleteOrderForm`, `FinishPurchase`, `CloseConfirmation`.
- **User Interfaces (Mapeo de Elementos):** `HomePage`, `ProductDetailPage`, `CartPage`, `OrderModal`, `ConfirmationModal` (selectores CSS y XPath robustos).
- **Interactions (Interacciones Específicas):** `AcceptAlert` para la captura y aceptación síncrona de las alertas nativas de JavaScript que emite Demoblaze.
- **Questions (Aserciones y Validaciones):** `TheCartProducts`, `TheCartTotal`, `TheConfirmationMessage`, `TheOrderDetails`.
- **Model (Entidades):** `CustomerInfo`, `OrderDetails`, `ProductOrder`.
- **Util (Lectores de Datos):** `JsonReader`, `CsvReader`, `Constants`.

### 2.3. Estrategia Data-Driven Testing (Gherkin, JSON y CSV)
El archivo feature ([`purchase_flow.feature`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_E2E/src/test/resources/features/purchase_flow.feature)) fue estructurado con 4 enfoques de ejecución:
1. `@Smoke`: Flujo feliz estándar de compra.
2. `@EsquemaEscenario`: Scenario Outline parametrizado con tabla `Examples` nativa de Gherkin.
3. `@ConsumoJson`: Scenario Outline que lee dinámicamente el archivo externo [`datos_compra.json`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_E2E/src/test/resources/data/datos_compra.json).
4. `@ConsumoCsv`: Scenario Outline que lee dinámicamente el archivo externo [`datos_compra.csv`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_E2E/src/test/resources/data/datos_compra.csv).

### 2.4. Resultados y Reportes
- **Resultado:** 5/5 escenarios pasados exitosamente (**100% BUILD SUCCESS**).
- **Reportes:** Serenity Living Documentation (`target/site/serenity/index.html`) con capturas paso a paso y Cucumber Reports en HTML y JSON.

---

## 3. INFORME DE LA PRUEBA DE APIS REST (DEMOBLAZE API)

### 3.1. Objetivo y Alcance
Automatizar y verificar los endpoints REST de autenticación y registro de **Demoblaze** (`https://api.demoblaze.com`):
- `POST /signup`: Registro de usuarios y control de duplicados.
- `POST /login`: Autenticación de usuarios válidos, extracción de token de sesión y manejo de credenciales erróneas.

### 3.2. Herramienta y Enfoque
Se implementó **Karate Framework 1.4.1** + **JUnit 5**, permitiendo redactar los contratos de prueba en sintaxis BDD (Gherkin), combinando peticiones HTTP, aserciones sobre payloads JSON y funciones utilitarias JavaScript en un solo archivo feature.

### 3.3. Desafíos Técnicos Resueltos (Lo más relevante)
1. **API no convencional (Retorno permanente de HTTP 200):**  
   La API responde HTTP 200 incluso ante credenciales incorrectas (*"Wrong password."*) o usuarios inexistentes (*"User does not exist."*). Se implementaron aserciones sobre el objeto JSON de respuesta (`response.errorMessage`) para certificar el negocio.
2. **Respuesta de Signup Exitoso con comillas y salto de línea (`""\n`):**  
   Al crear un usuario nuevo, el endpoint devuelve el texto plano `""` seguido de un salto de línea. Se normalizó la cadena aplicando `.trim()` para validar la respuesta exacta sin inducir falsos negativos.
3. **Independencia y Repetibilidad mediante Generación Dinámica de Usuarios:**  
   Dado que el backend rechaza registros con usernames repetidos, se implementó en `karate-config.js` la función `generateRandomUser` (timestamp + aleatorio), asegurando que cada escenario cree un usuario único y los tests se puedan ejecutar indefinidamente sin colisiones.
4. **Desacoplamiento de Rutas (Evitar acumulación de paths en Karate):**  
   En escenarios que encadenan `/signup` y luego `/login`, Karate acumula los paths. Se declaró en el Background la URL completa (`* def signupUrl = baseUrl + '/signup'`; `* def loginUrl = baseUrl + '/login'`) garantizando llamadas exactas.

### 3.4. Resultados y Reportes
- **Resultado:** 13 escenarios ejecutados (26 runs por política de reintento de Surefire), 0 fallos (**100% BUILD SUCCESS**).
- **Reporte:** Karate HTML Report en `target/karate-reports/karate-summary.html`.

---

## 4. INFORME DE LA PRUEBA DE PERFORMANCE & CARGA

El módulo de rendimiento abarca dos componentes complementarios:

### 4.1. Ejercicio 1: Script y Ejecución de Carga (Login FakeStoreAPI)
- **Endpoint Evaluado:** `POST https://fakestoreapi.com/auth/login`
- **Parametrización:** Archivo CSV ([`users.csv`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_Performance/Ejercicio_1_Script_Carga/data/users.csv)) con 5 cuentas de usuario cargadas eficientemente en memoria mediante `SharedArray` de K6 (< 45 MB RAM).
- **Herramientas Implementadas:**
  - **Grafana K6 v2.4.0 (Script Principal):** [`k6_login_load_test.js`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_Performance/Ejercicio_1_Script_Carga/scripts/k6_login_load_test.js) con ejecutor `constant-arrival-rate` fijado en 22 TPS.
  - **Apache JMeter 5.6.3 (Script Interoperable):** [`jmeter_login_load_test.jmx`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_Performance/Ejercicio_1_Script_Carga/scripts/jmeter_login_load_test.jmx) con `CSV Data Set Config` y temporizador de throughput (22 TPS).
- **Matriz de Cumplimiento de SLAs:**

| Criterio Evaluado | SLA / Umbral Exigido | Resultado Real en Prueba | Veredicto |
|---|---|---|---|
| **Rendimiento Mínimo (Throughput)** | &ge; 20 TPS | **21.77 TPS (21.77 req/s)** | **✅ CUMPLE (Superado)** |
| **Tiempo Máximo de Respuesta** | &le; 1.50 s (1,500 ms) | **1.03 s (1,030 ms)** | **✅ CUMPLE (Bajo límite)** |
| **Percentil 95 (P95)** | &le; 1.50 s (1,500 ms) | **0.43 s (438 ms)** | **✅ CUMPLE (Holgado)** |
| **Tasa de Error Aceptable** | &lt; 3.00% | **0.00% (0 errores en 661 peticiones)** | **✅ CUMPLE (Cero fallos)** |
| **Integridad de Autenticación** | 100% tokens válidos | **661/661 tokens extraídos (100%)** | **✅ CUMPLE** |

- **Reportes Generados:** Dashboard interactivo HTML ([`reporte_ejecucion.html`](file:///D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_Performance/Ejercicio_1_Script_Carga/reports/reporte_ejecucion.html)), JSON y TXT.

---

### 4.2. Ejercicio 2: Análisis de Resultados de Carga (App Transaction Balance)
A partir del archivo `textSummary.txt` y del diagrama temporal de monitoreo proporcionados, se realizó una evaluación técnica profunda de la prueba de carga ejecutada con 140 Usuarios Virtuales constantes durante 65 minutos (276,650 transacciones).

**Hallazgos Críticos del Análisis de Rendimiento:**
1. **Cumplimiento Aparente vs. Degradación Oculta:**  
   El acumulado reporta 2.44% de fallos y 97.55% de checks exitosos. No obstante, el monitoreo temporal revela una **caída catastrófica de rendimiento entre las 01:51:00 y las 01:58:00 (7 minutos)**, donde las peticiones cayeron de 82 req/s a 10-15 req/s.
2. **Relación VUs vs Throughput (Ley de Rendimiento):**  
   Los 140 VUs se mantuvieron constantes (la línea verde fue plana). El tiempo máximo de respuesta alcanzó **29.93 segundos**. Por la relación $\text{Throughput} = \frac{\text{VUs}}{\text{Tiempo de Respuesta}}$, al elevarse la latencia a 30s cada hilo quedó bloqueado esperando, produciendo la caída matemática del throughput a $140 / 30\text{s} \approx 4.67\text{ req/s}$. La caída se debió a **saturación en el servidor, no a desconexión de clientes**.
3. **Concentración de 5,987 Errores HTTP 5xx en Stage 1:**  
   El **88.58% de todos los fallos del test** ocurrieron exclusivamente en Stage 1 durante esa ventana de 7 minutos, representando una **indisponibilidad localizada cercana al 80%**.
4. **Causa Raíz Identificada:**  
   - Agotamiento del pool de conexiones hacia la Base de Datos (HikariCP / Tomcat JDBC).
   - Bloqueos transaccionales (*row-level lock contention / deadlocks*) en tablas de saldos de cuenta.
   - Timeouts de 30 segundos en el API Gateway o Balanceador de Carga (*HTTP 504 Gateway Timeout*).
   - Reinicio forzado de contenedores por memoria (*Kubernetes OOMKilled*), explicando el rebote instantáneo a 82.6 req/s a las 02:00:00.
5. **Recomendaciones de Arquitectura:**  
   - Reducción de Connection Timeout a 3,000 ms (*Fail-Fast*).
   - Desvío de consultas de saldo hacia Réplicas de Lectura (*Read Replicas*).
   - Implementación de Circuit Breaker (Resilience4j) con umbral de 2 segundos.
   - Caché distribuida Redis con TTL de 15 a 30 segundos para balances frecuentes.

---

## 5. CONCLUSIONES GENERALES Y ESTADO DE ENTREGABLES

- **Solución Integral y Robusta:** Se cubrieron todas las expectativas y criterios técnicos exigidos por Banco Pichincha y TCS en E2E, APIs y Performance.
- **Trazabilidad y Versionamiento:** Todos los insumos, scripts, fuentes, reportes enriquecidos y documentos Word se encuentran consolidados y sincronizados en la rama principal (`main`) del repositorio GitHub:
  `https://github.com/ronaldNk1625/reto_tecnico_qa_tcs.git`

---
**Firma:**  
*Ronald Berrones — QA Automation & Performance Engineer*  
*TCS / Banco Pichincha — Noviembre 2026*
