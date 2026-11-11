EJERCICIO 2 - API AUTOMATION CON KARATE FRAMEWORK
==================================================
Prueba Tecnica QA Automatizador - TCS / Banco Pichincha

TECNOLOGIAS
-----------
- Java 17
- Karate Framework 1.4.1
- JUnit 5
- Maven 3.9.6

PRERREQUISITOS
--------------
1. Java 17 instalado (java -version)
2. Maven 3.6+ instalado (mvn -version)
3. Conexion a internet (accede a https://api.demoblaze.com)

ESTRUCTURA DEL PROYECTO
-----------------------
Ejercicio_API/
  pom.xml
  src/test/java/
    karate-config.js                   <- configuracion global
    com/demoblaze/api/
      ApiRunner.java                   <- runner JUnit 5
      signup/signup.feature            <- tests del endpoint /signup
      login/login.feature              <- tests del endpoint /login
  src/test/resources/
    logback-test.xml
    data/
      signup_cases.json  signup_cases.csv
      login_cases.json   login_cases.csv

INSTRUCCIONES DE EJECUCION
--------------------------

1. Situarse en la carpeta del proyecto:
   cd Ejercicio_API

2. Ejecutar TODOS los tests:
   mvn test

3. Ejecutar solo Smoke:
   mvn test "-Dkarate.options=--tags @Smoke"

4. Ejecutar solo Regresion:
   mvn test "-Dkarate.options=--tags @Regresion"

5. Ejecutar solo data-driven JSON:
   mvn test "-Dkarate.options=--tags @DataDrivenJson"

6. Ejecutar solo data-driven CSV:
   mvn test "-Dkarate.options=--tags @DataDrivenCsv"

REPORTES GENERADOS
------------------
Luego de ejecutar mvn test:

  Karate HTML:  target/karate-reports/karate-summary.html
  JUnit XML:    target/surefire-reports/

Abrir reporte en Windows:
  start target\karate-reports\karate-summary.html

RESULTADO ESPERADO
------------------
Tests run: 26, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS

ESCENARIOS CUBIERTOS
--------------------
signup.feature (6 escenarios):
  - Caso 1: Crear nuevo usuario exitosamente
  - Caso 2: Usuario duplicado (error esperado)
  - Outline JSON: 2 casos de duplicado con datos desde JSON
  - Outline CSV:  2 casos de duplicado con datos desde CSV

login.feature (7 escenarios):
  - Caso 3: Login exitoso (obtiene Auth_token)
  - Caso 4A: Password incorrecto (error esperado)
  - Caso 4B: Usuario inexistente (error esperado)
  - Outline JSON: 2 casos de credenciales invalidas desde JSON
  - Outline CSV:  2 casos de credenciales invalidas desde CSV

NOTA SOBRE LA API
-----------------
La API demoblaze SIEMPRE retorna HTTP 200, incluso en errores.
Las validaciones de error se hacen sobre el cuerpo de la respuesta.

Autor: Ronald - QA Automation Engineer
Fecha: Noviembre 2026

