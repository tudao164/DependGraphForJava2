package com.example.demo.dto;

import com.example.demo.entity.Order;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class OrderStatusUpdateDTO {
    @NotNull(message = "Status is required")
    private Order.OrderStatus status;
}