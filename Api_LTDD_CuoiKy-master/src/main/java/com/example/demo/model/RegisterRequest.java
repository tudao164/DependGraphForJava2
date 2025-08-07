package com.example.demo.model;


import lombok.*;
import lombok.experimental.FieldDefaults;

//Đào Thanh Tú - 22110452



@Data
@NoArgsConstructor
@AllArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE)
@Builder
public class RegisterRequest {
    String password;

    String fullName;

    String email;

    String otp;

    Integer isActive;

    Boolean gender;
}
