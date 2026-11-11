@Login @ApiDemoblaze
Feature: Pruebas automatizadas del servicio REST Login (/login) en Demoblaze
  Como usuario registrado de Demoblaze
  Quiero autenticarme a traves del servicio /login
  Para obtener el token de sesion o recibir los mensajes de error correspondientes

  Background:
    * url baseUrl
    * header Content-Type = 'application/json'
    * header Accept = 'application/json'
    * def randomUserGen = generateRandomUser

  @LoginExitoso @Smoke
  Scenario: Caso 3: Usuario y password correcto en login - Generacion exitosa de Auth Token
    # 1. Crear previamente el usuario para garantizar su existencia
    * def usuarioValido = randomUserGen('login_user')
    * def claveValida = 'ClaveCorrecta2026*'
    * def payloadRegistro = { username: usuarioValido, password: claveValida }

    Given path 'signup'
    And request payloadRegistro
    When method post
    Then status 200
    And match response == '""'
    * karate.log('Usuario de prueba registrado previamente:', usuarioValido)

    # 2. Ejecutar login con credenciales correctas
    * def payloadLogin = { username: usuarioValido, password: claveValida }
    * karate.log('--> ENTRADA ENVIADA AL SERVICIO /login:', payloadLogin)

    Given path 'login'
    And request payloadLogin
    When method post
    Then status 200

    # 3. Capturar y auditar salida
    * karate.log('<-- SALIDA CAPTURADA DEL SERVICIO /login:', response)

    # Validacion: La API devuelve "Auth_token: <token>"
    And match response contains 'Auth_token:'
    * def authToken = response.replace('Auth_token: ', '').replace('"', '')
    * karate.log('Token de autorizacion extraido con exito:', authToken)
    And match authToken != ''

  @LoginPasswordIncorrecto @Regresion
  Scenario: Caso 4A: Usuario existente y password incorrecto en login
    # 1. Registrar usuario previo
    * def usuarioRegistrado = randomUserGen('user_wrong_pass')
    * def claveReal = 'ClaveValida999!'
    
    Given path 'signup'
    And request { username: usuarioRegistrado, password: claveReal }
    When method post
    Then status 200

    # 2. Intentar login con password incorrecto
    * def payloadErroneo = { username: usuarioRegistrado, password: 'PasswordTotalmenteErroneo!' }
    * karate.log('--> ENTRADA CON PASSWORD INCORRECTO:', payloadErroneo)

    Given path 'login'
    And request payloadErroneo
    When method post
    Then status 200

    # 3. Captura y validacion de salida
    * karate.log('<-- SALIDA CAPTURADA:', response)
    And match response == { errorMessage: 'Wrong password.' }
    And match response.errorMessage == 'Wrong password.'

  @LoginUsuarioInexistente @Regresion
  Scenario: Caso 4B: Usuario y password incorrecto en login - Usuario no existente
    * def payloadInexistente = { username: 'usuario_totalmente_inexistente_999999', password: 'CualquierPassword123!' }
    * karate.log('--> ENTRADA CON USUARIO INEXISTENTE:', payloadInexistente)

    Given path 'login'
    And request payloadInexistente
    When method post
    Then status 200

    * karate.log('<-- SALIDA CAPTURADA:', response)
    And match response == { errorMessage: 'User does not exist.' }
    And match response.errorMessage == 'User does not exist.'

  @OutlineLogin @DataDrivenJson
  Scenario Outline: Validacion de credenciales incorrectas consumiendo archivo JSON (<id>)
    * path 'login'
    * def payloadJson = { username: '<username>', password: '<password>' }
    * karate.log('Ejecutando prueba Login JSON: <description>')

    Given request payloadJson
    When method post
    Then status <expectedStatus>
    And match response.errorMessage == '<expectedMessage>'

    Examples:
      | read('classpath:data/login_cases.json') |

  @OutlineLogin @DataDrivenCsv
  Scenario Outline: Validacion de credenciales incorrectas consumiendo archivo CSV (<id>)
    * path 'login'
    * def payloadCsv = { username: '<username>', password: '<password>' }
    * karate.log('Ejecutando prueba Login CSV: <description>')

    Given request payloadCsv
    When method post
    Then status <expectedStatus>
    And match response.errorMessage == '<expectedMessage>'

    Examples:
      | read('classpath:data/login_cases.csv') |

