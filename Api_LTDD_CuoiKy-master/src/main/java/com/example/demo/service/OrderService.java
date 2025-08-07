package com.example.demo.service;

import com.example.demo.dto.CheckoutRequestDTO;
import com.example.demo.dto.OrderDTO;
import com.example.demo.dto.OrderStatusUpdateDTO;
import com.example.demo.entity.Order;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.List;

public interface OrderService {
    /**
     * Process checkout from cart to create a new order
     */
    OrderDTO checkout(String userId, CheckoutRequestDTO checkoutRequest);

    /**
     * Get a specific order by ID
     */
    OrderDTO getOrderById(String orderId);

    /**
     * Get all orders for a user
     */
    List<OrderDTO> getOrdersByUserId(String userId);

    /**
     * Get paginated orders for a user
     */
    Page<OrderDTO> getOrdersByUserId(String userId, Pageable pageable);

    /**
     * Update order status
     */
    OrderDTO updateOrderStatus(String orderId, OrderStatusUpdateDTO statusUpdateDTO);

    /**
     * Cancel an order
     */
    OrderDTO cancelOrder(String orderId);

    /**
     * Convert OrderStatus to Vietnamese display text
     */
    String getStatusDisplayText(Order.OrderStatus status);
}