package com.demoblaze.automation.userinterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public final class ProductDetailPage {

    private ProductDetailPage() {
    }

    public static final Target PRODUCT_NAME = Target.the("Titulo o nombre del producto")
            .located(By.className("name"));

    public static final Target PRODUCT_PRICE = Target.the("Precio del producto")
            .located(By.className("price-container"));

    public static final Target ADD_TO_CART_BUTTON = Target.the("Boton agregar al carrito")
            .locatedBy("//a[contains(@class,'btn') and contains(text(),'Add to cart')]");
}

