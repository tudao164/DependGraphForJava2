package com.example.ecommerce.core.service;

import com.example.ecommerce.core.model.User;
import com.example.ecommerce.core.model.Order;
import com.example.ecommerce.util.StringUtils;

public class NotificationService {
    
    public void sendWelcomeEmail(User user) {
        if (user != null && !StringUtils.isEmpty(user.getEmail())) {
            System.out.println("Sending welcome email to: " + user.getEmail());
        }
    }
    
    public void sendOrderConfirmation(Order order) {
        if (order != null && order.getUser() != null) {
            System.out.println("Sending order confirmation to: " + order.getUser().getEmail());
        }
    }
    
    public void sendPaymentConfirmation(Order order) {
        if (order != null && order.getUser() != null) {
            System.out.println("Sending payment confirmation to: " + order.getUser().getEmail());
        }
    }
}
