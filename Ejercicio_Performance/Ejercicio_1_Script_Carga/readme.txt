================================================================================
EJERCICIO 1 - SCRIPT DE PRUEBAS DE CARGA: SERVICIO LOGIN
BANCO PICHINCHA / TCS (TATA CONSULTANCY SERVICES)
================================================================================

1. DESCRIPCIÓN DEL EJERCICIO
--------------------------------------------------------------------------------
Automatización y ejecución de pruebas de carga para el endpoint de autenticación:
POST https://fakestoreapi.com/auth/login

El servicio recibe en formato JSON:
{
  "username": "user",
  "password": "passwd"
}

Criterios y SLAs exigidos:
- Alcanzar al menos 20 TPS (Transactions Per Second / RPS).
- Tiempo de respuesta permitido: máximo 1.5 segundos.
- Tasa de error aceptable: menor al 3% del total de peticiones.
- Parametrización desde archivo CSV con 5 juegos de credenciales.


2. TECNOLOGÍAS Y VERSIONES UTILIZADAS
--------------------------------------------------------------------------------
- Grafana K6: v2.4.0 (Windows/amd64)
- Apache JMeter: v5.6.3 (script .jmx interoperable)
- Python: 3.13.15 (generación de dashboard HTML de reportes)
- Sistema Operativo: Windows 11 / Windows Server


3. ESTRUCTURA DE ARCHIVOS DEL EJERCICIO 1
--------------------------------------------------------------------------------
Ejercicio_1_Script_Carga/
  ├── data/
  │   └── users.csv                   <- Archivo CSV con los 5 usuarios parametrizados
  ├── scripts/
  │   ├── k6_login_load_test.js       <- Script de carga K6 (SharedArray + Thresholds)
  │   └── jmeter_login_load_test.jmx  <- Script de carga JMeter (CSV Data Set + Assertions)
  ├── reports/
  │   ├── reporte_ejecucion.html      <- Dashboard HTML interactivo de resultados
  │   ├── summary.txt                 <- Resumen en texto plano generado por K6
  │   ├── summary.json                <- Datos crudos en JSON con todas las métricas
  │   └── build_html_report.py        <- Generador automatizado del reporte HTML
  ├── readme.txt                      <- Este archivo con instrucciones paso a paso
  └── conclusiones.txt                <- Hallazgos y conclusiones de la prueba de carga


4. INSTRUCCIONES PASO A PASO DE EJECUCIÓN (K6)
--------------------------------------------------------------------------------

Paso 1: Verificar la instalación de K6
  Abra una terminal (PowerShell o CMD) y ejecute:
  k6 version

  Si no lo tiene en el PATH pero descargó el binario portátil:
  & "C:\Users\ronal\tools\k6\k6-v2.4.0-windows-amd64\k6.exe" version

Paso 2: Navegar a la carpeta de scripts
  cd D:\Prueba_tecnica_tata\reto_tecnico_qa_tcs\Ejercicio_Performance\Ejercicio_1_Script_Carga\scripts

Paso 3: Ejecutar la prueba de carga
  k6 run k6_login_load_test.js

  (o indicando la ruta del ejecutable si no está en PATH):
  & "C:\Users\ronal\tools\k6\k6-v2.4.0-windows-amd64\k6.exe" run k6_login_load_test.js

Paso 4: Visualizar los reportes generados
  Los reportes se actualizarán automáticamente en la carpeta ../reports:
  - Resumen en consola: Visualizado al finalizar la ejecución.
  - Resumen texto: ../reports/summary.txt
  - Reporte JSON: ../reports/summary.json
  - Dashboard HTML: ../reports/reporte_ejecucion.html

  Para abrir el reporte HTML en su navegador:
  start ../reports/reporte_ejecucion.html


5. INSTRUCCIONES DE EJECUCIÓN ALTERNATIVA CON JMETER
--------------------------------------------------------------------------------
Si prefiere utilizar Apache JMeter:

1. Ejecución en modo GUI (Interactiva):
   jmeter -t scripts/jmeter_login_load_test.jmx

2. Ejecución en modo Non-GUI (Línea de Comandos / CI/CD):
   jmeter -n -t scripts/jmeter_login_load_test.jmx -l reports/jmeter_results.jtl -e -o reports/jmeter_dashboard/


6. RESULTADOS OBTENIDOS EN LA PRUEBA REAL
--------------------------------------------------------------------------------
Métrica                       Exigido por Examen     Obtenido Real         Estado
--------------------------------------------------------------------------------
Throughput mínimo (TPS)       >= 20 TPS              21.77 TPS             ✓ CUMPLE
Tiempo máximo de respuesta    <= 1.50 s (1500 ms)    1.03 s (1030 ms)      ✓ CUMPLE
Percentil 95 (P95)            <= 1.50 s (1500 ms)    0.43 s (438 ms)       ✓ CUMPLE
Tasa de error                 < 3.00%                0.00% (0 errores)     ✓ CUMPLE
Total de peticiones           N/A                    661 peticiones        ✓ EXITOSO
Checks de validación          N/A                    1,983 checks (100%)   ✓ EXITOSO
--------------------------------------------------------------------------------
CONCLUSIÓN: Todos los criterios de aceptación y SLAs fueron ampliamente superados.
