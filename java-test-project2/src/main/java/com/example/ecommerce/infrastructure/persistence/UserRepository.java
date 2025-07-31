package com.example.ecommerce.infrastructure.persistence;

import com.example.ecommerce.core.model.User;
import com.example.ecommerce.infrastructure.config.DatabaseConfig;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class UserRepository {
    private final Map<String, User> users = new HashMap<>();
    private final DatabaseConfig dbConfig;
    
    public UserRepository(DatabaseConfig dbConfig) {
        this.dbConfig = dbConfig;
    }
    
    public void save(User user) {
        System.out.println("Connecting to: " + dbConfig.getConnectionString());
        users.put(user.getId(), user);
    }
    
    public User findById(String id) {
        return users.get(id);
    }
    
    public List<User> findAll() {
        return new ArrayList<>(users.values());
    }
    
    public void update(User user) {
        users.put(user.getId(), user);
    }
    
    public void delete(String id) {
        users.remove(id);
    }
}
