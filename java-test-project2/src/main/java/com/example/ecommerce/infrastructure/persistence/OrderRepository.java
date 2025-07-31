package com.example.ecommerce.infrastructure.persistence;

import com.example.ecommerce.core.model.Order;
import com.example.ecommerce.core.model.User;
import com.example.ecommerce.infrastructure.config.DatabaseConfig;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class OrderRepository {
    private final Map<String, Order> orders = new HashMap<>();
    private final DatabaseConfig dbConfig;
    
    public OrderRepository(DatabaseConfig dbConfig) {
        this.dbConfig = dbConfig;
    }
    
    public void save(Order order) {
        System.out.println("Connecting to: " + dbConfig.getConnectionString());
        orders.put(order.getId(), order);
    }
    
    public Order findById(String id) {
        return orders.get(id);
    }
    
    public List<Order> findAll() {
        return new ArrayList<>(orders.values());
    }
    
    public List<Order> findByUser(User user) {
        return orders.values().stream()
                .filter(order -> order.getUser().getId().equals(user.getId()))
                .collect(Collectors.toList());
    }
    
    public void update(Order order) {
        orders.put(order.getId(), order);
    }
    
    public void delete(String id) {
        orders.remove(id);
    }
}
