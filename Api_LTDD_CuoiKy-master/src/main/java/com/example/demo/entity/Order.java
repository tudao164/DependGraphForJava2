package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Entity
@Table(name = "orders")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Order extends AbstractEntity {

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private UserEntity user;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> orderItems = new ArrayList<>();

    @Column(nullable = false)
    private BigDecimal totalAmount;

    @Column(nullable = false)
    @Enumerated(EnumType.STRING)
    private OrderStatus status;

    @Column(nullable = false)
    private String shippingAddress;

    @Column(nullable = false)
    private String phoneNumber;

    @Column(nullable = false)
    private Date orderDate;

    private Date deliveryDate;

    @PrePersist
    protected void onCreate() {
        orderDate = new Date();
        status = OrderStatus.PENDING;
    }

    public enum OrderStatus {
        PENDING,        // Chờ xử lý
        PROCESSING,     // Đang xử lý
        SHIPPING,       // Đang giao hàng
        DELIVERED,      // Đã giao hàng
        RECEIVED,       // Đã nhận hàng
        CANCELLED       // Đã hủy
    }
}