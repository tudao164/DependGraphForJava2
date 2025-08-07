package com.example.demo.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CartDTO {
    private String id;
    private String userId; // Đã sửa từ Long thành String
    private List<CartItemResponseDTO> items;
    private double totalPrice;
}
