# Conclusiones — Ejercicio 2: Automatización de APIs con Karate Framework

## Opiniones Generales

Karate Framework resultó ser una elección excelente para la automatización de APIs REST. A diferencia de otras herramientas como RestAssured (que requiere código Java extenso) o Postman/Newman, Karate permite escribir pruebas completamente en lenguaje Gherkin con sintaxis propia muy expresiva, lo que facilita la lectura y mantenimiento por parte de cualquier miembro del equipo QA.

---

## Hallazgos Técnicos Durante la Prueba

### 1. Comportamiento no convencional de la API (HTTP 200 para todo)

La API de Demoblaze retorna **HTTP 200 en todos los casos**, incluyendo errores. Esto va en contra de las buenas prácticas de diseño REST, donde se esperaría:
- `201 Created` para registro exitoso
- `409 Conflict` para usuario duplicado
- `401 Unauthorized` para credenciales inválidas

**Impacto en las pruebas:** No es posible validar el resultado únicamente por el código de estado; fue necesario examinar el cuerpo de la respuesta en cada caso, lo que añade complejidad a las aserciones.

### 2. Respuesta de registro exitoso: `""` (string literal entre comillas)

Al registrar un usuario exitosamente, la API retorna el cuerpo `""` — es decir, dos comillas dobles como texto plano, **no** un JSON vacío. Karate no parsea este valor como JSON (porque el `Content-Type` de la respuesta es `text/html; charset=utf-8`), por lo que la comparación debía hacerse sobre el string crudo.

Adicionalmente, la respuesta incluye un salto de línea al final (`""\n`), lo que hizo fallar comparaciones directas. La solución fue aplicar `.trim()` antes de comparar:
```gherkin
* def bodyNormalizado = response.trim()
And match bodyNormalizado == '""'
```

### 3. Acumulación de `path` en Karate entre requests del mismo escenario

Cuando un escenario realiza dos llamadas HTTP consecutivas (ej: primero a `/signup` y luego a `/login`), Karate **acumula** los segmentos de path si se usa `Given path 'signup'` seguido de `Given path 'login'`. Esto resulta en una URL inválida como `https://api.demoblaze.com/signup/login` → error 404.

**Solución adoptada:** Declarar las URLs completas en el `Background` de cada feature:
```gherkin
* def signupUrl = baseUrl + '/signup'
* def loginUrl  = baseUrl + '/login'
```
Y usar `Given url signupUrl` / `Given url loginUrl` en cada step, en lugar de `Given path`.

### 4. Generación dinámica de usuarios para garantizar unicidad

La API no permite registrar el mismo usuario dos veces. Para garantizar la **independencia de los escenarios** y que cada test sea repetible, se implementó una función JavaScript en `karate-config.js` que genera nombres únicos con timestamp y número aleatorio:
```javascript
generateRandomUser: function(prefix) {
  var timestamp = new Date().getTime();
  var randomInt = Math.floor(Math.random() * 90000) + 10000;
  return prefix + '_' + timestamp + '_' + randomInt;
}
```
Este enfoque garantiza que cada ejecución de tests no dependa del estado previo de la base de datos.

### 5. Data Driven Testing con JSON y CSV

El consumo de datos externos mediante `Scenario Outline` + `Examples: | read('classpath:...') |` funcionó perfectamente tanto para JSON como para CSV. Las columnas del CSV deben coincidir exactamente con los nombres de las columnas en la tabla `Examples`. El formato CSV fue el más frágil (sensible a espacios y codificación), mientras que JSON fue más robusto y expresivo.

---

## Consideraciones Adicionales

### Cobertura de Pruebas
Los escenarios implementados cubren los caminos más importantes:
- ✅ Flujo exitoso de registro (happy path)
- ✅ Manejo de duplicados en registro
- ✅ Flujo exitoso de login con validación de token
- ✅ Manejo de credenciales incorrectas
- ✅ Manejo de usuario inexistente
- ✅ Data-driven con JSON y CSV para escenarios negativos

### Lo que podría mejorarse en la API evaluada
1. **Códigos de estado HTTP adecuados** (`201`, `409`, `401`) en lugar de siempre `200`
2. **Respuesta de registro exitoso más informativa**, ej: `{"message":"User created successfully", "username":"..."}`
3. **Validación de formato de entrada** (longitud mínima de password, caracteres permitidos en username)
4. **Rate limiting / captcha** para prevenir registro masivo automatizado
5. **Endpoint de logout** y **renovación de token**

### Fortalezas de Karate Framework detectadas
- Sintaxis Gherkin nativa sin necesidad de step definitions Java
- Funciones JavaScript inline en los features
- `karate-config.js` como punto central de configuración por ambiente
- Reporte HTML integrado sin plugins adicionales
- Soporte nativo de JSON, XML, GraphQL en un mismo framework

### Dificultades encontradas
- La sandbox de ejecución del agente no tiene acceso a las herramientas del PATH del usuario (`java`, `mvn`), lo que requirió ejecutar con `BypassSandbox`
- La API retorna `text/html` como Content-Type en lugar de `application/json`, dificultando la comparación directa de respuestas
- El comportamiento del reintento automático de Surefire (`rerunFailingTestsCount=1`) duplica el número de runs reportados (26 runs para 13 escenarios)

---

## Resultado Final

```
Tests run: 26, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS — Total time: ~30 s
```

| Feature | Escenarios | Estado |
|---------|-----------|--------|
| signup.feature | 6 | ✅ Todos pasaron |
| login.feature | 7 | ✅ Todos pasaron |

---

**Autor:** Ronald — QA Automation Engineer  
**Fecha:** Noviembre 2026  
**Prueba Técnica:** TCS / Banco Pichincha

