================================================================================
MODULO DE PERFORMANCE TESTING - BANCO PICHINCHA / TCS
================================================================================

Este directorio contiene la solución completa de los dos ejercicios de la prueba 
técnica de rendimiento:

EJERCICIOS INCLUIDOS:
--------------------------------------------------------------------------------
1. Ejercicio 1: Script de Pruebas de Carga en Servicio de Login
   - Ubicación: Ejercicio_1_Script_Carga/
   - Endpoint: POST https://fakestoreapi.com/auth/login
   - Herramientas: Grafana K6 v2.4.0 y Apache JMeter v5.6.3
   - Datos: Parametrización desde archivo CSV con 5 credenciales
   - SLAs: Rendimiento >= 20 TPS, Tiempo máximo < 1.5s, Error < 3%
   - Entregables: Scripts (.js y .jmx), users.csv, reportes HTML/JSON/TXT,
     readme.txt y conclusiones.txt

2. Ejercicio 2: Análisis de Resultados de Prueba de Carga
   - Ubicación: Ejercicio_2_Analisis_Resultados/
   - Servicio Evaluado: App Transaction Balance
   - Entregable Oficial: InformeResultados.doc (y versiones .docx y .md)
   - Contenido: Hallazgos, conclusiones, recomendaciones de arquitectura,
     análisis cuantitativo de textSummary.txt y análisis temporal del diagrama
     de relación VUs vs Throughput (TPS).

INSTRUCCIONES DE EJECUCIÓN:
--------------------------------------------------------------------------------
Para reproducir la prueba de carga del Ejercicio 1 con K6:
1. Navegue a: Ejercicio_1_Script_Carga/scripts/
2. Ejecute: k6 run k6_login_load_test.js
3. Visualice el reporte en: Ejercicio_1_Script_Carga/reports/reporte_ejecucion.html

Para revisar el análisis del Ejercicio 2:
Abra el archivo: Ejercicio_2_Analisis_Resultados/InformeResultados.doc

Candidato: Ronald Berrones - QA Automation & Performance Engineer
Fecha: Noviembre 2026 - TCS / Banco Pichincha

