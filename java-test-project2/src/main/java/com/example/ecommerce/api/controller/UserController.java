package com.example.ecommerce.api.controller;

import com.example.ecommerce.api.dto.UserDTO;
import com.example.ecommerce.core.model.User;
import com.example.ecommerce.core.service.UserService;
import com.example.ecommerce.exception.InvalidInputException;
import com.example.ecommerce.util.StringUtils;

public class UserController {
    private final UserService userService;
    
    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    public UserDTO createUser(String name, String email) throws InvalidInputException {
        if (StringUtils.isEmpty(name) || StringUtils.isEmpty(email)) {
            throw new InvalidInputException("Name and email are required");
        }
        User user = userService.createUser(name, email);
        return convertToDTO(user);
    }
    
    public UserDTO getUser(String userId) throws InvalidInputException {
        if (StringUtils.isEmpty(userId)) {
            throw new InvalidInputException("User ID is required");
        }
        User user = userService.getUserById(userId);
        return convertToDTO(user);
    }
    
    private UserDTO convertToDTO(User user) {
        return new UserDTO(
            user.getId(),
            user.getName(),
            user.getEmail(),
            user.getAddress(),
            user.getRole()
        );
    }
}
