package com.demoblaze.automation.userinterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public final class CartPage {

    private CartPage() {
    }

    public static final Target PRODUCT_ROWS = Target.the("Filas de productos en la tabla del carrito")
            .locatedBy("//tbody[@id='tbodyid']/tr");

    public static final Target PRODUCT_NAME_CELL = Target.the("Celda de nombre para el producto {0}")
            .locatedBy("//tbody[@id='tbodyid']//td[normalize-space(text())='{0}']");

    public static final Target PRODUCT_TITLES = Target.the("Lista de titulos de productos en el carrito")
            .locatedBy("//tbody[@id='tbodyid']/tr/td[2]");

    public static final Target TOTAL_PRICE = Target.the("Precio total acumulado en el carrito")
            .located(By.id("totalp"));

    public static final Target PLACE_ORDER_BUTTON = Target.the("Boton Place Order")
            .locatedBy("//button[contains(@class,'btn-success') and contains(text(),'Place Order')]");
}

