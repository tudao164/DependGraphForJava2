package com.example.ecommerce.infrastructure.config;

import com.example.ecommerce.core.service.UserService;
import com.example.ecommerce.core.service.OrderService;
import com.example.ecommerce.core.service.NotificationService;
import com.example.ecommerce.core.service.PaymentService;
import com.example.ecommerce.infrastructure.persistence.UserRepository;
import com.example.ecommerce.infrastructure.persistence.OrderRepository;
import com.example.ecommerce.infrastructure.persistence.ProductRepository;
import com.example.ecommerce.security.PaymentValidator;

public class AppConfig {
    private final DatabaseConfig databaseConfig;
    private final UserRepository userRepository;
    private final OrderRepository orderRepository;
    private final ProductRepository productRepository;
    private final NotificationService notificationService;
    private final PaymentService paymentService;
    private final UserService userService;
    private final OrderService orderService;
    
    public AppConfig() {
        this.databaseConfig = new DatabaseConfig();
        this.userRepository = new UserRepository(databaseConfig);
        this.orderRepository = new OrderRepository(databaseConfig);
        this.productRepository = new ProductRepository(databaseConfig);
        this.notificationService = new NotificationService();
        this.paymentService = new PaymentService(new PaymentValidator());
        this.userService = new UserService(userRepository, notificationService);
        this.orderService = new OrderService(
            orderRepository,
            userRepository,
            productRepository,
            notificationService,
            paymentService
        );
    }
    
    public UserService getUserService() {
        return userService;
    }
    
    public OrderService getOrderService() {
        return orderService;
    }
}
