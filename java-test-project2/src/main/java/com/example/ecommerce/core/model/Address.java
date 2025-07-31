package com.example.ecommerce.core.model;

import com.example.ecommerce.util.StringUtils;

public class Address {
    private String id;
    private String street;
    private String city;
    private String state;
    private String zipCode;
    private String country;
    
    public Address(String street, String city, String state, String zipCode, String country) {
        this.id = java.util.UUID.randomUUID().toString();
        this.street = StringUtils.sanitize(street);
        this.city = StringUtils.sanitize(city);
        this.state = StringUtils.sanitize(state);
        this.zipCode = StringUtils.sanitize(zipCode);
        this.country = StringUtils.sanitize(country);
    }
    
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    
    public String getStreet() { return street; }
    public void setStreet(String street) { this.street = StringUtils.sanitize(street); }
    
    public String getCity() { return city; }
    public void setCity(String city) { this.city = StringUtils.sanitize(city); }
    
    public String getState() { return state; }
    public void setState(String state) { this.state = StringUtils.sanitize(state); }
    
    public String getZipCode() { return zipCode; }
    public void setZipCode(String zipCode) { this.zipCode = StringUtils.sanitize(zipCode); }
    
    public String getCountry() { return country; }
    public void setCountry(String country) { this.country = StringUtils.sanitize(country); }
}
