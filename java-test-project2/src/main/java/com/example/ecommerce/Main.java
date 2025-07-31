package com.example.ecommerce;

import com.example.ecommerce.api.controller.UserController;
import com.example.ecommerce.api.controller.OrderController;
import com.example.ecommerce.core.service.UserService;
import com.example.ecommerce.core.service.OrderService;
import com.example.ecommerce.infrastructure.config.AppConfig;

public class Main {
    public static void main(String[] args) {
        // Initialize configuration
        AppConfig appConfig = new AppConfig();
        
        // Create services
        UserService userService = appConfig.getUserService();
        OrderService orderService = appConfig.getOrderService();
        
        // Create controllers
        UserController userController = new UserController(userService);
        OrderController orderController = new OrderController(orderService);
        
        System.out.println("E-commerce application started");
        
        // Simulate API calls
        userController.createUser("John Doe", "john@example.com");
        orderController.createOrder("user123", "product456");
    }
}
