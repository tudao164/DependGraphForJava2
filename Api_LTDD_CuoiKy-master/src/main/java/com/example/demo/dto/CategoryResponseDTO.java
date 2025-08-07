package com.example.demo.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CategoryResponseDTO {
    private Long id;
    private String name;
    private String description;
    private String imageUrl;
    private Long parentId;
    private String parentName;
    private List<CategorySimpleDTO> children = new ArrayList<>();
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}

