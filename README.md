# 🚀 Prueba Técnica QA Automation - Banco Pichincha / TCS

Repositorio que contiene la solución completa de la prueba técnica práctica para el rol de **QA Automation Engineer** para **Banco Pichincha** a través de **TCS (Tata Consultancy Services)**.

---

## 📂 Estructura General del Repositorio

El examen práctico está compuesto por 2 ejercicios:

```text
reto_tecnico_qa_tcs/
│
├── Ejercicio_E2E/                  # Ejercicio 1: Automatización E2E en Demoblaze
│   ├── src/test/java/...           # Screenplay Pattern (Tasks, UI, Model, Questions, Steps)
│   ├── src/test/resources/...      # Features en Gherkin, serenity.conf y datos JSON/CSV
│   ├── pom.xml                     # Configuración de Maven y Serenity BDD 4.1.20
│   ├── readme.txt                  # Instrucciones paso a paso de ejecución (Requerido)
│   ├── README.md                   # Documentación detallada en Markdown con diagramas
│   ├── conclusiones.txt            # Hallazgos y conclusiones técnicas (Requerido)
│   └── conclusiones.md             # Informe técnico detallado
│
├── Ejercicio_API/                  # Ejercicio 2: Automatización de APIs (Siguiente fase)
│
├── .gitignore                      # Archivos y directorios excluidos de Git
└── README.md                       # Documentación general de la prueba técnica
```

---

## 📌 Ejercicio 1 - Automatización E2E (Demoblaze)

- **Sitio Bajo Prueba:** [Demoblaze Store](https://www.demoblaze.com/)
- **Framework Implementado:** **Serenity BDD 4.1.20 + Cucumber 7 + Screenplay Pattern + Java 17 + Maven**
- **Navegador Soportado:** Google Chrome (Headless y modo visual interactivo)
- **Estrategia de Datos:** Data-Driven Testing (Gherkin Scenario Outline, JSON y CSV)
- **Estado de Ejecución:** **100% Exitoso (5/5 tests passing)**
- **Reportes:** 
  - Serenity Living Documentation con capturas de pantalla automáticas (`target/site/serenity/index.html`).
  - Cucumber Reports HTML y JSON (`target/cucumber-reports/`).

👉 Consulte el directorio [`Ejercicio_E2E/`](Ejercicio_E2E/) para las instrucciones detalladas de instalación, ejecución y reportes.

---

## 👤 Información del Candidato

- **Nombre:** Ronald Berrones
- **Rol:** QA Automation Engineer
- **Fecha:** Noviembre 2026
