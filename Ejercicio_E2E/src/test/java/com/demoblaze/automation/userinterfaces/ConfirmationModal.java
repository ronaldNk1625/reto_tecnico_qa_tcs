package com.demoblaze.automation.userinterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public final class ConfirmationModal {

    private ConfirmationModal() {
    }

    public static final Target MODAL_CONTAINER = Target.the("Modal de confirmacion SweetAlert")
            .located(By.className("sweet-alert"));

    public static final Target TITLE_MESSAGE = Target.the("Titulo de confirmacion de compra")
            .locatedBy("//div[contains(@class,'sweet-alert')]//h2");

    public static final Target DETAILS_PARAGRAPH = Target.the("Parrafo de detalles de orden")
            .locatedBy("//div[contains(@class,'sweet-alert')]//p[contains(@class,'lead')]");

    public static final Target CONFIRM_BUTTON = Target.the("Boton OK de confirmacion")
            .locatedBy("//div[contains(@class,'sweet-alert')]//button[contains(@class,'confirm')]");
}

