================================================================================
PROYECTO DE AUTOMATIZACION E2E CON SERENITY BDD & SCREENPLAY - DEMOBLAZE
================================================================================
Candidato: Ronald Berrones
Prueba Tecnica: QA Automation Engineer (Banco Pichincha / TCS)
Fecha: Noviembre 2026
Sitio Bajo Prueba: https://www.demoblaze.com/
Framework: Serenity BDD 4.1.20 + Cucumber 7 + Screenplay Pattern + Java 17 + Maven
================================================================================

--------------------------------------------------------------------------------
1. DESCRIPCION DEL PROYECTO
--------------------------------------------------------------------------------
Este proyecto implementa una suite de automatizacion de pruebas de extremo a
extremo (E2E) para el flujo completo de compra en la tienda virtual Demoblaze.
La solucion esta construida bajo el patron de arquitectura Screenplay Pattern,
el cual desacopla responsabilidades, maximiza la reusabilidad y legibilidad,
y proporciona un modelo orientado a tareas del actor y objetivos de negocio.

El flujo automatizado cubre:
 1. Navegacion a la pagina principal y carga del catalogo de productos.
 2. Seleccion y adicion de dos productos al carrito de compras, gestionando
    apropiadamente las alertas nativas (window.alert) del navegador.
 3. Visualizacion y verificacion del carrito de compras (presencia de items).
 4. Diligenciamiento del formulario de compra en modal Bootstrap (Order Modal).
 5. Finalizacion de la compra y validacion de la orden generada (SweetAlert:
    mensaje de confirmacion, ID de orden, monto total y tarjeta).

--------------------------------------------------------------------------------
2. REQUISITOS PREVIOS DEL SISTEMA
--------------------------------------------------------------------------------
Asegurese de contar con las siguientes herramientas instaladas y configuradas:
 - Java Development Kit (JDK): Version 17 o superior.
     Verificar en consola: java -version
 - Apache Maven: Version 3.8.x o superior.
     Verificar en consola: mvn -version
 - Google Chrome: Version reciente instalada en el sistema.
     (Selenium Manager 4 gestiona el driver automaticamente).

--------------------------------------------------------------------------------
3. ESTRUCTURA DEL PROYECTO (SCREENPLAY PATTERN)
--------------------------------------------------------------------------------
Ejercicio_E2E/
  ├── pom.xml                                   # Gestion de dependencias y plugins
  ├── serenity.properties                       # Configuraciones globales de Serenity
  ├── readme.txt                                # Manual de ejecucion e instrucciones
  ├── README.md                                 # Documentacion detallada en Markdown
  ├── conclusiones.txt                          # Hallazgos, observaciones y opiniones
  ├── conclusiones.md                           # Informe extendido de conclusiones
  └── src/test/
      ├── java/com/demoblaze/automation/
      │   ├── model/                            # Modelos de dominio y DTOs
      │   │   ├── CustomerInfo.java             # Informacion del cliente y formulario
      │   │   ├── OrderDetails.java             # Datos parseados de la confirmacion
      │   │   └── ProductOrder.java             # Representacion de productos
      │   ├── userinterfaces/                   # Mapeo de elementos de la interfaz (Target)
      │   │   ├── HomePage.java                 # Elementos del catalogo y barra superior
      │   │   ├── ProductDetailPage.java        # Detalle de producto y boton Add to cart
      │   │   ├── CartPage.java                 # Tabla del carrito, total y boton Order
      │   │   ├── OrderModal.java               # Formulario de compra (campos y botones)
      │   │   └── ConfirmationModal.java        # Modal SweetAlert con resultado de compra
      │   ├── tasks/                            # Tareas de alto nivel del Actor
      │   │   ├── NavigateTo.java               # Apertura de la aplicacion
      │   │   ├── AddProduct.java               # Seleccion, agregar y manejo de alert
      │   │   ├── ViewCart.java                 # Acceso y espera a la vista del carrito
      │   │   ├── CompleteOrderForm.java        # Diligenciamiento de campos de orden
      │   │   ├── FinishPurchase.java           # Clic en Purchase y envio
      │   │   └── CloseConfirmation.java        # Cierre del modal con boton OK
      │   ├── interactions/                     # Acciones atomicas de bajo nivel
      │   │   └── AcceptAlert.java              # Espera explicita y aceptacion de alert
      │   ├── questions/                        # Validaciones y aserciones Screenplay
      │   │   ├── TheCartProducts.java          # Verifica productos visibles en carrito
      │   │   ├── TheCartTotal.java             # Obtiene el monto total del carrito
      │   │   ├── TheConfirmationMessage.java   # Valida el titulo de confirmacion
      │   │   └── TheOrderDetails.java          # Parsea y valida ID, monto y tarjeta
      │   ├── stepdefinitions/                  # Glue code Cucumber
      │   │   ├── Hook.java                     # Inicializacion del Stage / OnlineCast
      │   │   └── PurchaseStepDefinitions.java  # Implementacion de pasos Gherkin
      │   ├── runners/                          # Runner de ejecucion JUnit
      │   │   └── PurchaseRunner.java           # Runner con CucumberWithSerenity
      │   └── util/                             # Utilitarios y helpers
      │       ├── Constants.java                # Constantes de URLs y textos
      │       ├── JsonReader.java               # Consumo de datos desde archivo JSON
      │       └── CsvReader.java                # Consumo de datos desde archivo CSV
      └── resources/
          ├── serenity.conf                     # Configuracion de WebDriver y Chrome
          ├── features/
          │   └── purchase_flow.feature         # Especificaciones en Gherkin
          └── data/
              ├── datos_compra.json             # Archivo de datos de prueba en JSON
              └── datos_compra.csv              # Archivo de datos de prueba en CSV

--------------------------------------------------------------------------------
4. COMANDOS DE EJECUCION PASO A PASO
--------------------------------------------------------------------------------
Abra una terminal de comandos en la carpeta raiz del ejercicio:
    cd reto_tecnico_qa_tcs/Ejercicio_E2E

OPCION 1: Ejecucion completa de toda la suite
    mvn clean verify

OPCION 2: Ejecucion del escenario principal de humo (Smoke)
    mvn verify "-Dcucumber.filter.tags=@Smoke"

OPCION 3: Ejecucion de los escenarios parametrizados (Scenario Outline)
    mvn verify "-Dcucumber.filter.tags=@EsquemaEscenario"

OPCION 4: Ejecucion con consumo de datos desde JSON
    mvn verify "-Dcucumber.filter.tags=@ConsumoJson"

OPCION 5: Ejecucion con consumo de datos desde CSV
    mvn verify "-Dcucumber.filter.tags=@ConsumoCsv"

OPCION 6: Ejecucion en modo Headless (sin abrir ventana de navegador)
    mvn verify "-Dheadless.mode=true"

OPCION 7: Generar / Regenerar reporte agregado de Serenity manualmente
    mvn serenity:aggregate

--------------------------------------------------------------------------------
5. UBICACION Y CONSULTA DE REPORTES
--------------------------------------------------------------------------------
Una vez finalizada la ejecucion, los reportes se generan automaticamente en:

A. Reporte HTML de Serenity BDD (Recomendado para evaluacion ejecutiva y tecnica):
   Ruta relativa: target/site/serenity/index.html
   Ruta absoluta tipica: D:/Prueba_tecnica_tata/reto_tecnico_qa_tcs/Ejercicio_E2E/target/site/serenity/index.html
   Para abrirlo directamente desde PowerShell en Windows:
       Start-Process "target/site/serenity/index.html"

B. Reportes de Cucumber:
   - Reporte HTML: target/cucumber-reports/cucumber.html
   - Reporte JSON: target/cucumber-reports/cucumber.json
   Para abrir el reporte de Cucumber:
       Start-Process "target/cucumber-reports/cucumber.html"

--------------------------------------------------------------------------------
6. CONTACTO Y AUTORIA
--------------------------------------------------------------------------------
Autor: Ronald Berrones
Perfil: QA Automation Engineer
Repositorio Git: https://github.com/ronaldNk1625/reto_tecnico_qa_tcs.git
================================================================================

