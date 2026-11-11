package com.demoblaze.automation.questions;

import com.demoblaze.automation.model.OrderDetails;
import com.demoblaze.automation.userinterfaces.ConfirmationModal;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Question;

public class TheOrderDetails implements Question<OrderDetails> {

    public static TheOrderDetails generated() {
        return new TheOrderDetails();
    }

    @Override
    public OrderDetails answeredBy(Actor actor) {
        String detailsText = ConfirmationModal.DETAILS_PARAGRAPH.resolveFor(actor).getText();
        return OrderDetails.fromConfirmationText(detailsText);
    }
}

