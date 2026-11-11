package com.demoblaze.automation.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Map;

@JsonIgnoreProperties(ignoreUnknown = true)
public class CustomerInfo {

    @JsonProperty("nombre")
    private String name;

    @JsonProperty("pais")
    private String country;

    @JsonProperty("ciudad")
    private String city;

    @JsonProperty("tarjeta")
    private String creditCard;

    @JsonProperty("mes")
    private String month;

    @JsonProperty("anio")
    private String year;

    public CustomerInfo() {
    }

    public CustomerInfo(String name, String country, String city, String creditCard, String month, String year) {
        this.name = name;
        this.country = country;
        this.city = city;
        this.creditCard = creditCard;
        this.month = month;
        this.year = year;
    }

    public static CustomerInfo fromMap(Map<String, String> data) {
        return new CustomerInfo(
                data.getOrDefault("nombre", data.getOrDefault("name", "")),
                data.getOrDefault("pais", data.getOrDefault("country", "")),
                data.getOrDefault("ciudad", data.getOrDefault("city", "")),
                data.getOrDefault("tarjeta", data.getOrDefault("creditCard", data.getOrDefault("card", ""))),
                data.getOrDefault("mes", data.getOrDefault("month", "")),
                data.getOrDefault("anio", data.getOrDefault("year", ""))
        );
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getCreditCard() {
        return creditCard;
    }

    public void setCreditCard(String creditCard) {
        this.creditCard = creditCard;
    }

    public String getMonth() {
        return month;
    }

    public void setMonth(String month) {
        this.month = month;
    }

    public String getYear() {
        return year;
    }

    public void setYear(String year) {
        this.year = year;
    }

    @Override
    public String toString() {
        return "CustomerInfo{" +
                "name='" + name + '\'' +
                ", country='" + country + '\'' +
                ", city='" + city + '\'' +
                ", creditCard='" + creditCard + '\'' +
                ", month='" + month + '\'' +
                ", year='" + year + '\'' +
                '}';
    }
}

