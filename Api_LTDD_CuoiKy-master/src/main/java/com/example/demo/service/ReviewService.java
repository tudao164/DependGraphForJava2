package com.example.demo.service;

import com.example.demo.dto.ReviewDTO;
import com.example.demo.entity.Review;

import java.util.List;

public interface ReviewService {
    List<Review> getAllReviews();
    Review getReviewById(Long id);
    List<Review> getReviewsByProductId(Long productId);
    List<Review> getReviewsByUserId(String userId);
    Review createReview(ReviewDTO reviewDTO);
    Review updateReview(Long id, ReviewDTO reviewDTO);
    void deleteReview(Long id);
}
