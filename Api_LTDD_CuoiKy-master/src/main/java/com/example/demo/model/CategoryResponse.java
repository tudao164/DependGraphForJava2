package com.example.demo.model;

import lombok.*;
import lombok.experimental.FieldDefaults;

//Đào Thanh Tú - 22110452
//Trịnh Trung Hào - 22110316


@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@FieldDefaults(level = AccessLevel.PRIVATE)
public class CategoryResponse {
    String id;
    String name;
    String description;
    String imageUrl;
}
