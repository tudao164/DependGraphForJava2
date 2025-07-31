package com.example.ecommerce.infrastructure.persistence;

import com.example.ecommerce.core.model.Product;
import com.example.ecommerce.infrastructure.config.DatabaseConfig;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ProductRepository {
    private final Map<String, Product> products = new HashMap<>();
    private final DatabaseConfig dbConfig;
    
    public ProductRepository(DatabaseConfig dbConfig) {
        this.dbConfig = dbConfig;
    }
    
    public void save(Product product) {
        System.out.println("Connecting to: " + dbConfig.getConnectionString());
        products.put(product.getId(), product);
    }
    
    public Product findById(String id) {
        return products.get(id);
    }
    
    public List<Product> findAll() {
        return new ArrayList<>(products.values());
    }
    
    public void update(Product product) {
        products.put(product.getId(), product);
    }
    
    public void delete(String id) {
        products.remove(id);
    }
}
