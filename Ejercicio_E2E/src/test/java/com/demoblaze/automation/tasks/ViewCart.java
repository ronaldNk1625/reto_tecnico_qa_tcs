package com.demoblaze.automation.tasks;

import static net.serenitybdd.screenplay.Tasks.instrumented;
import static net.serenitybdd.screenplay.matchers.WebElementStateMatchers.isClickable;
import static net.serenitybdd.screenplay.matchers.WebElementStateMatchers.isVisible;

import com.demoblaze.automation.userinterfaces.CartPage;
import com.demoblaze.automation.userinterfaces.HomePage;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.waits.WaitUntil;

public class ViewCart implements Task {

    public static ViewCart onScreen() {
        return instrumented(ViewCart.class);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        actor.attemptsTo(
                WaitUntil.the(HomePage.NAV_CART, isClickable()).forNoMoreThan(15).seconds(),
                Click.on(HomePage.NAV_CART),
                WaitUntil.the(CartPage.PLACE_ORDER_BUTTON, isClickable()).forNoMoreThan(15).seconds(),
                WaitUntil.the(CartPage.PRODUCT_ROWS, isVisible()).forNoMoreThan(15).seconds()
        );
    }
}

