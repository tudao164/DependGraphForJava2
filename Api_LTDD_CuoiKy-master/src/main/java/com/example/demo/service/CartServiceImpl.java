package com.example.demo.service;

import com.example.demo.dto.CartDTO;
import com.example.demo.dto.CartItemDTO;
import com.example.demo.dto.CartItemResponseDTO;
import com.example.demo.entity.Cart;
import com.example.demo.entity.CartItem;
import com.example.demo.entity.Product;
import com.example.demo.entity.UserEntity;
import com.example.demo.exception.ProductNotFoundException;
import com.example.demo.exception.UserNotFoundException;
import com.example.demo.repository.CartItemRepository;
import com.example.demo.repository.CartRepository;
import com.example.demo.repository.ProductRepository;
import com.example.demo.repository.IUserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class CartServiceImpl implements CartService {

    private final CartRepository cartRepository;
    private final CartItemRepository cartItemRepository;
    private final IUserRepository userRepository;
    private final ProductRepository productRepository;

    @Autowired
    public CartServiceImpl(
            CartRepository cartRepository,
            CartItemRepository cartItemRepository,
            IUserRepository userRepository,
            ProductRepository productRepository) {
        this.cartRepository = cartRepository;
        this.cartItemRepository = cartItemRepository;
        this.userRepository = userRepository;
        this.productRepository = productRepository;
    }

    @Override
    public CartDTO getCartByUserId(String userId) {
        UserEntity user = userRepository.findById(userId)
                .orElseThrow(() -> new UserNotFoundException("User not found with id: " + userId));

        Cart cart = cartRepository.findByUser(user)
                .orElseGet(() -> {
                    Cart newCart = new Cart();
                    newCart.setUser(user);
                    return cartRepository.save(newCart);
                });

        return convertToCartDTO(cart);
    }

    @Override
    @Transactional
    public CartDTO addItemToCart(String userId, CartItemDTO cartItemDTO) {
        UserEntity user = userRepository.findById(userId)
                .orElseThrow(() -> new UserNotFoundException("User not found with id: " + userId));

        Product product = productRepository.findById(cartItemDTO.getProductId())
                .orElseThrow(() -> new ProductNotFoundException(cartItemDTO.getProductId()));

        Cart cart = cartRepository.findByUser(user)
                .orElseGet(() -> {
                    Cart newCart = new Cart();
                    newCart.setUser(user);
                    return cartRepository.save(newCart);
                });

        Optional<CartItem> existingCartItem = cartItemRepository.findByCartAndProduct(cart, product);

        if (existingCartItem.isPresent()) {
            CartItem cartItem = existingCartItem.get();
            cartItem.setQuantity(cartItem.getQuantity() + cartItemDTO.getQuantity());
            cartItemRepository.save(cartItem);
        } else {
            CartItem newCartItem = new CartItem();
            newCartItem.setCart(cart);
            newCartItem.setProduct(product);
            newCartItem.setQuantity(cartItemDTO.getQuantity());
            cart.getCartItems().add(newCartItem);
            cartItemRepository.save(newCartItem);
        }

        return convertToCartDTO(cart);
    }

    @Override
    @Transactional
    public CartDTO updateCartItem(String userId, CartItemDTO cartItemDTO) {
        UserEntity user = userRepository.findById(userId)
                .orElseThrow(() -> new UserNotFoundException("User not found with id: " + userId));

        Product product = productRepository.findById(cartItemDTO.getProductId())
                .orElseThrow(() -> new ProductNotFoundException(cartItemDTO.getProductId()));

        Cart cart = cartRepository.findByUser(user)
                .orElseThrow(() -> new RuntimeException("Cart not found for user with id: " + userId));

        CartItem cartItem = cartItemRepository.findByCartAndProduct(cart, product)
                .orElseThrow(() -> new RuntimeException("Cart item not found for product with id: " + cartItemDTO.getProductId()));

        cartItem.setQuantity(cartItemDTO.getQuantity());
        cartItemRepository.save(cartItem);

        return convertToCartDTO(cart);
    }

    @Override
    @Transactional
    public CartDTO removeItemFromCart(String userId, Long productId) {
        UserEntity user = userRepository.findById(userId)
                .orElseThrow(() -> new UserNotFoundException("User not found with id: " + userId));

        Product product = productRepository.findById(productId)
                .orElseThrow(() -> new ProductNotFoundException(productId));

        Cart cart = cartRepository.findByUser(user)
                .orElseThrow(() -> new RuntimeException("Cart not found for user with id: " + userId));

        Optional<CartItem> cartItemOptional = cartItemRepository.findByCartAndProduct(cart, product);

        if (cartItemOptional.isPresent()) {
            CartItem cartItem = cartItemOptional.get();
            cart.getCartItems().remove(cartItem);
            cartItemRepository.delete(cartItem);
        }

        return convertToCartDTO(cart);
    }

    @Override
    @Transactional
    public void clearCart(String userId) {
        UserEntity user = userRepository.findById(userId)
                .orElseThrow(() -> new UserNotFoundException("User not found with id: " + userId));

        Cart cart = cartRepository.findByUser(user)
                .orElseThrow(() -> new RuntimeException("Cart not found for user with id: " + userId));

        cart.getCartItems().clear();
        cartRepository.save(cart);
    }

    private CartDTO convertToCartDTO(Cart cart) {
        List<CartItemResponseDTO> cartItemDTOs = cart.getCartItems().stream()
                .map(this::convertToCartItemResponseDTO)
                .collect(Collectors.toList());

        double totalPrice = cartItemDTOs.stream()
                .mapToDouble(item -> item.getSubtotal().doubleValue())
                .sum();

        CartDTO cartDTO = new CartDTO();
        cartDTO.setId(cart.getId());
        cartDTO.setUserId(cart.getUser().getId()); // Đã sửa để sử dụng String userId
        cartDTO.setItems(cartItemDTOs);
        cartDTO.setTotalPrice(totalPrice);

        return cartDTO;
    }

    private CartItemResponseDTO convertToCartItemResponseDTO(CartItem cartItem) {
        Product product = cartItem.getProduct();
        BigDecimal subtotal = product.getPrice().multiply(BigDecimal.valueOf(cartItem.getQuantity()));

        CartItemResponseDTO dto = new CartItemResponseDTO();
        dto.setId(cartItem.getId());
        dto.setProductId(product.getId());
        dto.setProductName(product.getName());
        dto.setProductImageUrl(product.getImageUrl());
        dto.setProductPrice(product.getPrice());
        dto.setQuantity(cartItem.getQuantity());
        dto.setSubtotal(subtotal);

        return dto;
    }
}