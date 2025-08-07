package com.example.demo.controller;

import com.example.demo.entity.UserEntity;
import com.example.demo.model.*;
import com.example.demo.repository.IUserRepository;
import com.example.demo.service.AuthService;
import com.example.demo.service.UserService;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

//Đào Thanh Tú - 22110452

@Slf4j
@RestController
@RequestMapping()
@RequiredArgsConstructor
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class UserController {

    AuthService authService;
    UserService userService;
    IUserRepository userRepository;

    @GetMapping("/demo")
    ApiResponse<String> demo() {
        UserEntity user = UserEntity.builder()
                .email("tudao")
                .password("1234")
                .picture("test")
                .fullName("test")
                .build();
        userRepository.save(
                user
        );
        return ApiResponse.<String>builder()
                .message("")
                .code(200)
                .result(user.getEmail())
                .build();
    }

    @PostMapping("/register")
    ApiResponse<UserResponse> register(@RequestBody RegisterRequest registerRequest) {
        UserResponse user = userService.register(registerRequest);
        String message;
        if(user == null){
            message="Email đã tồn tại";
            return ApiResponse.<UserResponse>builder()
                    .code(200)
                    .result(null)
                    .message(message)
                    .build();
        }else {
            message ="Đăng kí thành công";
            return ApiResponse.<UserResponse>builder()
                    .code(200)
                    .message(message)
                    .result(user)
                    .build();
        }
    }

    @PostMapping("/login")
    ApiResponse<UserResponse> login(@RequestBody LoginRequest loginRequest) {
        return ApiResponse.<UserResponse>builder()
                .message("Đăng nhập thành công")
                .code(200)
                .result(userService.login(loginRequest))
                .build();
    }

    @PostMapping("/verify-user")
    ApiResponse<String> verifyUser(@RequestBody VerifyRequest request) {
        int status = authService.verifyUser(request.getEmail(), request.getOtp());

        if (status == -1) {
            return ApiResponse.<String>builder()
                    .code(404)
                    .message("Email not found")
                    .build();
        } else if (status == 0) {
            return ApiResponse.<String>builder()
                    .code(400)
                    .message("OTP does not match")
                    .build();
        } else {
            return ApiResponse.<String>builder()
                    .code(200)
                    .message("Verification successful")
                    .build();
        }
    }

    // New API endpoints

    @GetMapping("/users/{id}")
    ApiResponse<UserResponse> getUserById(@PathVariable String id) {
        return ApiResponse.<UserResponse>builder()
                .code(200)
                .message("User retrieved successfully")
                .result(userService.getUserById(id))
                .build();
    }

    @DeleteMapping("/users/{id}")
    ApiResponse<Boolean> deleteUser(@PathVariable String id) {
        boolean result = userService.deleteUserById(id);
        return ApiResponse.<Boolean>builder()
                .code(200)
                .message("User deleted successfully")
                .result(result)
                .build();
    }

    @PostMapping("/forgot-password")
    ApiResponse<Boolean> forgotPassword(@RequestBody ForgotPasswordRequest request) {
        boolean result = userService.forgotPassword(request.getEmail());
        return ApiResponse.<Boolean>builder()
                .code(200)
                .message("Password reset email sent successfully")
                .result(result)
                .build();
    }

    @PostMapping("/reset-password")
    ApiResponse<Boolean> resetPassword(@RequestBody ResetPasswordRequest request) {
        boolean result = userService.resetPassword(request);
        if (result) {
            return ApiResponse.<Boolean>builder()
                    .code(200)
                    .message("Password reset successfully")
                    .result(true)
                    .build();
        } else {
            return ApiResponse.<Boolean>builder()
                    .code(400)
                    .message("Invalid OTP")
                    .result(false)
                    .build();
        }
    }

    @PutMapping("/users/{id}")
    ApiResponse<UserResponse> updateUser(@PathVariable String id,
                                         @RequestBody UpdateUserRequest request) {
        return ApiResponse.<UserResponse>builder()
                .code(200)
                .message("User updated successfully")
                .result(userService.updateUserInfo(id, request))
                .build();
    }
}