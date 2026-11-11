@Signup @ApiDemoblaze
Feature: Pruebas automatizadas del servicio REST Signup (/signup) en Demoblaze
  Como sistema cliente de Demoblaze
  Quiero enviar peticiones POST al servicio de registro
  Para validar la creacion de nuevos usuarios y el control de duplicados

  Background:
    * url baseUrl
    * path 'signup'
    * header Content-Type = 'application/json'
    * header Accept = 'application/json'
    * def randomUserGen = generateRandomUser

  @CrearNuevoUsuario @Smoke
  Scenario: Caso 1: Crear un nuevo usuario exitosamente en signup
    # Entradas dinamicas para garantizar unicidad
    * def nuevoUsuario = randomUserGen('signup_user')
    * def claveUsuario = defaultPassword
    * def payload = { username: nuevoUsuario, password: claveUsuario }

    # Auditoria de entradas
    * karate.log('--> ENTRADA ENVIADA AL SERVICIO /signup:', payload)

    Given request payload
    When method post
    Then status 200

    # Auditoria de salidas
    * karate.log('<-- SALIDA CAPTURADA DEL SERVICIO /signup:', response)

    # Validacion: La API de Demoblaze responde con un string vacio "" al registrar exitosamente
    And match response == '""'

  @UsuarioExistente @Regresion
  Scenario: Caso 2: Intentar crear un usuario que ya existe en el sistema
    # 1. Registrar el usuario inicial
    * def usuarioExistente = randomUserGen('existing_user')
    * def payloadInicial = { username: usuarioExistente, password: defaultPassword }
    
    Given request payloadInicial
    When method post
    Then status 200
    And match response == '""'
    * karate.log('Usuario inicial registrado exitosamente:', usuarioExistente)

    # 2. Intentar registrar el mismo usuario nuevamente
    * karate.log('--> ENTRADA DE REINTENTO (DUPLICADO):', payloadInicial)
    Given request payloadInicial
    When method post
    Then status 200

    # Auditoria de salida capturada
    * karate.log('<-- SALIDA DE ERROR CAPTURADA:', response)

    # Validacion del mensaje de error retornado por la API
    And match response == { errorMessage: 'This user already exist.' }
    And match response.errorMessage == 'This user already exist.'

  @OutlineSignup @DataDrivenJson
  Scenario Outline: Intento de registro duplicado consumiendo datos externos desde archivo JSON (<id>)
    # Se genera y registra un usuario previo
    * def userTest = randomUserGen('json_user')
    * def primerRegistro = { username: userTest, password: '<password>' }
    
    Given request primerRegistro
    When method post
    Then status 200

    # Segundo intento con el mismo usuario
    * karate.log('Ejecutando caso Outline JSON: <description>')
    * def intentoDuplicado = { username: userTest, password: '<password>' }
    Given request intentoDuplicado
    When method post
    Then status <expectedStatus>
    And match response.errorMessage == '<expectedErrorMessage>'

    Examples:
      | read('classpath:data/signup_cases.json') |

  @OutlineSignup @DataDrivenCsv
  Scenario Outline: Intento de registro duplicado consumiendo datos externos desde archivo CSV (<id>)
    * def userCsvTest = randomUserGen('csv_user')
    * def primerRegistroCsv = { username: userCsvTest, password: '<password>' }
    
    Given request primerRegistroCsv
    When method post
    Then status 200

    * karate.log('Ejecutando caso Outline CSV: <description>')
    * def intentoDuplicadoCsv = { username: userCsvTest, password: '<password>' }
    Given request intentoDuplicadoCsv
    When method post
    Then status <expectedStatus>
    And match response.errorMessage == '<expectedErrorMessage>'

    Examples:
      | read('classpath:data/signup_cases.csv') |

