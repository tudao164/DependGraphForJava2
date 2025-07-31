package com.example.ecommerce.core.model;

import com.example.ecommerce.exception.InvalidOrderException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class Order {
    private String id;
    private User user;
    private List<Product> products;
    private double totalAmount;
    private LocalDateTime orderDate;
    private OrderStatus status;
    
    public Order(User user, List<Product> products) throws InvalidOrderException {
        if (user == null || products == null || products.isEmpty()) {
            throw new InvalidOrderException("Invalid order: user or products cannot be null/empty");
        }
        this.id = java.util.UUID.randomUUID().toString();
        this.user = user;
        this.products = new ArrayList<>(products);
        this.orderDate = LocalDateTime.now();
        this.status = OrderStatus.PENDING;
        this.totalAmount = calculateTotal();
    }
    
    private double calculateTotal() {
        return products.stream()
                .mapToDouble(Product::getPrice)
                .sum();
    }
    
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    
    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }
    
    public List<Product> getProducts() { return products; }
    public void setProducts(List<Product> products) { this.products = new ArrayList<>(products); }
    
    public double getTotalAmount() { return totalAmount; }
    public void setTotalAmount(double totalAmount) { this.totalAmount = totalAmount; }
    
    public LocalDateTime getOrderDate() { return orderDate; }
    public void setOrderDate(LocalDateTime orderDate) { this.orderDate = orderDate; }
    
    public OrderStatus getStatus() { return status; }
    public void setStatus(OrderStatus status) { this.status = status; }
}
