package com.example.demo.controller;

import com.example.demo.dto.CategoryDTO;
import com.example.demo.dto.ResponseDTO;
import com.example.demo.entity.Category;
import com.example.demo.service.CategoryService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/categories")
public class CategoryController {

    private final CategoryService categoryService;

    @Autowired
    public CategoryController(CategoryService categoryService) {
        this.categoryService = categoryService;
    }

    @GetMapping
    public ResponseEntity<ResponseDTO<List<Category>>> getAllCategories() {
        List<Category> categories = categoryService.getAllCategories();
        return ResponseEntity.ok(ResponseDTO.success("Categories fetched successfully", categories));
    }

    @GetMapping("/root")
    public ResponseEntity<ResponseDTO<List<Category>>> getRootCategories() {
        List<Category> categories = categoryService.getRootCategories();
        return ResponseEntity.ok(ResponseDTO.success("Root categories fetched successfully", categories));
    }

    @GetMapping("/{id}/subcategories")
    public ResponseEntity<ResponseDTO<List<Category>>> getSubcategories(@PathVariable Long id) {
        List<Category> subcategories = categoryService.getSubcategories(id);
        return ResponseEntity.ok(ResponseDTO.success("Subcategories fetched successfully", subcategories));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ResponseDTO<Category>> getCategoryById(@PathVariable Long id) {
        Category category = categoryService.getCategoryById(id);
        return ResponseEntity.ok(ResponseDTO.success("Category fetched successfully", category));
    }

    @GetMapping("/name/{name}")
    public ResponseEntity<ResponseDTO<Category>> getCategoryByName(@PathVariable String name) {
        Category category = categoryService.getCategoryByName(name);
        return ResponseEntity.ok(ResponseDTO.success("Category fetched successfully", category));
    }

    @PostMapping
    public ResponseEntity<ResponseDTO<Category>> createCategory(@Valid @RequestBody CategoryDTO categoryDTO) {
        Category createdCategory = categoryService.createCategory(categoryDTO);
        return new ResponseEntity<>(
                ResponseDTO.success("Category created successfully", createdCategory),
                HttpStatus.CREATED
        );
    }

    @PutMapping("/{id}")
    public ResponseEntity<ResponseDTO<Category>> updateCategory(
            @PathVariable Long id,
            @Valid @RequestBody CategoryDTO categoryDTO) {
        Category updatedCategory = categoryService.updateCategory(id, categoryDTO);
        return ResponseEntity.ok(ResponseDTO.success("Category updated successfully", updatedCategory));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ResponseDTO<Void>> deleteCategory(@PathVariable Long id) {
        categoryService.deleteCategory(id);
        return ResponseEntity.ok(ResponseDTO.success("Category deleted successfully", null));
    }
}