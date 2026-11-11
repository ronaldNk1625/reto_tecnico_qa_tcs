package com.demoblaze.automation.model;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class OrderDetails {

    private String id;
    private String amount;
    private String cardNumber;
    private String name;
    private String date;
    private String rawText;

    public OrderDetails() {
    }

    public OrderDetails(String id, String amount, String cardNumber, String name, String date, String rawText) {
        this.id = id;
        this.amount = amount;
        this.cardNumber = cardNumber;
        this.name = name;
        this.date = date;
        this.rawText = rawText;
    }

    public static OrderDetails fromConfirmationText(String text) {
        OrderDetails details = new OrderDetails();
        details.setRawText(text);

        if (text == null || text.isEmpty()) {
            return details;
        }

        Pattern idPattern = Pattern.compile("Id:\\s*(\\d+)");
        Pattern amountPattern = Pattern.compile("Amount:\\s*(\\d+\\s*(?:USD)?)");
        Pattern cardPattern = Pattern.compile("Card Number:\\s*(\\w+)");
        Pattern namePattern = Pattern.compile("Name:\\s*(.+)");
        Pattern datePattern = Pattern.compile("Date:\\s*(.+)");

        Matcher idMatcher = idPattern.matcher(text);
        if (idMatcher.find()) {
            details.setId(idMatcher.group(1).trim());
        }

        Matcher amountMatcher = amountPattern.matcher(text);
        if (amountMatcher.find()) {
            details.setAmount(amountMatcher.group(1).trim());
        }

        Matcher cardMatcher = cardPattern.matcher(text);
        if (cardMatcher.find()) {
            details.setCardNumber(cardMatcher.group(1).trim());
        }

        Matcher nameMatcher = namePattern.matcher(text);
        if (nameMatcher.find()) {
            details.setName(nameMatcher.group(1).trim());
        }

        Matcher dateMatcher = datePattern.matcher(text);
        if (dateMatcher.find()) {
            details.setDate(dateMatcher.group(1).trim());
        }

        return details;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getAmount() {
        return amount;
    }

    public void setAmount(String amount) {
        this.amount = amount;
    }

    public String getCardNumber() {
        return cardNumber;
    }

    public void setCardNumber(String cardNumber) {
        this.cardNumber = cardNumber;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getRawText() {
        return rawText;
    }

    public void setRawText(String rawText) {
        this.rawText = rawText;
    }

    @Override
    public String toString() {
        return "OrderDetails{" +
                "id='" + id + '\'' +
                ", amount='" + amount + '\'' +
                ", cardNumber='" + cardNumber + '\'' +
                ", name='" + name + '\'' +
                ", date='" + date + '\'' +
                '}';
    }
}

