package com.example.demo.service;

import com.example.demo.dto.CategoryDTO;
import com.example.demo.entity.Category;
import com.example.demo.exception.CategoryNotFoundException;
import com.example.demo.exception.DuplicateCategoryException;
import com.example.demo.repository.CategoryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class CategoryServiceImpl implements CategoryService {

    private final CategoryRepository categoryRepository;

    @Autowired
    public CategoryServiceImpl(CategoryRepository categoryRepository) {
        this.categoryRepository = categoryRepository;
    }

    @Override
    public List<Category> getAllCategories() {
        return categoryRepository.findAll();
    }

    @Override
    public List<Category> getRootCategories() {
        return categoryRepository.findByParentIsNull();
    }

    @Override
    public List<Category> getSubcategories(Long parentId) {
        return categoryRepository.findByParentId(parentId);
    }

    @Override
    public Category getCategoryById(Long id) {
        return categoryRepository.findById(id)
                .orElseThrow(() -> new CategoryNotFoundException(id));
    }

    @Override
    public Category getCategoryByName(String name) {
        return categoryRepository.findByName(name)
                .orElseThrow(() -> new CategoryNotFoundException("Category not found with name: " + name));
    }

    @Override
    @Transactional
    public Category createCategory(CategoryDTO categoryDTO) {
        // Kiểm tra category name đã tồn tại chưa
        Optional<Category> existingCategory = categoryRepository.findByName(categoryDTO.getName());
        if (existingCategory.isPresent()) {
            throw new DuplicateCategoryException("Category with name " + categoryDTO.getName() + " already exists");
        }

        Category category = new Category();
        mapDtoToEntity(categoryDTO, category);

        return categoryRepository.save(category);
    }

    @Override
    @Transactional
    public Category updateCategory(Long id, CategoryDTO categoryDTO) {
        Category existingCategory = getCategoryById(id);

        // Kiểm tra nếu thay đổi tên, đảm bảo tên mới chưa được sử dụng
        if (!existingCategory.getName().equals(categoryDTO.getName())) {
            Optional<Category> categoryWithSameName = categoryRepository.findByName(categoryDTO.getName());
            if (categoryWithSameName.isPresent() && !categoryWithSameName.get().getId().equals(id)) {
                throw new DuplicateCategoryException("Category with name " + categoryDTO.getName() + " already exists");
            }
        }

        mapDtoToEntity(categoryDTO, existingCategory);
        existingCategory.setUpdatedAt(LocalDateTime.now());

        return categoryRepository.save(existingCategory);
    }

    @Override
    @Transactional
    public void deleteCategory(Long id) {
        if (!categoryRepository.existsById(id)) {
            throw new CategoryNotFoundException(id);
        }
        categoryRepository.deleteById(id);
    }

    private void mapDtoToEntity(CategoryDTO dto, Category entity) {
        entity.setName(dto.getName());
        entity.setDescription(dto.getDescription());
        entity.setImageUrl(dto.getImageUrl());

        // Xử lý parent category nếu có
        if (dto.getParentId() != null) {
            Category parentCategory = categoryRepository.findById(dto.getParentId())
                    .orElseThrow(() -> new CategoryNotFoundException(dto.getParentId()));
            entity.setParent(parentCategory);
        } else {
            entity.setParent(null);
        }
    }
}