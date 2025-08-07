package com.example.demo.controller;

import com.example.demo.dto.ProductDTO;
import com.example.demo.dto.ResponseDTO;
import com.example.demo.entity.Product;
import com.example.demo.service.ProductService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/products")
public class ProductController {

    private final ProductService productService;

    @Autowired
    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping
    public ResponseEntity<ResponseDTO<List<Product>>> getAllProducts() {
        List<Product> products = productService.getAllProducts();
        return ResponseEntity.ok(ResponseDTO.success("Products fetched successfully", products));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ResponseDTO<Product>> getProductById(@PathVariable Long id) {
        Product product = productService.getProductById(id);
        return ResponseEntity.ok(ResponseDTO.success("Product fetched successfully", product));
    }

    @PostMapping
    public ResponseEntity<ResponseDTO<Product>> createProduct(@Valid @RequestBody ProductDTO productDTO) {
        Product createdProduct = productService.createProduct(productDTO);
        return new ResponseEntity<>(
                ResponseDTO.success("Product created successfully", createdProduct),
                HttpStatus.CREATED
        );
    }

    @PutMapping("/{id}")
    public ResponseEntity<ResponseDTO<Product>> updateProduct(
            @PathVariable Long id,
            @Valid @RequestBody ProductDTO productDTO) {
        Product updatedProduct = productService.updateProduct(id, productDTO);
        return ResponseEntity.ok(ResponseDTO.success("Product updated successfully", updatedProduct));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ResponseDTO<Void>> deleteProduct(@PathVariable Long id) {
        productService.deleteProduct(id);
        return ResponseEntity.ok(ResponseDTO.success("Product deleted successfully", null));
    }

    @GetMapping("/category/{categoryId}")
    public ResponseEntity<ResponseDTO<List<Product>>> getProductsByCategory(@PathVariable Long categoryId) {
        List<Product> products = productService.getProductsByCategory(categoryId);
        return ResponseEntity.ok(ResponseDTO.success("Products fetched successfully", products));
    }

    @GetMapping("/search")
    public ResponseEntity<ResponseDTO<List<Product>>> searchProducts(@RequestParam String name) {
        List<Product> products = productService.searchProductsByName(name);
        return ResponseEntity.ok(ResponseDTO.success("Search results", products));
    }
}