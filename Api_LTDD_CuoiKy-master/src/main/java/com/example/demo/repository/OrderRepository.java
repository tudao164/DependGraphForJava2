package com.example.demo.repository;

import com.example.demo.entity.Order;
import com.example.demo.entity.UserEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface OrderRepository extends JpaRepository<Order, String> {
    List<Order> findByUserOrderByOrderDateDesc(UserEntity user);
    Page<Order> findByUserOrderByOrderDateDesc(UserEntity user, Pageable pageable);
}