package com.example.ecommerce.api.dto;

import com.example.ecommerce.core.model.OrderStatus;
import java.time.LocalDateTime;
import java.util.List;

public class OrderDTO {
    private String id;
    private String userId;
    private List<String> productIds;
    private double totalAmount;
    private LocalDateTime orderDate;
    private OrderStatus status;
    
    public OrderDTO() {}
    
    public OrderDTO(String id, String userId, List<String> productIds, double totalAmount, 
                   LocalDateTime orderDate, OrderStatus status) {
        this.id = id;
        this.userId = userId;
        this.productIds = productIds;
        this.totalAmount = totalAmount;
        this.orderDate = orderDate;
        this.status = status;
    }
    
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    
    public String getUserId() { return userId; }
    public void setUserId(String userId) { this.userId = userId; }
    
    public List<String> getProductIds() { return productIds; }
    public void setProductIds(List<String> productIds) { this.productIds = productIds; }
    
    public double getTotalAmount() { return totalAmount; }
    public void setTotalAmount(double totalAmount) { this.totalAmount = totalAmount; }
    
    public LocalDateTime getOrderDate() { return orderDate; }
    public void setOrderDate(LocalDateTime orderDate) { this.orderDate = orderDate; }
    
    public OrderStatus getStatus() { return status; }
    public void setStatus(OrderStatus status) { this.status = status; }
}
