package com.example.ecommerce.api.dto;

import com.example.ecommerce.core.model.Address;
import com.example.ecommerce.core.model.UserRole;

public class UserDTO {
    private String id;
    private String name;
    private String email;
    private Address address;
    private UserRole role;
    
    public UserDTO() {}
    
    public UserDTO(String id, String name, String email, Address address, UserRole role) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.address = address;
        this.role = role;
    }
    
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    public Address getAddress() { return address; }
    public void setAddress(Address address) { this.address = address; }
    
    public UserRole getRole() { return role; }
    public void setRole(UserRole role) { this.role = role; }
}
