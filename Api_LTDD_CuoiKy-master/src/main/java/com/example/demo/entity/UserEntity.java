package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.FieldDefaults;

// Đào Thanh Tú - 22110452

@Entity(name = "tbl_user")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE)
public class UserEntity extends AbstractEntity {

    @Column(name = "password")
    String password;

    @Column(name = "full_name")
    String fullName;

    @Column(name = "email")
    String email;

    @Column(name = "otp")
    String otp;

    @Column(name = "is_active")
    Integer isActive;

    @Column(name = "picture")
    String picture;
}
