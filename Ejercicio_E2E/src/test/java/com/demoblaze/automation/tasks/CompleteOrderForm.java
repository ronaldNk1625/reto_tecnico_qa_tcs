package com.demoblaze.automation.tasks;

import static net.serenitybdd.screenplay.Tasks.instrumented;
import static net.serenitybdd.screenplay.matchers.WebElementStateMatchers.isClickable;
import static net.serenitybdd.screenplay.matchers.WebElementStateMatchers.isVisible;

import com.demoblaze.automation.model.CustomerInfo;
import com.demoblaze.automation.userinterfaces.CartPage;
import com.demoblaze.automation.userinterfaces.OrderModal;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.actions.Enter;
import net.serenitybdd.screenplay.waits.WaitUntil;

public class CompleteOrderForm implements Task {

    private final CustomerInfo customer;

    public CompleteOrderForm(CustomerInfo customer) {
        this.customer = customer;
    }

    public static CompleteOrderForm withCustomer(CustomerInfo customer) {
        return instrumented(CompleteOrderForm.class, customer);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        actor.attemptsTo(
                WaitUntil.the(CartPage.PLACE_ORDER_BUTTON, isClickable()).forNoMoreThan(15).seconds(),
                Click.on(CartPage.PLACE_ORDER_BUTTON),
                WaitUntil.the(OrderModal.NAME_INPUT, isVisible()).forNoMoreThan(15).seconds(),
                Enter.theValue(customer.getName()).into(OrderModal.NAME_INPUT),
                Enter.theValue(customer.getCountry()).into(OrderModal.COUNTRY_INPUT),
                Enter.theValue(customer.getCity()).into(OrderModal.CITY_INPUT),
                Enter.theValue(customer.getCreditCard()).into(OrderModal.CARD_INPUT),
                Enter.theValue(customer.getMonth()).into(OrderModal.MONTH_INPUT),
                Enter.theValue(customer.getYear()).into(OrderModal.YEAR_INPUT)
        );
    }
}

