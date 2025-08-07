package com.example.demo.controller;

import com.example.demo.dto.ResponseDTO;
import com.example.demo.dto.ReviewDTO;
import com.example.demo.entity.Review;
import com.example.demo.service.ReviewService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/reviews")
public class ReviewController {

    private final ReviewService reviewService;

    @Autowired
    public ReviewController(ReviewService reviewService) {
        this.reviewService = reviewService;
    }

    @GetMapping
    public ResponseEntity<ResponseDTO<List<Review>>> getAllReviews() {
        List<Review> reviews = reviewService.getAllReviews();
        return ResponseEntity.ok(ResponseDTO.success("Reviews fetched successfully", reviews));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ResponseDTO<Review>> getReviewById(@PathVariable Long id) {
        Review review = reviewService.getReviewById(id);
        return ResponseEntity.ok(ResponseDTO.success("Review fetched successfully", review));
    }

    @GetMapping("/product/{productId}")
    public ResponseEntity<ResponseDTO<List<Review>>> getReviewsByProductId(@PathVariable Long productId) {
        List<Review> reviews = reviewService.getReviewsByProductId(productId);
        return ResponseEntity.ok(ResponseDTO.success("Reviews for product fetched successfully", reviews));
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<ResponseDTO<List<Review>>> getReviewsByUserId(@PathVariable String userId) {
        List<Review> reviews = reviewService.getReviewsByUserId(userId);
        return ResponseEntity.ok(ResponseDTO.success("Reviews by user fetched successfully", reviews));
    }

    @PostMapping
    public ResponseEntity<ResponseDTO<Review>> createReview(@Valid @RequestBody ReviewDTO reviewDTO) {
        Review createdReview = reviewService.createReview(reviewDTO);
        return new ResponseEntity<>(
                ResponseDTO.success("Review created successfully", createdReview),
                HttpStatus.CREATED
        );
    }

    @PutMapping("/{id}")
    public ResponseEntity<ResponseDTO<Review>> updateReview(
            @PathVariable Long id,
            @Valid @RequestBody ReviewDTO reviewDTO) {
        Review updatedReview = reviewService.updateReview(id, reviewDTO);
        return ResponseEntity.ok(ResponseDTO.success("Review updated successfully", updatedReview));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ResponseDTO<Void>> deleteReview(@PathVariable Long id) {
        reviewService.deleteReview(id);
        return ResponseEntity.ok(ResponseDTO.success("Review deleted successfully", null));
    }
}