package com.demoblaze.automation.userinterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public final class OrderModal {

    private OrderModal() {
    }

    public static final Target MODAL_CONTAINER = Target.the("Modal de orden de compra")
            .located(By.id("orderModal"));

    public static final Target NAME_INPUT = Target.the("Campo Nombre")
            .located(By.id("name"));

    public static final Target COUNTRY_INPUT = Target.the("Campo Pais")
            .located(By.id("country"));

    public static final Target CITY_INPUT = Target.the("Campo Ciudad")
            .located(By.id("city"));

    public static final Target CARD_INPUT = Target.the("Campo Tarjeta de Credito")
            .located(By.id("card"));

    public static final Target MONTH_INPUT = Target.the("Campo Mes")
            .located(By.id("month"));

    public static final Target YEAR_INPUT = Target.the("Campo Anio")
            .located(By.id("year"));

    public static final Target PURCHASE_BUTTON = Target.the("Boton Purchase para completar orden")
            .locatedBy("//button[contains(@class,'btn-primary') and normalize-space(text())='Purchase']");

    public static final Target CLOSE_BUTTON = Target.the("Boton Close del modal")
            .locatedBy("//div[@id='orderModal']//button[normalize-space(text())='Close']");
}

