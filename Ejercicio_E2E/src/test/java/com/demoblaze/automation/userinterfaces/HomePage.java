package com.demoblaze.automation.userinterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public final class HomePage {

    private HomePage() {
    }

    public static final Target PRODUCT_CARDS = Target.the("Tarjetas de productos en el catalogo")
            .located(By.cssSelector("#tbodyid .card"));

    public static final Target PRODUCT_ITEM = Target.the("Enlace del producto {0}")
            .locatedBy("//div[@id='tbodyid']//a[normalize-space(text())='{0}']");

    public static final Target NAV_HOME = Target.the("Enlace Home de navegacion")
            .locatedBy("//a[contains(@class,'nav-link') and contains(text(),'Home')]");

    public static final Target NAV_BRAND = Target.the("Logo de la marca Demoblaze")
            .located(By.className("navbar-brand"));

    public static final Target NAV_CART = Target.the("Enlace Cart de navegacion")
            .located(By.id("cartur"));
}

