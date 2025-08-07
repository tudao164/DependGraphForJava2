package com.example.demo.model;

import lombok.*;
import lombok.experimental.FieldDefaults;

///BỎ KHÔNG DÙNG

// Request to initiate password reset
@Data
@NoArgsConstructor
@AllArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE)
@Builder
public class PasswordResetInitRequest {
    String email;
}
