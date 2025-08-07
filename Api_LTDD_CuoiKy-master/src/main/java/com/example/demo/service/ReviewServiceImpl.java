package com.example.demo.service;

import com.example.demo.dto.ReviewDTO;
import com.example.demo.entity.Product;
import com.example.demo.entity.Review;
import com.example.demo.entity.UserEntity;
import com.example.demo.exception.ProductNotFoundException;
import com.example.demo.exception.ReviewNotFoundException;
import com.example.demo.exception.UserNotFoundException;
import com.example.demo.repository.ProductRepository;
import com.example.demo.repository.ReviewRepository;
import com.example.demo.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class ReviewServiceImpl implements ReviewService {

    private final ReviewRepository reviewRepository;
    private final ProductRepository productRepository;
    private final UserRepository userRepository;

    @Autowired
    public ReviewServiceImpl(ReviewRepository reviewRepository,
                             ProductRepository productRepository,
                             UserRepository userRepository) {
        this.reviewRepository = reviewRepository;
        this.productRepository = productRepository;
        this.userRepository = userRepository;
    }

    @Override
    public List<Review> getAllReviews() {
        return reviewRepository.findAll();
    }

    @Override
    public Review getReviewById(Long id) {
        return reviewRepository.findById(id)
                .orElseThrow(() -> new ReviewNotFoundException(id));
    }

    @Override
    public List<Review> getReviewsByProductId(Long productId) {
        return reviewRepository.findByProduct_Id(productId);
    }

    @Override
    public List<Review> getReviewsByUserId(String userId) {
        return reviewRepository.findByUser_Id(userId);
    }

    @Override
    @Transactional
    public Review createReview(ReviewDTO reviewDTO) {
        Review review = new Review();
        mapDtoToEntity(reviewDTO, review);
        return reviewRepository.save(review);
    }

    @Override
    @Transactional
    public Review updateReview(Long id, ReviewDTO reviewDTO) {
        Review existingReview = getReviewById(id);

        // Only update content and rating from DTO
        existingReview.setContent(reviewDTO.getContent());
        existingReview.setRating(reviewDTO.getRating());
        existingReview.setUpdatedAt(LocalDateTime.now());

        return reviewRepository.save(existingReview);
    }

    @Override
    @Transactional
    public void deleteReview(Long id) {
        if (!reviewRepository.existsById(id)) {
            throw new ReviewNotFoundException(id);
        }
        reviewRepository.deleteById(id);
    }

    private void mapDtoToEntity(ReviewDTO dto, Review entity) {
        entity.setContent(dto.getContent());
        entity.setRating(dto.getRating());

        // Set product
        Product product = productRepository.findById(dto.getProductId())
                .orElseThrow(() -> new ProductNotFoundException(dto.getProductId()));
        entity.setProduct(product);

        // Set user
        UserEntity user = userRepository.findById(dto.getUserId())
                .orElseThrow(() -> new UserNotFoundException("User not found with ID: " + dto.getUserId()));
        entity.setUser(user);
    }
}
