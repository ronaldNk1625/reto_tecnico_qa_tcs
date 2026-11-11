package com.demoblaze.automation.tasks;

import static net.serenitybdd.screenplay.Tasks.instrumented;
import static net.serenitybdd.screenplay.matchers.WebElementStateMatchers.isClickable;
import static net.serenitybdd.screenplay.matchers.WebElementStateMatchers.isVisible;

import com.demoblaze.automation.userinterfaces.ConfirmationModal;
import com.demoblaze.automation.userinterfaces.OrderModal;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.waits.WaitUntil;

public class FinishPurchase implements Task {

    public static FinishPurchase confirm() {
        return instrumented(FinishPurchase.class);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        actor.attemptsTo(
                WaitUntil.the(OrderModal.PURCHASE_BUTTON, isClickable()).forNoMoreThan(15).seconds(),
                Click.on(OrderModal.PURCHASE_BUTTON),
                WaitUntil.the(ConfirmationModal.TITLE_MESSAGE, isVisible()).forNoMoreThan(15).seconds()
        );
    }
}

