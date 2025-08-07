package com.example.demo.model;


import lombok.*;
import lombok.experimental.FieldDefaults;

//Đào Thanh Tú - 22110452
//Trịnh Trung Hào - 22110316


@Data
@NoArgsConstructor
@AllArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE)
@Builder
public class VerifyRequest {
    String email;
    String otp;
}
