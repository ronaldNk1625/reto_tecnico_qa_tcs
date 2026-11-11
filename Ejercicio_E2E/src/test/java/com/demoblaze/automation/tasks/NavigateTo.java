package com.demoblaze.automation.tasks;

import static net.serenitybdd.screenplay.Tasks.instrumented;

import com.demoblaze.automation.userinterfaces.HomePage;
import com.demoblaze.automation.util.Constants;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.actions.Open;
import net.serenitybdd.screenplay.waits.WaitUntil;
import static net.serenitybdd.screenplay.matchers.WebElementStateMatchers.isVisible;

public class NavigateTo implements Task {

    private final String url;

    public NavigateTo(String url) {
        this.url = url;
    }

    public static NavigateTo theHomePage() {
        return instrumented(NavigateTo.class, Constants.DEMOBLAZE_URL);
    }

    public static NavigateTo theUrl(String url) {
        return instrumented(NavigateTo.class, url);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        actor.attemptsTo(
                Open.url(url),
                WaitUntil.the(HomePage.PRODUCT_CARDS, isVisible()).forNoMoreThan(15).seconds()
        );
    }
}

