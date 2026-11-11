package com.demoblaze.automation.interactions;

import static net.serenitybdd.screenplay.Tasks.instrumented;

import java.time.Duration;
import net.serenitybdd.core.Serenity;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Interaction;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import org.openqa.selenium.Alert;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AcceptAlert implements Interaction {

    private static final Logger LOGGER = LoggerFactory.getLogger(AcceptAlert.class);
    private final String expectedTextSubstring;
    private final int timeoutSeconds;

    public AcceptAlert(String expectedTextSubstring, int timeoutSeconds) {
        this.expectedTextSubstring = expectedTextSubstring;
        this.timeoutSeconds = timeoutSeconds;
    }

    public static AcceptAlert withExpectedText(String expectedText) {
        return instrumented(AcceptAlert.class, expectedText, 10);
    }

    public static AcceptAlert havingTimeout(int seconds) {
        return instrumented(AcceptAlert.class, null, seconds);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        WebDriver driver = BrowseTheWeb.as(actor).getDriver();
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(timeoutSeconds));

        try {
            Alert alert = wait.until(ExpectedConditions.alertIsPresent());
            String alertText = alert.getText();
            LOGGER.info("Alerta detectada con texto: '{}'", alertText);
            Serenity.recordReportData().withTitle("Alerta de navegador").andContents("Texto capturado: " + alertText);

            if (expectedTextSubstring != null && !expectedTextSubstring.isEmpty()) {
                if (!alertText.contains(expectedTextSubstring)) {
                    LOGGER.warn("El texto de la alerta '{}' no contiene el substring esperado '{}'", alertText, expectedTextSubstring);
                }
            }
            alert.accept();
            LOGGER.info("Alerta aceptada exitosamente.");
        } catch (Exception e) {
            LOGGER.error("No se presento la alerta en el tiempo especificado ({}s): {}", timeoutSeconds, e.getMessage());
            throw new RuntimeException("Fallo al esperar o aceptar la alerta nativa: " + e.getMessage(), e);
        }
    }
}

