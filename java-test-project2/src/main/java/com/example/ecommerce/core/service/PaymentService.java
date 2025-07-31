package com.example.ecommerce.core.service;

import com.example.ecommerce.core.model.Order;
import com.example.ecommerce.security.PaymentValidator;

public class PaymentService {
    private final PaymentValidator paymentValidator;
    
    public PaymentService(PaymentValidator paymentValidator) {
        this.paymentValidator = paymentValidator;
    }
    
    public boolean processPayment(Order order) {
        if (!paymentValidator.validateOrder(order)) {
            return false;
        }
        System.out.println("Processing payment for order: " + order.getId());
        System.out.println("Amount: $" + order.getTotalAmount());
        return Math.random() > 0.1; // 90% success rate
    }
}
