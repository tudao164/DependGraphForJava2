package com.example.demo.service;

import com.example.demo.dto.CategoryDTO;
import com.example.demo.entity.Category;
import java.util.List;

public interface CategoryService {
    List<Category> getAllCategories();
    List<Category> getRootCategories();
    List<Category> getSubcategories(Long parentId);
    Category getCategoryById(Long id);
    Category getCategoryByName(String name);
    Category createCategory(CategoryDTO categoryDTO);
    Category updateCategory(Long id, CategoryDTO categoryDTO);
    void deleteCategory(Long id);
}
