package com.example.demo.model;

import lombok.*;
import lombok.experimental.FieldDefaults;

//Trịnh Trung Hào - 22110316


@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@FieldDefaults(level = AccessLevel.PRIVATE)
public class CategoryRequest {
    String name;
    String description;
    String imageUrl;
}
