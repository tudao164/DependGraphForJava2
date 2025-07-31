package com.example.ecommerce.core.service;

import com.example.ecommerce.core.model.User;
import com.example.ecommerce.core.model.Address;
import com.example.ecommerce.infrastructure.persistence.UserRepository;
import com.example.ecommerce.exception.InvalidInputException;
import com.example.ecommerce.util.StringUtils;

public class UserService {
    private final UserRepository userRepository;
    private final NotificationService notificationService;
    
    public UserService(UserRepository userRepository, NotificationService notificationService) {
        this.userRepository = userRepository;
        this.notificationService = notificationService;
    }
    
    public User createUser(String name, String email) throws InvalidInputException {
        if (StringUtils.isEmpty(name) || StringUtils.isEmpty(email)) {
            throw new InvalidInputException("Name and email are required");
        }
        User user = new User(name, email);
        userRepository.save(user);
        notificationService.sendWelcomeEmail(user);
        return user;
    }
    
    public User getUserById(String id) throws InvalidInputException {
        if (StringUtils.isEmpty(id)) {
            throw new InvalidInputException("User ID is required");
        }
        return userRepository.findById(id);
    }
    
    public void updateUserAddress(String userId, Address address) throws InvalidInputException {
        if (StringUtils.isEmpty(userId) || address == null) {
            throw new InvalidInputException("User ID and address are required");
        }
        User user = userRepository.findById(userId);
        if (user != null) {
            user.setAddress(address);
            userRepository.update(user);
        }
    }
}
