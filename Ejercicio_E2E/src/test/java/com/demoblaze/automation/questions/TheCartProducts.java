package com.demoblaze.automation.questions;

import com.demoblaze.automation.userinterfaces.CartPage;
import java.util.List;
import java.util.stream.Collectors;
import net.serenitybdd.core.pages.WebElementFacade;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Question;

public class TheCartProducts implements Question<List<String>> {

    public static TheCartProducts displayed() {
        return new TheCartProducts();
    }

    @Override
    public List<String> answeredBy(Actor actor) {
        List<WebElementFacade> rows = CartPage.PRODUCT_TITLES.resolveAllFor(actor);
        return rows.stream()
                .map(WebElementFacade::getText)
                .map(String::trim)
                .collect(Collectors.toList());
    }
}

