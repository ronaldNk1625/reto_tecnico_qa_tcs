package com.demoblaze.automation.tasks;

import static net.serenitybdd.screenplay.Tasks.instrumented;
import static net.serenitybdd.screenplay.matchers.WebElementStateMatchers.isClickable;
import static net.serenitybdd.screenplay.matchers.WebElementStateMatchers.isVisible;

import com.demoblaze.automation.interactions.AcceptAlert;
import com.demoblaze.automation.userinterfaces.HomePage;
import com.demoblaze.automation.userinterfaces.ProductDetailPage;
import com.demoblaze.automation.util.Constants;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.waits.WaitUntil;

public class AddProduct implements Task {

    private final String productName;

    public AddProduct(String productName) {
        this.productName = productName;
    }

    public static AddProduct named(String productName) {
        return instrumented(AddProduct.class, productName);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        actor.attemptsTo(
                WaitUntil.the(HomePage.PRODUCT_ITEM.of(productName), isVisible()).forNoMoreThan(15).seconds(),
                Click.on(HomePage.PRODUCT_ITEM.of(productName)),
                WaitUntil.the(ProductDetailPage.PRODUCT_NAME, isVisible()).forNoMoreThan(15).seconds(),
                WaitUntil.the(ProductDetailPage.ADD_TO_CART_BUTTON, isClickable()).forNoMoreThan(15).seconds(),
                Click.on(ProductDetailPage.ADD_TO_CART_BUTTON),
                AcceptAlert.withExpectedText(Constants.ALERT_PRODUCT_ADDED),
                WaitUntil.the(HomePage.NAV_HOME, isClickable()).forNoMoreThan(10).seconds(),
                Click.on(HomePage.NAV_HOME),
                WaitUntil.the(HomePage.PRODUCT_CARDS, isVisible()).forNoMoreThan(15).seconds()
        );
    }
}

