package com.example.demo.service;

import com.example.demo.entity.UserEntity;
import com.example.demo.exception.AppException;
import com.example.demo.exception.ErrorCode;
import com.example.demo.exception.UserNotFoundException;
import com.example.demo.model.*;
import com.example.demo.repository.IUserRepository;
import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;
import java.util.Random;

//Đào Thanh Tú - 22110452

@Slf4j
@Service
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public class UserService {

    IUserRepository userRepository;
    EmailService emailService;
    PasswordEncoder passwordEncoder = new BCryptPasswordEncoder(10);
    Random RANDOM = new Random();

    // Existing methods
    public UserResponse login(LoginRequest request) {
        UserEntity user = userRepository.findByEmail(request.getUsername());
        if (user == null)
            throw new AppException(ErrorCode.USER_NOT_EXISTED);

        boolean authenticated = passwordEncoder.matches(request.getPassword(), user.getPassword())
                && user.getIsActive() == 1;

        if (!authenticated)
            throw new AppException(ErrorCode.UNAUTHENTICATED);

        return UserResponse.builder()
                .id(user.getId()) // Thêm ID vào response
                .isActive((user.getIsActive() == null || user.getIsActive() == 0) ? 0 : 1)
                .fullName(user.getFullName())
                .email(user.getEmail())
                .password(passwordEncoder.encode(user.getPassword()))
                .picture(user.getPicture())
                .build();
    }

    public UserResponse register(RegisterRequest request) {
        if (userRepository.findByEmail(request.getEmail()) != null) {
            log.info("Email existed");
            return null;
        }

        // Build new user for this request
        UserEntity userEntity = UserEntity.builder()
                .fullName(request.getFullName())
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .isActive(0)
                .picture("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1rHMHPZtUE9En7ObJdHD_jaubF4tIQdRGdg&s")
                .build();

        try {
            // Tạo
            String otpCode = generateOtp();
            userEntity.setOtp(otpCode);
            var newUser = userRepository.save(userEntity);
            String subject = "🔑 Activate Your Account at MyApp!";
            String body = "Hello " + newUser.getFullName() + ",\n\n"
                    + "Thank you for signing up at MyApp. To activate your account, please use the following OTP code:\n\n"
                    + "🔒 Your OTP Code: " + otpCode + "\n\n"
                    + "This code is valid for the next 10 minutes. Please do not share this code with anyone.\n\n"
                    + "If you did not request this, please ignore this email.\n\n"
                    + "Best regards,\n";

            // Gửi
            emailService.sendSimpleMail(userEntity.getEmail(), subject, body);
            // Sau khi gửi thì trả về response
            return buildUserResponse(newUser);
        } catch (Exception e) {
            log.error(e.getMessage());
            throw new AppException(ErrorCode.UNCATEGORIZED);
        }
    }

    // New methods
    public UserResponse getUserById(String id) {
        UserEntity user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException("User not found with ID: " + id));
        return buildUserResponse(user);
    }

    public boolean deleteUserById(String id) {
        if (!userRepository.existsById(id)) {
            throw new UserNotFoundException("User not found with ID: " + id);
        }
        userRepository.deleteById(id);
        return true;
    }

    public boolean forgotPassword(String email) {
        UserEntity user = userRepository.findByEmail(email);
        if (user == null) {
            throw new UserNotFoundException("User not found with email: " + email);
        }

        // Generate new OTP
        String otpCode = generateOtp();
        user.setOtp(otpCode);
        userRepository.save(user);

        // Send email with OTP
        String subject = "🔑 Password Reset Request";
        String body = "Hello " + user.getFullName() + ",\n\n"
                + "We received a request to reset your password. Please use the following OTP code:\n\n"
                + "🔒 Your OTP Code: " + otpCode + "\n\n"
                + "This code is valid for the next 10 minutes. Please do not share this code with anyone.\n\n"
                + "If you did not request this, please ignore this email.\n\n"
                + "Best regards,\n";

        emailService.sendSimpleMail(email, subject, body);
        return true;
    }

    public boolean resetPassword(ResetPasswordRequest request) {
        UserEntity user = userRepository.findByEmail(request.getEmail());
        if (user == null) {
            throw new UserNotFoundException("User not found with email: " + request.getEmail());
        }

        // Verify OTP
        if (!user.getOtp().equals(request.getOtp())) {
            return false;
        }

        // Update password
        user.setPassword(passwordEncoder.encode(request.getNewPassword()));
        user.setOtp(null); // Clear OTP after use
        userRepository.save(user);
        return true;
    }

    public UserResponse updateUserInfo(String id, UpdateUserRequest request) {
        UserEntity user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException("User not found with ID: " + id));

        // Update user fields if provided
        if (request.getFullName() != null && !request.getFullName().isEmpty()) {
            user.setFullName(request.getFullName());
        }

        if (request.getPicture() != null && !request.getPicture().isEmpty()) {
            user.setPicture(request.getPicture());
        }

        // Save updated user
        UserEntity updatedUser = userRepository.save(user);
        return buildUserResponse(updatedUser);
    }

    // Helper methods
    private String generateOtp() {
        return String.format("%06d", RANDOM.nextInt(999999));
    }

    private UserResponse buildUserResponse(UserEntity user) {
        return UserResponse.builder()
                .id(user.getId()) // Thêm ID vào response
                .fullName(user.getFullName())
                .email(user.getEmail())
                .password(user.getPassword())
                .isActive((user.getIsActive() == null || user.getIsActive() == 0) ? 0 : 1)
                .picture(user.getPicture())
                .build();
    }

    public String logout() {
        return "Logout successful";
    }
}