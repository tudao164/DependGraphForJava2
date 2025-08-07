package com.example.demo.controller;

import com.example.demo.dto.CheckoutRequestDTO;
import com.example.demo.dto.OrderDTO;
import com.example.demo.dto.OrderStatusUpdateDTO;
import com.example.demo.dto.ResponseDTO;
import com.example.demo.service.OrderService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService orderService;

    @Autowired
    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @PostMapping("/checkout/{userId}")
    public ResponseEntity<ResponseDTO<OrderDTO>> checkout(
            @PathVariable String userId,
            @Valid @RequestBody CheckoutRequestDTO checkoutRequest) {
        OrderDTO order = orderService.checkout(userId, checkoutRequest);
        return new ResponseEntity<>(
                ResponseDTO.success("Order created successfully", order),
                HttpStatus.CREATED
        );
    }

    @GetMapping("/{orderId}")
    public ResponseEntity<ResponseDTO<OrderDTO>> getOrderById(@PathVariable String orderId) {
        OrderDTO order = orderService.getOrderById(orderId);
        return ResponseEntity.ok(ResponseDTO.success("Order fetched successfully", order));
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<ResponseDTO<List<OrderDTO>>> getOrdersByUserId(@PathVariable String userId) {
        List<OrderDTO> orders = orderService.getOrdersByUserId(userId);
        return ResponseEntity.ok(ResponseDTO.success("Orders fetched successfully", orders));
    }

    @GetMapping("/user/{userId}/paged")
    public ResponseEntity<ResponseDTO<Page<OrderDTO>>> getPagedOrdersByUserId(
            @PathVariable String userId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {

        Pageable pageable = PageRequest.of(page, size);
        Page<OrderDTO> orders = orderService.getOrdersByUserId(userId, pageable);

        return ResponseEntity.ok(ResponseDTO.success("Orders fetched successfully", orders));
    }

    @PutMapping("/{orderId}/status")
    public ResponseEntity<ResponseDTO<OrderDTO>> updateOrderStatus(
            @PathVariable String orderId,
            @Valid @RequestBody OrderStatusUpdateDTO statusUpdateDTO) {

        OrderDTO updatedOrder = orderService.updateOrderStatus(orderId, statusUpdateDTO);
        return ResponseEntity.ok(ResponseDTO.success("Order status updated successfully", updatedOrder));
    }

    @PutMapping("/{orderId}/cancel")
    public ResponseEntity<ResponseDTO<OrderDTO>> cancelOrder(@PathVariable String orderId) {
        OrderDTO cancelledOrder = orderService.cancelOrder(orderId);
        return ResponseEntity.ok(ResponseDTO.success("Order cancelled successfully", cancelledOrder));
    }
}