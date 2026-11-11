package com.demoblaze.automation.questions;

import com.demoblaze.automation.userinterfaces.ConfirmationModal;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Question;

public class TheConfirmationMessage implements Question<String> {

    public static TheConfirmationMessage displayed() {
        return new TheConfirmationMessage();
    }

    @Override
    public String answeredBy(Actor actor) {
        return ConfirmationModal.TITLE_MESSAGE.resolveFor(actor).getText().trim();
    }
}

