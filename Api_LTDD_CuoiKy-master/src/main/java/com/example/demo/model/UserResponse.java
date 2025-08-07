package com.example.demo.model;

import lombok.*;
import lombok.experimental.FieldDefaults;

//Đào Thanh Tú - 22110452

@Data
@NoArgsConstructor
@AllArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE)
@Builder
public class UserResponse {
    String id; // Thêm trường id
    String password;
    String fullName;
    String email;
    Integer isActive;
    String picture;
    boolean gender;
}