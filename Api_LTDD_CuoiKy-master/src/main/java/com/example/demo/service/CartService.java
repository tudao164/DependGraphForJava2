package com.example.demo.service;

import com.example.demo.dto.CartDTO;
import com.example.demo.dto.CartItemDTO;

public interface CartService {
    CartDTO getCartByUserId(String userId);
    CartDTO addItemToCart(String userId, CartItemDTO cartItemDTO);
    CartDTO updateCartItem(String userId, CartItemDTO cartItemDTO);
    CartDTO removeItemFromCart(String userId, Long productId);
    void clearCart(String userId);
}