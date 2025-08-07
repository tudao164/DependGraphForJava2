package com.example.demo.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class OrderItemDTO {
    private String id;
    private Long productId;
    private String productName;
    private String productImageUrl;
    private BigDecimal price;
    private int quantity;
    private BigDecimal subtotal;
}