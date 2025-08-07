package com.example.demo.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.math.BigDecimal;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CartItemResponseDTO {
    private String id; // Changed from Long to String
    private Long productId;
    private String productName;
    private String productImageUrl;
    private BigDecimal productPrice;
    private int quantity;
    private BigDecimal subtotal;
}