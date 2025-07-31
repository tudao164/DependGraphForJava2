package com.example.ecommerce.core.model;

import com.example.ecommerce.util.StringUtils;

public class Product {
    private String id;
    private String name;
    private double price;
    private Category category;
    private int stockQuantity;
    
    public Product(String name, double price, int stockQuantity) {
        this.id = java.util.UUID.randomUUID().toString();
        this.name = StringUtils.sanitize(name);
        this.price = price;
        this.stockQuantity = stockQuantity;
    }
    
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = StringUtils.sanitize(name); }
    
    public double getPrice() { return price; }
    public void setPrice(double price) { this.price = price; }
    
    public Category getCategory() { return category; }
    public void setCategory(Category category) { this.category = category; }
    
    public int getStockQuantity() { return stockQuantity; }
    public void setStockQuantity(int stockQuantity) { this.stockQuantity = stockQuantity; }
}
