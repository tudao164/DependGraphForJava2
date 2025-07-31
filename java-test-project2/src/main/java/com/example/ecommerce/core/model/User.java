package com.example.ecommerce.core.model;

import com.example.ecommerce.util.StringUtils;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class User {
    private String id;
    private String name;
    private String email;
    private List<Order> orders;
    private Address address;
    private UserRole role;
    
    public User(String name, String email) {
        this.id = UUID.randomUUID().toString();
        this.name = StringUtils.sanitize(name);
        this.email = StringUtils.sanitize(email);
        this.orders = new ArrayList<>();
        this.role = UserRole.CUSTOMER;
    }
    
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = StringUtils.sanitize(name); }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = StringUtils.sanitize(email); }
    
    public List<Order> getOrders() { return orders; }
    public void addOrder(Order order) { this.orders.add(order); }
    
    public Address getAddress() { return address; }
    public void setAddress(Address address) { this.address = address; }
    
    public UserRole getRole() { return role; }
    public void setRole(UserRole role) { this.role = role; }
}
