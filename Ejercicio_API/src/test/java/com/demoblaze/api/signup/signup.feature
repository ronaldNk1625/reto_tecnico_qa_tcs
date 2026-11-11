@Signup @ApiDemoblaze
Feature: Pruebas automatizadas del servicio REST Signup (/signup) en Demoblaze
  Como sistema cliente de Demoblaze
  Quiero enviar peticiones POST al servicio de registro
  Para validar la creacion de nuevos usuarios y el control de duplicados

  Background:
    * def signupUrl = baseUrl + '/signup'
    * def randomUserGen = generateRandomUser

  @CrearNuevoUsuario @Smoke
  Scenario: Caso 1: Crear un nuevo usuario exitosamente en signup
    # Entradas dinamicas para garantizar unicidad en cada ejecucion
    * def nuevoUsuario = randomUserGen('signup_user')
    * def claveUsuario = defaultPassword
    * def payload = { username: '#(nuevoUsuario)', password: '#(claveUsuario)' }

    # Auditoria de entradas
    * karate.log('--> ENTRADA ENVIADA AL SERVICIO /signup:', payload)

    Given url signupUrl
    And header Content-Type = 'application/json'
    And header Accept = 'application/json'
    And request payload
    When method post
    Then status 200

    # Auditoria de salidas
    * karate.log('<-- SALIDA CAPTURADA DEL SERVICIO /signup:', response)

    # Validacion: La API de Demoblaze responde con string literal "" al registrar exitosamente
    # La respuesta llega como texto plano con posible whitespace; se normaliza antes de comparar
    * def bodyNormalizado = response.trim()
    And match bodyNormalizado == '""'

  @UsuarioExistente @Regresion
  Scenario: Caso 2: Intentar crear un usuario que ya existe en el sistema
    # 1. Registrar el usuario inicial con nombre unico
    * def usuarioExistente = randomUserGen('existing_user')
    * def payloadInicial = { username: '#(usuarioExistente)', password: '#(defaultPassword)' }

    Given url signupUrl
    And header Content-Type = 'application/json'
    And header Accept = 'application/json'
    And request payloadInicial
    When method post
    Then status 200
    * def bodyNorm1 = response.trim()
    And match bodyNorm1 == '""'
    * karate.log('Usuario inicial registrado exitosamente:', usuarioExistente)

    # 2. Intentar registrar el mismo usuario nuevamente (duplicado)
    * karate.log('--> ENTRADA DE REINTENTO (DUPLICADO):', payloadInicial)
    Given url signupUrl
    And header Content-Type = 'application/json'
    And header Accept = 'application/json'
    And request payloadInicial
    When method post
    Then status 200

    # Auditoria de salida capturada
    * karate.log('<-- SALIDA DE ERROR CAPTURADA:', response)

    # Validacion del mensaje de error retornado por la API
    And match response == { errorMessage: 'This user already exist.' }
    And match response.errorMessage == 'This user already exist.'

  @OutlineSignup @DataDrivenJson
  Scenario Outline: Intento de registro duplicado consumiendo datos externos desde archivo JSON (<id>)
    # Se genera un usuario unico y se registra por primera vez
    * def userTest = randomUserGen('json_user')
    * def primerRegistro = { username: '#(userTest)', password: '<password>' }

    * karate.log('Ejecutando caso Outline JSON: <description>')
    Given url signupUrl
    And header Content-Type = 'application/json'
    And header Accept = 'application/json'
    And request primerRegistro
    When method post
    Then status 200
    * def bodyNormJson1 = response.trim()
    And match bodyNormJson1 == '""'

    # Segundo intento con el mismo usuario genera error de duplicado
    * def intentoDuplicado = { username: '#(userTest)', password: '<password>' }
    Given url signupUrl
    And header Content-Type = 'application/json'
    And header Accept = 'application/json'
    And request intentoDuplicado
    When method post
    Then status <expectedStatus>
    And match response.errorMessage == '<expectedErrorMessage>'

    Examples:
      | read('classpath:data/signup_cases.json') |

  @OutlineSignup @DataDrivenCsv
  Scenario Outline: Intento de registro duplicado consumiendo datos externos desde archivo CSV (<id>)
    # Se genera un usuario unico y se registra por primera vez
    * def userCsvTest = randomUserGen('csv_user')
    * def primerRegistroCsv = { username: '#(userCsvTest)', password: '<password>' }

    * karate.log('Ejecutando caso Outline CSV: <description>')
    Given url signupUrl
    And header Content-Type = 'application/json'
    And header Accept = 'application/json'
    And request primerRegistroCsv
    When method post
    Then status 200
    * def bodyNormCsv1 = response.trim()
    And match bodyNormCsv1 == '""'

    # Segundo intento con el mismo usuario genera error de duplicado
    * def intentoDuplicadoCsv = { username: '#(userCsvTest)', password: '<password>' }
    Given url signupUrl
    And header Content-Type = 'application/json'
    And header Accept = 'application/json'
    And request intentoDuplicadoCsv
    When method post
    Then status <expectedStatus>
    And match response.errorMessage == '<expectedErrorMessage>'

    Examples:
      | read('classpath:data/signup_cases.csv') |
