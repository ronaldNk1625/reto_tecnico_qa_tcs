# 📝 Conclusiones y Hallazgos Técnicos - Automatización E2E Demoblaze

> **Evaluación Técnica QA Automation** | Banco Pichincha - TCS (Tata Consultancy Services)  
> **Candidato:** Ronald Berrones  
> **Framework:** Serenity BDD 4.1.20 + Cucumber 7 + Screenplay Pattern + Java 17  
> **Aplicación:** [Demoblaze Store](https://www.demoblaze.com/)

---

## 📌 1. Resumen Ejecutivo de la Prueba

| Métrica | Valor |
| :--- | :--- |
| **Total de Escenarios Ejecutados** | 4 escenarios (5 casos de prueba totales) |
| **Casos Exitosos (Passed)** | 5 (100%) |
| **Casos Fallidos (Failed)** | 0 (0%) |
| **Errores / Comprometidos** | 0 |
| **Tasa de Éxito** | **100%** |
| **Navegador** | Google Chrome 157.0 (Selenium 4 / ChromeOptions) |
| **Reportes Generados** | Serenity BDD HTML (con screenshots) + Cucumber HTML/JSON |

---

## 🔍 2. Hallazgos Observados Durante la Automatización

### 1. Comportamiento Asíncrono (SPA / AJAX)
La plataforma web de Demoblaze opera como una **Single Page Application** con Bootstrap y jQuery, apoyada en el backend REST `https://api.demoblaze.com/`. Cada acción de catálogo y carrito dispara peticiones asíncronas en segundo plano:
- Al agregar un producto, la solicitud viaja a `/addtocart`.
- Al abrir la página del carrito (`cart.html`), se hace una petición a `/viewcart` que puebla dinámicamente la tabla HTML con las filas de productos.

**Impacto en la prueba:** Una automatización basada en esperas estáticas (`Thread.sleep`) resultaría en pruebas lentas o frágiles (*flaky tests*).  
**Solución aplicada:** Se implementaron esperas explícitas fluidas a través de los métodos de Serenity `WaitUntil.the(element, isVisible()).forNoMoreThan(15).seconds()`, garantizando estabilidad e independencia de la latencia de red.

### 2. Alertas Nativas de JavaScript (`window.alert`)
A diferencia de los sitios web modernos que usan componentes modales HTML/CSS para notificaciones (tipo Toasts), Demoblaze emplea `alert("Product added")`:
- El diálogo nativo del navegador interrumpe el hilo del DOM. Cualquier intento de Selenium por hacer clic o interactuar con otro elemento mientras la alerta esté presente desencadena un error inmediato `org.openqa.selenium.UnhandledAlertException`.

**Solución aplicada:** Se construyó la interacción de Screenplay `AcceptAlert`, la cual:
1. Emplea `ExpectedConditions.alertIsPresent()` con timeout configurable.
2. Extrae el texto de la alerta para auditoría en el reporte de Serenity (`Serenity.recordReportData()`).
3. Ejecuta `alert.accept()` garantizando la liberación del contexto del navegador.

### 3. Renderizado y Transiciones de Modales (Bootstrap & SweetAlert)
- **Formulario de Compra:** Se ubica en un modal estándar de Bootstrap (`#orderModal`).
- **Confirmación de Compra:** Se despliega a través de la librería **SweetAlert** (`.sweet-alert`), la cual cuenta con animaciones de opacidad y escala (*fade-in / scale-in*).

**Solución aplicada:** Se mapearon los Targets con selectores precisos y se orquestaron las tareas de llenado de formulario y aserción con sincronización sobre los contenedores activos.

### 4. Observaciones Funcionales y de Seguridad en Demoblaze
- **Compra Anónima:** Se permite finalizar transacciones sin registro ni login de usuario.
- **Ausencia de Validación en Datos de Pago:** El formulario acepta números de tarjeta arbitrarios sin validación del algoritmo de Luhn, sin fecha de expiración verificable y sin código de verificación (CVV).
- **Consistencia en Totales:** Se observó que el cálculo del total en `#totalp` se realiza del lado del cliente sumando los precios de los productos renderizados.

---

## 🛠️ 3. Consideraciones Técnicas y Buenas Prácticas

1. **Patrón Screenplay:**
   - Desacoplamiento total entre las intenciones del usuario (Tasks), las consultas de estado (Questions) y la localización de elementos (User Interfaces).
   - Facilidad de mantenimiento: si un selector cambia en la web, solo se actualiza una línea en la clase UI correspondiente sin afectar las tareas ni los step definitions.

2. **Data-Driven Testing Multi-Fuente:**
   - **Gherkin Scenario Outline:** Permite a los analistas de negocio leer y proponer combinaciones en la tabla de `Ejemplos:`.
   - **JSON Reader:** Integración con `datos_compra.json` para estructuras de datos complejas o anidadas.
   - **CSV Reader:** Integración con `datos_compra.csv` para cargas masivas y matrices de prueba tabulares.

3. **Reportes y Living Documentation:**
   - **Serenity Living Documentation:** Genera un informe HTML interactivo en `target/site/serenity/index.html` con evidencia visual (capturas de pantalla) de cada paso.
   - **Cucumber Reports:** Genera reportes en formato estándar JSON y HTML en `target/cucumber-reports/` para integración en dashboards de calidad y pipelines CI/CD.

---

## 💡 4. Recomendaciones para el Proyecto

1. **Atributos de Automatización (`data-qa` / `data-testid`):**
   Recomendar a los equipos de desarrollo frontend incorporar atributos dedicados a pruebas, evitando depender de clases estéticas de Bootstrap que puedan cambiar durante rediseños.
2. **Integración Continua:**
   Configurar ejecución programada en herramientas de CI/CD (Jenkins, GitLab CI, GitHub Actions) ejecutando `mvn clean verify -Dheadless.mode=true`.
3. **Pruebas de Integración de API:**
   Complementar las pruebas de UI con pruebas de nivel de servicios (REST API) contra los endpoints `/signup`, `/login` y `/addtocart` para asegurar una pirámide de pruebas equilibrada.

