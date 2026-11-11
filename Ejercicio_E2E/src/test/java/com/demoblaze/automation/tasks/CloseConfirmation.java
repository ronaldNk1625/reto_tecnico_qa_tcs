package com.demoblaze.automation.tasks;

import static net.serenitybdd.screenplay.Tasks.instrumented;
import static net.serenitybdd.screenplay.matchers.WebElementStateMatchers.isClickable;

import com.demoblaze.automation.userinterfaces.ConfirmationModal;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.waits.WaitUntil;

public class CloseConfirmation implements Task {

    public static CloseConfirmation andFinish() {
        return instrumented(CloseConfirmation.class);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        actor.attemptsTo(
                WaitUntil.the(ConfirmationModal.CONFIRM_BUTTON, isClickable()).forNoMoreThan(15).seconds(),
                Click.on(ConfirmationModal.CONFIRM_BUTTON)
        );
    }
}

