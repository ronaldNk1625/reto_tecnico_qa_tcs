package com.demoblaze.automation.model;

public class ProductOrder {

    private String firstProduct;
    private String secondProduct;

    public ProductOrder() {
    }

    public ProductOrder(String firstProduct, String secondProduct) {
        this.firstProduct = firstProduct;
        this.secondProduct = secondProduct;
    }

    public String getFirstProduct() {
        return firstProduct;
    }

    public void setFirstProduct(String firstProduct) {
        this.firstProduct = firstProduct;
    }

    public String getSecondProduct() {
        return secondProduct;
    }

    public void setSecondProduct(String secondProduct) {
        this.secondProduct = secondProduct;
    }
}

