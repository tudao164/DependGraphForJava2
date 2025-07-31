package com.example.ecommerce.core.service;

import com.example.ecommerce.core.model.Order;
import com.example.ecommerce.core.model.User;
import com.example.ecommerce.core.model.Product;
import com.example.ecommerce.core.model.OrderStatus;
import com.example.ecommerce.infrastructure.persistence.OrderRepository;
import com.example.ecommerce.infrastructure.persistence.UserRepository;
import com.example.ecommerce.infrastructure.persistence.ProductRepository;
import com.example.ecommerce.exception.InvalidOrderException;
import com.example.ecommerce.util.StringUtils;
import java.util.List;
import java.util.stream.Collectors;

public class OrderService {
    private final OrderRepository orderRepository;
    private final UserRepository userRepository;
    private final ProductRepository productRepository;
    private final NotificationService notificationService;
    private final PaymentService paymentService;
    
    public OrderService(OrderRepository orderRepository, UserRepository userRepository,
                       ProductRepository productRepository, NotificationService notificationService,
                       PaymentService paymentService) {
        this.orderRepository = orderRepository;
        this.userRepository = userRepository;
        this.productRepository = productRepository;
        this.notificationService = notificationService;
        this.paymentService = paymentService;
    }
    
    public Order createOrder(String userId, List<String> productIds) throws InvalidOrderException {
        if (StringUtils.isEmpty(userId) || productIds == null || productIds.isEmpty()) {
            throw new InvalidOrderException("User ID and product IDs are required");
        }
        
        User user = userRepository.findById(userId);
        if (user == null) {
            throw new InvalidOrderException("User not found");
        }
        
        List<Product> products = productIds.stream()
                .map(productRepository::findById)
                .filter(product -> product != null)
                .collect(Collectors.toList());
        
        if (products.isEmpty()) {
            throw new InvalidOrderException("No valid products found");
        }
        
        Order order = new Order(user, products);
        orderRepository.save(order);
        user.addOrder(order);
        userRepository.update(user);
        notificationService.sendOrderConfirmation(order);
        
        return order;
    }
    
    public void processPayment(String orderId) throws InvalidOrderException {
        Order order = orderRepository.findById(orderId);
        if (order == null) {
            throw new InvalidOrderException("Order not found");
        }
        
        boolean paymentSuccess = paymentService.processPayment(order);
        if (paymentSuccess) {
            order.setStatus(OrderStatus.CONFIRMED);
            orderRepository.update(order);
            notificationService.sendPaymentConfirmation(order);
        }
    }
}
