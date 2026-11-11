package com.demoblaze.automation.stepdefinitions;

import static net.serenitybdd.screenplay.actors.OnStage.theActorCalled;
import static net.serenitybdd.screenplay.actors.OnStage.theActorInTheSpotlight;
import static org.assertj.core.api.Assertions.assertThat;

import com.demoblaze.automation.model.CustomerInfo;
import com.demoblaze.automation.model.OrderDetails;
import com.demoblaze.automation.questions.TheCartProducts;
import com.demoblaze.automation.questions.TheConfirmationMessage;
import com.demoblaze.automation.questions.TheOrderDetails;
import com.demoblaze.automation.tasks.AddProduct;
import com.demoblaze.automation.tasks.CloseConfirmation;
import com.demoblaze.automation.tasks.CompleteOrderForm;
import com.demoblaze.automation.tasks.FinishPurchase;
import com.demoblaze.automation.tasks.NavigateTo;
import com.demoblaze.automation.tasks.ViewCart;
import com.demoblaze.automation.util.CsvReader;
import com.demoblaze.automation.util.JsonReader;
import com.fasterxml.jackson.databind.JsonNode;
import io.cucumber.datatable.DataTable;
import io.cucumber.java.es.Cuando;
import io.cucumber.java.es.Dado;
import io.cucumber.java.es.Entonces;
import java.util.List;
import java.util.Map;

public class PurchaseStepDefinitions {

    @Dado("que el cliente se encuentra en la pagina principal de Demoblaze")
    public void queElClienteSeEncuentraEnLaPaginaPrincipalDeDemoblaze() {
        theActorCalled("Cliente Demoblaze").wasAbleTo(
                NavigateTo.theHomePage()
        );
    }

    @Cuando("el cliente agrega los productos {string} y {string} al carrito")
    public void elClienteAgregaLosProductosYAlCarrito(String producto1, String producto2) {
        theActorInTheSpotlight().remember("PRODUCTO_1", producto1);
        theActorInTheSpotlight().remember("PRODUCTO_2", producto2);

        theActorInTheSpotlight().attemptsTo(
                AddProduct.named(producto1),
                AddProduct.named(producto2)
        );
    }

    @Cuando("visualiza el carrito de compras verificando los productos agregados")
    public void visualizaElCarritoDeComprasVerificandoLosProductosAgregados() {
        theActorInTheSpotlight().attemptsTo(
                ViewCart.onScreen()
        );

        String p1 = theActorInTheSpotlight().recall("PRODUCTO_1");
        String p2 = theActorInTheSpotlight().recall("PRODUCTO_2");

        List<String> itemsEnCarrito = theActorInTheSpotlight().asksFor(TheCartProducts.displayed());
        assertThat(itemsEnCarrito)
                .as("Verificar que ambos productos seleccionados esten en la tabla del carrito")
                .contains(p1, p2);
    }

    @Cuando("completa el formulario de compra con los datos del cliente:")
    public void completaElFormularioDeCompraConLosDatosDelCliente(DataTable dataTable) {
        List<Map<String, String>> rows = dataTable.asMaps(String.class, String.class);
        CustomerInfo customer = CustomerInfo.fromMap(rows.get(0));
        theActorInTheSpotlight().remember("CUSTOMER_INFO", customer);

        theActorInTheSpotlight().attemptsTo(
                CompleteOrderForm.withCustomer(customer)
        );
    }

    @Cuando("finaliza la compra")
    public void finalizaLaCompra() {
        theActorInTheSpotlight().attemptsTo(
                FinishPurchase.confirm()
        );
    }

    @Entonces("visualiza el mensaje de confirmacion {string}")
    public void visualizaElMensajeDeConfirmacion(String mensajeEsperado) {
        String mensajeActual = theActorInTheSpotlight().asksFor(TheConfirmationMessage.displayed());
        assertThat(mensajeActual)
                .as("Verificar mensaje de confirmacion de la compra")
                .isEqualTo(mensajeEsperado);
    }

    @Entonces("verifica que los detalles de la orden contengan el monto correspondiente y la tarjeta {string}")
    public void verificaQueLosDetallesDeLaOrdenContenganElMontoCorrespondienteYLaTarjeta(String tarjetaEsperada) {
        OrderDetails details = theActorInTheSpotlight().asksFor(TheOrderDetails.generated());

        assertThat(details.getId())
                .as("Verificar que la orden genero un ID")
                .isNotBlank();

        assertThat(details.getCardNumber())
                .as("Verificar que el numero de tarjeta coincide")
                .contains(tarjetaEsperada);

        theActorInTheSpotlight().attemptsTo(
                CloseConfirmation.andFinish()
        );
    }

    @Cuando("el cliente realiza la compra consumiendo el archivo JSON {string} con identificador {string}")
    public void elClienteRealizaLaCompraConsumiendoElArchivoJSONConIdentificador(String archivoJson, String idTest) {
        JsonNode testData = JsonReader.getTestCaseById(archivoJson, idTest);

        String producto1 = testData.get("producto1").asText();
        String producto2 = testData.get("producto2").asText();

        JsonNode clienteNode = testData.get("cliente");
        CustomerInfo customer = new CustomerInfo(
                clienteNode.get("nombre").asText(),
                clienteNode.get("pais").asText(),
                clienteNode.get("ciudad").asText(),
                clienteNode.get("tarjeta").asText(),
                clienteNode.get("mes").asText(),
                clienteNode.get("anio").asText()
        );

        theActorInTheSpotlight().remember("PRODUCTO_1", producto1);
        theActorInTheSpotlight().remember("PRODUCTO_2", producto2);
        theActorInTheSpotlight().remember("CUSTOMER_INFO", customer);

        theActorInTheSpotlight().attemptsTo(
                AddProduct.named(producto1),
                AddProduct.named(producto2),
                ViewCart.onScreen()
        );

        List<String> itemsEnCarrito = theActorInTheSpotlight().asksFor(TheCartProducts.displayed());
        assertThat(itemsEnCarrito).contains(producto1, producto2);

        theActorInTheSpotlight().attemptsTo(
                CompleteOrderForm.withCustomer(customer),
                FinishPurchase.confirm()
        );
    }

    @Cuando("el cliente realiza la compra consumiendo el archivo CSV {string} con identificador {string}")
    public void elClienteRealizaLaCompraConsumiendoElArchivoCSVConIdentificador(String archivoCsv, String idTest) {
        Map<String, String> row = CsvReader.getTestCaseById(archivoCsv, idTest);

        String producto1 = row.get("producto1");
        String producto2 = row.get("producto2");

        CustomerInfo customer = CustomerInfo.fromMap(row);

        theActorInTheSpotlight().remember("PRODUCTO_1", producto1);
        theActorInTheSpotlight().remember("PRODUCTO_2", producto2);
        theActorInTheSpotlight().remember("CUSTOMER_INFO", customer);

        theActorInTheSpotlight().attemptsTo(
                AddProduct.named(producto1),
                AddProduct.named(producto2),
                ViewCart.onScreen()
        );

        List<String> itemsEnCarrito = theActorInTheSpotlight().asksFor(TheCartProducts.displayed());
        assertThat(itemsEnCarrito).contains(producto1, producto2);

        theActorInTheSpotlight().attemptsTo(
                CompleteOrderForm.withCustomer(customer),
                FinishPurchase.confirm()
        );
    }
}

