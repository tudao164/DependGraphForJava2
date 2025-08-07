package com.example.demo.controller;

import com.example.demo.dto.CartDTO;
import com.example.demo.dto.CartItemDTO;
import com.example.demo.dto.ResponseDTO;
import com.example.demo.service.CartService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/carts")
public class CartController {

    private final CartService cartService;

    @Autowired
    public CartController(CartService cartService) {
        this.cartService = cartService;
    }

    @GetMapping("/{userId}")
    public ResponseEntity<ResponseDTO<CartDTO>> getCartByUserId(@PathVariable String userId) {
        CartDTO cart = cartService.getCartByUserId(userId);
        return ResponseEntity.ok(ResponseDTO.success("Cart fetched successfully", cart));
    }

    @PostMapping("/{userId}/items")
    public ResponseEntity<ResponseDTO<CartDTO>> addItemToCart(
            @PathVariable String userId,
            @Valid @RequestBody CartItemDTO cartItemDTO) {
        CartDTO updatedCart = cartService.addItemToCart(userId, cartItemDTO);
        return new ResponseEntity<>(
                ResponseDTO.success("Item added to cart successfully", updatedCart),
                HttpStatus.CREATED
        );
    }

    @PutMapping("/{userId}/items")
    public ResponseEntity<ResponseDTO<CartDTO>> updateCartItem(
            @PathVariable String userId,
            @Valid @RequestBody CartItemDTO cartItemDTO) {
        CartDTO updatedCart = cartService.updateCartItem(userId, cartItemDTO);
        return ResponseEntity.ok(ResponseDTO.success("Cart item updated successfully", updatedCart));
    }

    @DeleteMapping("/{userId}/items/{productId}")
    public ResponseEntity<ResponseDTO<CartDTO>> removeItemFromCart(
            @PathVariable String userId,
            @PathVariable Long productId) {
        CartDTO updatedCart = cartService.removeItemFromCart(userId, productId);
        return ResponseEntity.ok(ResponseDTO.success("Item removed from cart successfully", updatedCart));
    }

    @DeleteMapping("/{userId}")
    public ResponseEntity<ResponseDTO<Void>> clearCart(@PathVariable String userId) {
        cartService.clearCart(userId);
        return ResponseEntity.ok(ResponseDTO.success("Cart cleared successfully", null));
    }
}