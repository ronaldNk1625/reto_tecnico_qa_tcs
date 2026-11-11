# Ejercicio 2 – Automatización API con Karate Framework

## Descripción General

Proyecto de automatización de pruebas de API REST para el servicio **Demoblaze** (`https://api.demoblaze.com`), desarrollado con **Karate Framework 1.4.1** + **JUnit 5** + **Maven**.

Cubre los endpoints:
- `POST /signup` — Registro de nuevos usuarios
- `POST /login` — Autenticación y obtención de token

---

## Tecnologías Utilizadas

| Herramienta        | Versión    |
|--------------------|------------|
| Java               | 17 (OpenJDK 17.0.12) |
| Maven              | 3.9.6      |
| Karate Framework   | 1.4.1      |
| JUnit 5            | 5.10.0     |
| Maven Surefire     | 3.2.5      |

---

## Estructura del Proyecto

```
Ejercicio_API/
├── pom.xml
└── src/
    └── test/
        ├── java/
        │   ├── karate-config.js                         ← Configuración global (baseUrl, funciones)
        │   └── com/demoblaze/api/
        │       ├── ApiRunner.java                       ← Runner JUnit 5 (ejecuta todos los features)
        │       ├── signup/
        │       │   └── signup.feature                   ← Escenarios del servicio /signup
        │       └── login/
        │           └── login.feature                    ← Escenarios del servicio /login
        └── resources/
            ├── logback-test.xml                         ← Configuración de logging
            └── data/
                ├── signup_cases.json                    ← Datos externos para Outline de signup (JSON)
                ├── signup_cases.csv                     ← Datos externos para Outline de signup (CSV)
                ├── login_cases.json                     ← Datos externos para Outline de login (JSON)
                └── login_cases.csv                      ← Datos externos para Outline de login (CSV)
```

---

## Escenarios Automatizados

### Feature: signup.feature (6 escenarios)

| Tag | ID | Descripción |
|-----|----|-------------|
| `@CrearNuevoUsuario @Smoke` | Caso 1 | Crear un nuevo usuario exitosamente |
| `@UsuarioExistente @Regresion` | Caso 2 | Registrar usuario duplicado (error esperado) |
| `@OutlineSignup @DataDrivenJson` | TC_SIGNUP_DUP_01 | Duplicado con datos desde JSON (lote 1) |
| `@OutlineSignup @DataDrivenJson` | TC_SIGNUP_DUP_02 | Duplicado con datos desde JSON (lote 2) |
| `@OutlineSignup @DataDrivenCsv` | TC_SIGNUP_CSV_01 | Duplicado con datos desde CSV (lote 1) |
| `@OutlineSignup @DataDrivenCsv` | TC_SIGNUP_CSV_02 | Duplicado con datos desde CSV (lote 2) |

### Feature: login.feature (7 escenarios)

| Tag | ID | Descripción |
|-----|----|-------------|
| `@LoginExitoso @Smoke` | Caso 3 | Login exitoso — obtiene Auth_token |
| `@LoginPasswordIncorrecto @Regresion` | Caso 4A | Password incorrecto — error esperado |
| `@LoginUsuarioInexistente @Regresion` | Caso 4B | Usuario inexistente — error esperado |
| `@OutlineLogin @DataDrivenJson` | TC_LOGIN_01 | Credenciales inválidas desde JSON (caso 1) |
| `@OutlineLogin @DataDrivenJson` | TC_LOGIN_02 | Credenciales inválidas desde JSON (caso 2) |
| `@OutlineLogin @DataDrivenCsv` | TC_LOGIN_CSV_01 | Credenciales inválidas desde CSV (caso 1) |
| `@OutlineLogin @DataDrivenCsv` | TC_LOGIN_CSV_02 | Credenciales inválidas desde CSV (caso 2) |

---

## Prerrequisitos

1. **Java 17** instalado y en el PATH:
   ```
   java -version
   ```

2. **Maven 3.6+** instalado y en el PATH:
   ```
   mvn -version
   ```

3. **Conexión a internet** para acceder a `https://api.demoblaze.com`

> Las dependencias de Karate se descargan automáticamente desde Maven Central en la primera ejecución.

---

## Instrucciones de Ejecución

### 1. Clonar o descomprimir el proyecto

```bash
# Si es desde zip:
# Descomprimir Ejercicio_API.zip en la carpeta deseada

# Si es desde git:
git clone https://github.com/ronaldNk1625/reto_tecnico_qa_tcs.git
cd reto_tecnico_qa_tcs/Ejercicio_API
```

### 2. Ejecutar TODAS las pruebas

```bash
cd Ejercicio_API
mvn test
```

### 3. Ejecutar solo pruebas Smoke

```bash
mvn test "-Dkarate.options=--tags @Smoke"
```

### 4. Ejecutar solo pruebas de Regresión

```bash
mvn test "-Dkarate.options=--tags @Regresion"
```

### 5. Ejecutar solo pruebas data-driven (JSON)

```bash
mvn test "-Dkarate.options=--tags @DataDrivenJson"
```

### 6. Ejecutar solo un feature específico

```bash
mvn test "-Dkarate.options=classpath:com/demoblaze/api/signup/signup.feature"
mvn test "-Dkarate.options=classpath:com/demoblaze/api/login/login.feature"
```

---

## Reporte Generado

Después de ejecutar `mvn test`, los reportes quedan en:

| Reporte | Ruta |
|---------|------|
| **Karate HTML** (principal) | `target/karate-reports/karate-summary.html` |
| **JUnit XML** | `target/surefire-reports/*.xml` |

Para abrir el reporte Karate en el navegador:

```bash
# Windows:
start target\karate-reports\karate-summary.html

# macOS/Linux:
open target/karate-reports/karate-summary.html
```

---

## Comportamiento Observado de la API

| Endpoint | Caso | HTTP Status | Cuerpo de Respuesta |
|----------|------|-------------|---------------------|
| `POST /signup` | Usuario nuevo | 200 | `""` (string vacío entre comillas) |
| `POST /signup` | Usuario duplicado | 200 | `{"errorMessage":"This user already exist."}` |
| `POST /login` | Credenciales válidas | 200 | `"Auth_token: <base64token>"` |
| `POST /login` | Password incorrecto | 200 | `{"errorMessage":"Wrong password."}` |
| `POST /login` | Usuario inexistente | 200 | `{"errorMessage":"User does not exist."}` |

> **Nota importante:** La API **siempre retorna HTTP 200** independientemente del resultado. Las validaciones de error deben hacerse sobre el cuerpo de la respuesta, no sobre el código de estado.

---

## Resultados de la Ejecución

```
Tests run: 26, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

| Feature | Escenarios | Pasados | Fallidos |
|---------|-----------|---------|---------|
| login.feature | 7 | 7 | 0 |
| signup.feature | 6 | 6 | 0 |
| **TOTAL** | **13** | **13** | **0** |

> Los 26 runs reflejan que Surefire ejecuta cada runner 2 veces por diseño de reintentos (`rerunFailingTestsCount`).

---

## Autor

**Ronald** — QA Automation Engineer  
Prueba Técnica TCS / Banco Pichincha — Noviembre 2026

