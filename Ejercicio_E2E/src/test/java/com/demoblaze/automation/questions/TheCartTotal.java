package com.demoblaze.automation.questions;

import com.demoblaze.automation.userinterfaces.CartPage;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Question;

public class TheCartTotal implements Question<String> {

    public static TheCartTotal displayed() {
        return new TheCartTotal();
    }

    @Override
    public String answeredBy(Actor actor) {
        if (!CartPage.TOTAL_PRICE.resolveFor(actor).isVisible()) {
            return "0";
        }
        return CartPage.TOTAL_PRICE.resolveFor(actor).getText().trim();
    }
}

