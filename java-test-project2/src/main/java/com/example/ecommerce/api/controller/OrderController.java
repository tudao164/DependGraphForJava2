package com.example.ecommerce.api.controller;

import com.example.ecommerce.api.dto.OrderDTO;
import com.example.ecommerce.core.model.Order;
import com.example.ecommerce.core.service.OrderService;
import com.example.ecommerce.exception.InvalidInputException;
import com.example.ecommerce.util.StringUtils;
import java.util.Arrays;

public class OrderController {
    private final OrderService orderService;
    
    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }
    
    public OrderDTO createOrder(String userId, String productId) throws InvalidInputException {
        if (StringUtils.isEmpty(userId) || StringUtils.isEmpty(productId)) {
            throw new InvalidInputException("User ID and Product ID are required");
        }
        Order order = orderService.createOrder(userId, Arrays.asList(productId));
        return convertToDTO(order);
    }
    
    private OrderDTO convertToDTO(Order order) {
        return new OrderDTO(
            order.getId(),
            order.getUser().getId(),
            order.getProducts().stream().map(Product::getId).collect(Collectors.toList()),
            order.getTotalAmount(),
            order.getOrderDate(),
            order.getStatus()
        );
    }
}
