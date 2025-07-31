package com.example.ecommerce.core.model;

import com.example.ecommerce.util.StringUtils;

public class Category {
    private String id;
    private String name;
    private String description;
    private Category parentCategory;
    
    public Category(String name, String description) {
        this.id = java.util.UUID.randomUUID().toString();
        this.name = StringUtils.sanitize(name);
        this.description = StringUtils.sanitize(description);
    }
    
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = StringUtils.sanitize(name); }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = StringUtils.sanitize(description); }
    
    public Category getParentCategory() { return parentCategory; }
    public void setParentCategory(Category parentCategory) { this.parentCategory = parentCategory; }
}
