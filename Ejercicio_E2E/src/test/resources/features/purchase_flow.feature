#language: es
@Demoblaze @CompraE2E
Característica: Flujo de compra de extremo a extremo en la tienda virtual Demoblaze
  Como un usuario de la tienda Demoblaze
  Quiero seleccionar dos productos, agregarlos al carrito y completar el formulario de pedido
  Para finalizar una compra exitosa y obtener la confirmación con los datos de mi orden

  Antecedentes:
    Dado que el cliente se encuentra en la pagina principal de Demoblaze

  @Smoke @Regresion @FlujoCompleto
  Escenario: Compra exitosa de dos productos en Demoblaze
    Cuando el cliente agrega los productos "Samsung galaxy s6" y "Nokia lumia 1520" al carrito
    Y visualiza el carrito de compras verificando los productos agregados
    Y completa el formulario de compra con los datos del cliente:
      | nombre          | pais    | ciudad   | tarjeta          | mes | anio |
      | Ronald Berrones | Ecuador | Riobamba | 1234567890123456 | 06  | 2026 |
    Y finaliza la compra
    Entonces visualiza el mensaje de confirmacion "Thank you for your purchase!"
    Y verifica que los detalles de la orden contengan el monto correspondiente y la tarjeta "1234567890123456"

  @EsquemaEscenario @DataDriven
  Esquema del escenario: Compra exitosa parametrizada con multiples productos y clientes
    Cuando el cliente agrega los productos "<producto1>" y "<producto2>" al carrito
    Y visualiza el carrito de compras verificando los productos agregados
    Y completa el formulario de compra con los datos del cliente:
      | nombre   | pais   | ciudad   | tarjeta   | mes   | anio   |
      | <nombre> | <pais> | <ciudad> | <tarjeta> | <mes> | <anio> |
    Y finaliza la compra
    Entonces visualiza el mensaje de confirmacion "Thank you for your purchase!"
    Y verifica que los detalles de la orden contengan el monto correspondiente y la tarjeta "<tarjeta>"

    Ejemplos:
      | producto1         | producto2        | nombre          | pais     | ciudad   | tarjeta          | mes | anio |
      | Samsung galaxy s6 | Nokia lumia 1520 | Ronald Berrones | Ecuador  | Riobamba | 1234567890123456 | 06  | 2026 |
      | Nexus 6           | Sony xperia z5   | Maria Gomez     | Colombia | Bogota   | 9876543210987654 | 11  | 2025 |

  @ConsumoJson
  Esquema del escenario: Compra exitosa consumiendo datos externos desde archivo JSON
    Cuando el cliente realiza la compra consumiendo el archivo JSON "<archivoJson>" con identificador "<idTest>"
    Entonces visualiza el mensaje de confirmacion "Thank you for your purchase!"

    Ejemplos:
      | archivoJson              | idTest |
      | data/datos_compra.json   | TC01   |

  @ConsumoCsv
  Esquema del escenario: Compra exitosa consumiendo datos externos desde archivo CSV
    Cuando el cliente realiza la compra consumiendo el archivo CSV "<archivoCsv>" con identificador "<idTest>"
    Entonces visualiza el mensaje de confirmacion "Thank you for your purchase!"

    Ejemplos:
      | archivoCsv              | idTest |
      | data/datos_compra.csv   | TC01   |

