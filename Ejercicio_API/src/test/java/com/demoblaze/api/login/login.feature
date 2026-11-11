@Login @ApiDemoblaze
Feature: Pruebas automatizadas del servicio REST Login (/login) en Demoblaze
  Como usuario registrado de Demoblaze
  Quiero autenticarme a traves del servicio /login
  Para obtener el token de sesion o recibir los mensajes de error correspondientes

  Background:
    * def signupUrl = baseUrl + '/signup'
    * def loginUrl  = baseUrl + '/login'
    * def randomUserGen = generateRandomUser

  @LoginExitoso @Smoke
  Scenario: Caso 3: Usuario y password correcto en login - Generacion exitosa de Auth Token
    # 1. Crear previamente el usuario para garantizar su existencia en el sistema
    * def usuarioValido = randomUserGen('login_user')
    * def claveValida = 'ClaveCorrecta2026*'
    * def payloadRegistro = { username: '#(usuarioValido)', password: '#(claveValida)' }

    Given url signupUrl
    And header Content-Type = 'application/json'
    And header Accept = 'application/json'
    And request payloadRegistro
    When method post
    Then status 200
    # La API devuelve "" al registrar exitosamente (texto plano con posible whitespace)
    * def signupBody = response.trim()
    And match signupBody == '""'
    * karate.log('Usuario de prueba registrado previamente:', usuarioValido)

    # 2. Ejecutar login con credenciales correctas
    * def payloadLogin = { username: '#(usuarioValido)', password: '#(claveValida)' }
    * karate.log('--> ENTRADA ENVIADA AL SERVICIO /login:', payloadLogin)

    Given url loginUrl
    And header Content-Type = 'application/json'
    And header Accept = 'application/json'
    And request payloadLogin
    When method post
    Then status 200

    # 3. Capturar y auditar salida
    * karate.log('<-- SALIDA CAPTURADA DEL SERVICIO /login:', response)

    # Validacion: La API devuelve string con "Auth_token: <token>"
    And match response contains 'Auth_token:'
    * def authToken = response.replace('Auth_token: ', '').replace('"', '').trim()
    * karate.log('Token de autorizacion extraido con exito:', authToken)
    And match authToken != ''

  @LoginPasswordIncorrecto @Regresion
  Scenario: Caso 4A: Usuario existente y password incorrecto en login
    # 1. Registrar usuario previo con credenciales conocidas
    * def usuarioRegistrado = randomUserGen('user_wrong_pass')
    * def claveReal = 'ClaveValida999!'

    Given url signupUrl
    And header Content-Type = 'application/json'
    And header Accept = 'application/json'
    And request { username: '#(usuarioRegistrado)', password: '#(claveReal)' }
    When method post
    Then status 200
    * def signupBody2 = response.trim()
    And match signupBody2 == '""'

    # 2. Intentar login con password incorrecto
    * def payloadErroneo = { username: '#(usuarioRegistrado)', password: 'PasswordTotalmenteErroneo!' }
    * karate.log('--> ENTRADA CON PASSWORD INCORRECTO:', payloadErroneo)

    Given url loginUrl
    And header Content-Type = 'application/json'
    And header Accept = 'application/json'
    And request payloadErroneo
    When method post
    Then status 200

    # 3. Captura y validacion de salida de error
    * karate.log('<-- SALIDA CAPTURADA:', response)
    And match response == { errorMessage: 'Wrong password.' }
    And match response.errorMessage == 'Wrong password.'

  @LoginUsuarioInexistente @Regresion
  Scenario: Caso 4B: Usuario y password incorrecto en login - Usuario no existente
    * def payloadInexistente = { username: 'usuario_totalmente_inexistente_999999', password: 'CualquierPassword123!' }
    * karate.log('--> ENTRADA CON USUARIO INEXISTENTE:', payloadInexistente)

    Given url loginUrl
    And header Content-Type = 'application/json'
    And header Accept = 'application/json'
    And request payloadInexistente
    When method post
    Then status 200

    * karate.log('<-- SALIDA CAPTURADA:', response)
    And match response == { errorMessage: 'User does not exist.' }
    And match response.errorMessage == 'User does not exist.'

  @OutlineLogin @DataDrivenJson
  Scenario Outline: Validacion de credenciales incorrectas consumiendo archivo JSON (<id>)
    * def payloadJson = { username: '<username>', password: '<password>' }
    * karate.log('Ejecutando prueba Login JSON: <description>')

    Given url loginUrl
    And header Content-Type = 'application/json'
    And header Accept = 'application/json'
    And request payloadJson
    When method post
    Then status <expectedStatus>
    And match response.errorMessage == '<expectedMessage>'

    Examples:
      | read('classpath:data/login_cases.json') |

  @OutlineLogin @DataDrivenCsv
  Scenario Outline: Validacion de credenciales incorrectas consumiendo archivo CSV (<id>)
    * def payloadCsv = { username: '<username>', password: '<password>' }
    * karate.log('Ejecutando prueba Login CSV: <description>')

    Given url loginUrl
    And header Content-Type = 'application/json'
    And header Accept = 'application/json'
    And request payloadCsv
    When method post
    Then status <expectedStatus>
    And match response.errorMessage == '<expectedMessage>'

    Examples:
      | read('classpath:data/login_cases.csv') |
