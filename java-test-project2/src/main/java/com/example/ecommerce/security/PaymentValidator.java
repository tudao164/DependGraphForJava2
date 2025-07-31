package com.example.ecommerce.security;

import com.example.ecommerce.core.model.Order;
import com.example.ecommerce.util.StringUtils;

public class PaymentValidator {
    
    public boolean validateOrder(Order order) {
        if (order == null || order.getUser() == null || order.getProducts() == null) {
            return false;
        }
        if (StringUtils.isEmpty(order.getId()) || order.getTotalAmount() <= 0) {
            return false;
        }
        return order.getProducts().stream().allMatch(p -> p.getPrice() > 0);
    }
}
