package com.example.demo.service;

import com.example.demo.dto.*;
import com.example.demo.entity.*;
import com.example.demo.exception.OrderNotFoundException;
import com.example.demo.exception.UserNotFoundException;
import com.example.demo.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class OrderServiceImpl implements OrderService {

    private final OrderRepository orderRepository;
    private final OrderItemRepository orderItemRepository;
    private final CartRepository cartRepository;
    private final CartItemRepository cartItemRepository;
    private final IUserRepository userRepository;
    private final ProductRepository productRepository;

    @Autowired
    public OrderServiceImpl(
            OrderRepository orderRepository,
            OrderItemRepository orderItemRepository,
            CartRepository cartRepository,
            CartItemRepository cartItemRepository,
            IUserRepository userRepository,
            ProductRepository productRepository) {
        this.orderRepository = orderRepository;
        this.orderItemRepository = orderItemRepository;
        this.cartRepository = cartRepository;
        this.cartItemRepository = cartItemRepository;
        this.userRepository = userRepository;
        this.productRepository = productRepository;
    }

    @Override
    @Transactional
    public OrderDTO checkout(String userId, CheckoutRequestDTO checkoutRequest) {
        // Find user
        UserEntity user = userRepository.findById(userId)
                .orElseThrow(() -> new UserNotFoundException("User not found with id: " + userId));

        // Find user's cart
        Cart cart = cartRepository.findByUser(user)
                .orElseThrow(() -> new RuntimeException("Cart not found for user with id: " + userId));

        // Check if cart is empty
        if (cart.getCartItems() == null || cart.getCartItems().isEmpty()) {
            throw new RuntimeException("Cannot checkout an empty cart");
        }

        // Create a new order
        Order order = new Order();
        order.setUser(user);
        order.setShippingAddress(checkoutRequest.getShippingAddress());
        order.setPhoneNumber(checkoutRequest.getPhoneNumber());

        // Calculate total amount and create order items
        BigDecimal totalAmount = BigDecimal.ZERO;

        for (CartItem cartItem : cart.getCartItems()) {
            Product product = cartItem.getProduct();

            // Create order item
            OrderItem orderItem = new OrderItem();
            orderItem.setOrder(order);
            orderItem.setProduct(product);
            orderItem.setQuantity(cartItem.getQuantity());
            orderItem.setPrice(product.getPrice()); // Store the current price
            BigDecimal subtotal = product.getPrice().multiply(BigDecimal.valueOf(cartItem.getQuantity()));
            orderItem.setSubtotal(subtotal);

            // Add to order items list
            order.getOrderItems().add(orderItem);

            // Add to total amount
            totalAmount = totalAmount.add(subtotal);
        }

        order.setTotalAmount(totalAmount);

        // Save order
        Order savedOrder = orderRepository.save(order);

        // Clear the cart after successful checkout
        cart.getCartItems().clear();
        cartRepository.save(cart);

        // Return OrderDTO
        return convertToOrderDTO(savedOrder);
    }

    @Override
    public OrderDTO getOrderById(String orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException("Order not found with id: " + orderId));

        return convertToOrderDTO(order);
    }

    @Override
    public List<OrderDTO> getOrdersByUserId(String userId) {
        UserEntity user = userRepository.findById(userId)
                .orElseThrow(() -> new UserNotFoundException("User not found with id: " + userId));

        List<Order> orders = orderRepository.findByUserOrderByOrderDateDesc(user);

        return orders.stream()
                .map(this::convertToOrderDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<OrderDTO> getOrdersByUserId(String userId, Pageable pageable) {
        UserEntity user = userRepository.findById(userId)
                .orElseThrow(() -> new UserNotFoundException("User not found with id: " + userId));

        Page<Order> ordersPage = orderRepository.findByUserOrderByOrderDateDesc(user, pageable);

        return ordersPage.map(this::convertToOrderDTO);
    }

    @Override
    @Transactional
    public OrderDTO updateOrderStatus(String orderId, OrderStatusUpdateDTO statusUpdateDTO) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException("Order not found with id: " + orderId));

        order.setStatus(statusUpdateDTO.getStatus());

        if (statusUpdateDTO.getStatus() == Order.OrderStatus.DELIVERED) {
            order.setDeliveryDate(new Date());
        }

        Order updatedOrder = orderRepository.save(order);
        return convertToOrderDTO(updatedOrder);
    }

    @Override
    @Transactional
    public OrderDTO cancelOrder(String orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException("Order not found with id: " + orderId));

        // Only allow cancellation if the order hasn't been shipped yet
        if (order.getStatus() == Order.OrderStatus.SHIPPING ||
                order.getStatus() == Order.OrderStatus.DELIVERED ||
                order.getStatus() == Order.OrderStatus.RECEIVED) {
            throw new RuntimeException("Cannot cancel an order that has been shipped or delivered");
        }

        order.setStatus(Order.OrderStatus.CANCELLED);
        Order updatedOrder = orderRepository.save(order);

        return convertToOrderDTO(updatedOrder);
    }

    @Override
    public String getStatusDisplayText(Order.OrderStatus status) {
        switch (status) {
            case PENDING:
                return "Chờ xử lý";
            case PROCESSING:
                return "Đang xử lý";
            case SHIPPING:
                return "Đang giao hàng";
            case DELIVERED:
                return "Đã giao hàng";
            case RECEIVED:
                return "Đã nhận hàng";
            case CANCELLED:
                return "Đã hủy";
            default:
                return status.name();
        }
    }

    private OrderDTO convertToOrderDTO(Order order) {
        List<OrderItemDTO> orderItemDTOs = order.getOrderItems().stream()
                .map(this::convertToOrderItemDTO)
                .collect(Collectors.toList());

        OrderDTO orderDTO = new OrderDTO();
        orderDTO.setId(order.getId());
        orderDTO.setUserId(order.getUser().getId());
        orderDTO.setItems(orderItemDTOs);
        orderDTO.setTotalAmount(order.getTotalAmount());
        orderDTO.setStatus(order.getStatus());
        orderDTO.setStatusDisplay(getStatusDisplayText(order.getStatus()));
        orderDTO.setShippingAddress(order.getShippingAddress());
        orderDTO.setPhoneNumber(order.getPhoneNumber());
        orderDTO.setOrderDate(order.getOrderDate());
        orderDTO.setDeliveryDate(order.getDeliveryDate());

        return orderDTO;
    }

    private OrderItemDTO convertToOrderItemDTO(OrderItem orderItem) {
        Product product = orderItem.getProduct();

        OrderItemDTO dto = new OrderItemDTO();
        dto.setId(orderItem.getId());
        dto.setProductId(product.getId());
        dto.setProductName(product.getName());
        dto.setProductImageUrl(product.getImageUrl());
        dto.setPrice(orderItem.getPrice());
        dto.setQuantity(orderItem.getQuantity());
        dto.setSubtotal(orderItem.getSubtotal());

        return dto;
    }
}