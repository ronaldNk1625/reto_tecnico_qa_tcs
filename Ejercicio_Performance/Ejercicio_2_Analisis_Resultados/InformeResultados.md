# INFORME DE ANÁLISIS DE RESULTADOS DE PRUEBAS DE CARGA

**Proyecto / Aplicación:** App Transaction Balance  
**Entidad / Cliente:** Banco Pichincha / TCS (Tata Consultancy Services)  
**Rol:** QA Automation & Performance Engineer  
**Fecha de Emisión:** Noviembre 2026  
**Documento:** InformeResultados.doc / InformeResultados.md  

---

## 1. RESUMEN EJECUTIVO

El presente informe detalla el análisis técnico y cuantitativo derivado de la prueba de carga ejecutada sobre el servicio **"App Transaction Balance"**, cuyo objetivo fue evaluar el comportamiento, estabilidad, tiempos de respuesta y tasa de fallos bajo una carga sostenida de **140 Usuarios Virtuales (VUs)** durante un periodo aproximado de **65 minutos**.

### Métricas Clave de la Ejecución

| Métrica | Valor Obtenido | Umbral de Referencia (SLA) | Evaluación |
|---|---|---|---|
| **Total de Transacciones (`http_reqs`)** | 276,650 peticiones | N/A | Alto volumen procesado |
| **Throughput Promedio** | 73.18 req/s | > 70 req/s | Aceptable a nivel global |
| **Tiempo Promedio de Respuesta (`avg`)** | 861.68 ms | < 1,000 ms | Dentro del rango |
| **Mediana de Respuesta (`med`)** | 613.42 ms | < 1,000 ms | Óptimo en régimen estable |
| **Percentil 90 (`p90`)** | 1.28 s (1,280 ms) | < 1,500 ms | Aceptable |
| **Percentil 95 (`p95`)** | **1.57 s (1,570 ms)** | < 1,500 ms | **⚠️ SUPERÓ EL SLA (Debe ser &le; 1.5s)** |
| **Tiempo Máximo de Respuesta (`max`)** | **29.93 s (29,930 ms)** | < 5.0 s | **🚨 CRÍTICO (Borde de timeout de 30s)** |
| **Tasa de Errores Global (`http_req_failed`)**| 2.44% (6,759 fallos) | < 3.00% | Cumple SLA globalmente (< 3%) |
| **Tasa de Éxito en Checks** | 97.55% (269,891 OK) | > 97.00% | Cumple en el acumulado |

### Diagnóstico Principal
Aunque las métricas consolidadas muestran un cumplimiento aparente de los SLAs generales (error global del 2.44% frente al 3% tolerado), **el análisis temporal y el monitoreo revelan una degradación crítica del servicio entre las 01:51:00 y las 01:58:00 (duración ~7 minutos)**, donde el rendimiento colapsó de ~80 req/s a menos de 15 req/s y se concentraron **5,987 errores 5xx** junto a tiempos de respuesta de hasta **29.93 segundos**.

---

## 2. ANÁLISIS DETALLADO DEL DIAGRAMA DE MONITOREO (VUs vs HTTP_REQS)

El gráfico de monitoreo temporal (01:35:00 a 02:40:00) registra la correlación entre la concurrencia de Usuarios Virtuales (línea verde) y las peticiones procesadas por segundo (línea azul).

```
VUs / Throughput
150 VUs | -----------------------[140 VUs constantes]-----------------------
        |   /\__/\/\            /\                               /\__/\/\
100 req |  /        \          /  \ (Recuperación)              /        \
 80 req | /          \________/    \___________________________/          \
        |             |      |
 20 req |             |CAÍDA | (01:51 a 01:58 -> 10-15 req/s)
  0 req |_ _ _ _ _ _ _|_ _ _ |_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
        01:35       01:51  01:58   02:02                      02:37    02:40
```

### Fases Observadas en el Comportamiento del Sistema

#### Fase 1: Régimen Estable Inicial (01:36:00 – 01:50:00)
- **Carga:** Rampa inicial rápida hasta alcanzar los **140 VUs**.
- **Comportamiento:** El throughput oscila de manera estable entre **75 y 90 req/s**.
- **Latencia:** Los tiempos de respuesta se mantienen alrededor de la mediana (613 ms), demostrando que la arquitectura soporta inicialmente los 140 usuarios sin saturación.

#### Fase 2: Incidente de Degradación y Colapso (01:51:00 – 01:58:00) ⚠️
- **Carga:** Los **140 VUs se mantienen invariables en la gráfica** (línea verde plana).
- **Anomalía:** A partir de las 01:51:00, las peticiones por segundo caen en picada desde ~82 req/s hasta situarse en un valle crítico de **10 a 15 req/s**, manteniéndose deprimido durante casi 8 minutos.
- **Explicación Matemática de la Relación VUs vs TPS:**
  La ley fundamental del rendimiento establece:
  $$\text{Throughput (TPS)} = \frac{\text{VUs}}{\text{Tiempo de Respuesta (Response Time)} + \text{Think Time}}$$
  Cuando el tiempo de respuesta del servidor se dispara de **600 ms** a **~29.93 segundos**, cada usuario virtual queda bloqueado esperando la respuesta HTTP antes de enviar la siguiente iteración. Con 140 usuarios bloqueados durante 30 segundos:
  $$\text{Throughput Mínimo Teórico} = \frac{140 \text{ VUs}}{30 \text{ s}} \approx 4.67 \text{ req/s}$$
  Esto explica por qué el throughput se desplomó drásticamente sin que disminuyera la cantidad de usuarios virtuales: **los VUs se encontraban en espera activa (bloqueo por latencia).**

#### Fase 3: Rebote y Recuperación Abrupta (01:59:00 – 02:02:00)
- En el minuto 01:59:00 el throughput muestra un primer pico de recuperación, y para las **02:00:00** regresa de golpe al nivel nominal de ~80 req/s.
- En el tooltip de monitoreo de las **02:02:00**, se valida:
  - `vus: 140`
  - `http_reqs: 82.6/s`
- Este tipo de recuperación instantánea en escalón es característica de un **reinicio de contenedor/pod (Kubernetes Pod Restart / OOMKilled)**, una purga del pool de conexiones o la liberación forzada de bloqueos en base de datos.

#### Fase 4: Régimen Post-Incidente (02:02:00 – 02:36:00)
- El sistema continúa operando a ~80 req/s hasta el inicio de la rampa de bajada (ramp-down) a las 02:37:00.

---

## 3. ANÁLISIS CUANTITATIVO DE ERRORES Y TIEMPOS (TEXTSUMMARY.TXT)

### 3.1. Distribución y Clasificación de Errores por Etapas

La métrica de errores desglosada por etapas en el archivo `textSummary.txt` revela con exactitud quirúrgica dónde se produjo la falla:

| Etapa de Prueba | Tipo de Error HTTP | Cantidad de Fallos | Tasa / Frecuencia | Impacto |
|---|---|---|---|---|
| **Stage 0 (Warm-up)** | HTTP 5xx | 1 fallo | 0.000265/s | Marginal |
| **Stage 1 (Carga Sostenida)** | **HTTP 4xx** | **769 fallos** | 0.203409/s | Errores de cliente / Throttling / 429 |
| **Stage 1 (Carga Sostenida)** | **HTTP 5xx** | **5,987 fallos** | **1.583625/s** | **🚨 88.58% de todos los fallos del test** |
| **Stage 2 (Ramp-down)** | HTTP 5xx | 2 fallos | 0.000529/s | Marginal |
| **TOTAL ERRORES** | **4xx + 5xx** | **6,759 fallos** | **2.44% del total** | **Concentrados en el incidente** |

#### Conclusiones del desglose de errores:
1. **Los 5,987 errores HTTP 5xx ocurrieron casi en su totalidad durante el colapso de las 01:51 a 01:58 en el Stage 1.**
2. Durante esos 7 minutos (~420 segundos), la tasa real de fallos en esa ventana no fue del 2.44%, sino de aproximadamente:
   $$\text{Tasa de Fallo en Ventana Crítica} = \frac{5,987 \text{ fallos}}{\approx 7,500 \text{ peticiones en ventana}} \approx 80\% \text{ de indisponibilidad}$$
3. Los **769 errores HTTP 4xx** corresponden muy probablemente a códigos **HTTP 429 (Too Many Requests)** generados por mecanismos de rate-limiting del API Gateway, o a **HTTP 400/409** por concurrencia no serializada en la actualización del saldo de transacciones.

### 3.2. Desglose de Componentes de Latencia de Red

| Componente | Tiempo Promedio | Mediana | Máximo | P95 | Diagnóstico |
|---|---|---|---|---|---|
| `http_req_blocked` | 10.97 µs | 0 s | 35.02 ms | 0 s | Excelente (sin encolamiento local) |
| `http_req_connecting` | 3.3 µs | 0 s | 11.82 ms | 0 s | Negociación TCP instantánea |
| `http_req_tls_handshaking` | 7.36 µs | 0 s | 27.02 ms | 0 s | Handshake SSL/TLS reutilizado |
| `http_req_sending` | 43.22 µs | 0 s | 31.25 ms | 517 µs | Envío de payload ultra-rápido |
| **`http_req_waiting` (TTFB)** | **861.21 ms** | **613.01 ms** | **29.93 s** | **1.57 s** | **🚨 Cuello de botella en procesamiento backend** |
| `http_req_receiving` | 424.03 µs | 320.7 µs | 39.58 ms | 1.05 ms | Descarga de respuesta normal |

**Deducción Técnica Indiscutible:**  
El tiempo total de respuesta (`http_req_duration avg = 861.68 ms, max = 29.93 s`) es idéntico al tiempo de espera en el servidor (`http_req_waiting avg = 861.21 ms, max = 29.93 s`).  
**La red, la conexión TCP y la capa de transporte funcionaron de forma impecable (< 1 ms); el retraso y los timeouts se originaron 100% en el servidor de aplicaciones y la base de datos.**

---

## 4. ANÁLISIS DE CAUSA RAÍZ (ROOT CAUSE ANALYSIS)

A partir de la correlación entre el tiempo máximo de 29.93 segundos, el desplome a 10 req/s, la concentración de errores 5xx en Stage 1 y la posterior recuperación en escalón, se identifican las siguientes causas raíz más probables:

1. **Agotamiento del Pool de Conexiones a Base de Datos (Connection Pool Starvation):**
   Al llegar a 140 usuarios concurrentes sobre una operación transaccional ("App Transaction Balance"), el pool de conexiones (ej. HikariCP / Tomcat JDBC) se agotó. Las peticiones entrantes quedaron en cola de espera hasta agotar el connection timeout configurado (típicamente 30 segundos).

2. **Bloqueos Transaccionales y Contención de Filas (Deadlocks / Row-Level Lock Contention):**
   Al tratarse de transacciones de balance financiero (`Transaction Balance`), si múltiples VUs intentan consultar o bloquear registros en tablas compartidas (cuentas, libros contables, saldos) con aislamiento `SERIALIZABLE` o `SELECT ... FOR UPDATE`, se generan cascadas de bloqueos (lock waits) que congelan los hilos ejecutores.

3. **Límite de Timeout en Balanceador de Carga / Reverse Proxy (HTTP 504 Gateway Timeout):**
   El valor máximo registrado de **29.93 segundos** es la firma característica de un timeout de proxy inverso (AWS ALB / Nginx / Traefik / Kong) configurado con `proxy_read_timeout 30s`. Cumplidos los 30 segundos sin respuesta del microservicio, el proxy corta la conexión y retorna un código `HTTP 504 Gateway Timeout` al cliente.

4. **Colapso de Memoria y Recolección de Basura Severa (JVM Full GC Pause / OOMKilled):**
   En arquitecturas Java/Spring Boot o Node.js, la acumulación masiva de peticiones no atendidas satura el Heap, provocando pausas de "Stop-the-World" de varios segundos o el reinicio forzado del pod por Kubernetes al superar el memory limit (`OOMKilled`), lo cual coincide con la recuperación abrupta observada a las 02:00:00.

---

## 5. CONCLUSIONES

1. **Cumplimiento Parcial Engañoso:**  
   Si bien la prueba arrojó un 97.55% de checks exitosos y una tasa de fallo global del 2.44% (menor al umbral del 3%), **la prueba NO es satisfactoria para un ambiente productivo bancario**, dado que el sistema experimentó una caída severa de casi 8 minutos con una tasa de indisponibilidad localizada cercana al 80%.

2. **Incumplimiento de SLA en Percentiles Altos:**  
   El Percentil 95 obtenido fue de **1.57 segundos**, superando el límite estándar bancario de 1.50 segundos. El tiempo máximo de **29.93 segundos** representa una experiencia inaceptable para los clientes de la aplicación móvil/web del Banco Pichincha.

3. **Falta de Resiliencia y Mecanismos de Falla Temprana (Fail-Fast):**  
   El sistema retuvo peticiones durante 30 segundos en lugar de aplicar políticas de Circuit Breaker (ej. Resilience4j / Envoy) que respondan inmediatamente con degradación controlada o mensajes de reintento.

---

## 6. RECOMENDACIONES TÉCNICAS Y DE ARQUITECTURA

Con el fin de certificar el servicio para su paso a producción, se recomienda ejecutar el siguiente plan de remediación:

### A. A Nivel de Base de Datos y Capa de Persistencia
1. **Dimensionamiento del Pool de Conexiones:**
   Ajustar el tamaño máximo del pool (ej. `maximumPoolSize: 50-70`) y reducir el `connectionTimeout` a un máximo de **3,000 ms** para fallar rápido en lugar de retener hilos 30 segundos.
2. **Optimización de Consultas e Índices en Balance:**
   Revisar los planes de ejecución (`EXPLAIN ANALYZE`) en las tablas de balance transaccional. Implementar índices compuestos en `(account_id, transaction_date)`.
3. **Nivel de Aislamiento y Réplicas de Lectura (Read Replicas):**
   Separar el tráfico: enviar consultas de saldo a réplicas de lectura de base de datos (`Read-Only Data Replicas`) y reservar la instancia primaria (`Writer`) exclusivamente para transferencias y débitos.

### B. A Nivel de Microservicios y Balanceo de Carga
4. **Implementación de Circuit Breaker:**
   Configurar Resilience4j / Spring Cloud CircuitBreaker para que, si el 20% de las peticiones exceden 2 segundos o fallan, el circuito se abra de inmediato retornando una respuesta alternativa o caché temporal en milisegundos.
5. **Ajuste de Timeouts:**
   Reducir el `read_timeout` entre el API Gateway y el microservicio a un máximo de **5 segundos**. Una petición financiera no debe quedar retenida 30 segundos en el gateway.
6. **Políticas de Auto-escalado Horizontal (HPA en Kubernetes):**
   Configurar HPA con base en métricas personalizadas (tasa de peticiones por segundo y latencia de respuesta), no solo CPU, para aprovisionar pods adicionales de forma preventiva antes de que la carga alcance los 140 VUs.

### C. A Nivel de Caché y Throttling
7. **Caché Distribuida con Redis:**
   Implementar una capa de almacenamiento en caché en memoria (Redis Cache) con TTL corto (ej. 10 a 30 segundos) para consultas frecuentes de saldo. Esto absorbería hasta el 70% de las peticiones de balance sin tocar la base de datos relacional.
8. **Plan de Retest:**
   Ejecutar una prueba de re-certificación idéntica (140 VUs constantes durante 60 minutos) tras aplicar las optimizaciones, fijando como criterio de éxito:
   - `http_req_failed < 0.5%`
   - `p(95) < 1,000 ms`
   - `max < 3,000 ms`
   - Ausencia absoluta de caídas en la gráfica de Throughput.

---
**Firma:**  
*Ronald Berrones — QA Automation & Performance Engineer*  
*TCS / Banco Pichincha*

