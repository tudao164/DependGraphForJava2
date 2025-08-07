package com.example.demo.dto;

import com.example.demo.entity.Order;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class OrderDTO {
    private String id;
    private String userId;
    private List<OrderItemDTO> items;
    private BigDecimal totalAmount;
    private Order.OrderStatus status;
    private String statusDisplay; // Hiển thị tiếng Việt
    private String shippingAddress;
    private String phoneNumber;
    private Date orderDate;
    private Date deliveryDate;
}