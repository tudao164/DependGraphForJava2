package com.example.demo.model;
import lombok.*;
import lombok.experimental.FieldDefaults;

//BỎ KHÔNG DÙNG
@Data
@NoArgsConstructor
@AllArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE)
@Builder
public class PasswordResetCompleteRequest {
    String email;
    String otp;
    String newPassword;
}
