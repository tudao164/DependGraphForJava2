package com.example.demo.exception;

// Nguyễn Công Quý - 22110403

import lombok.AccessLevel;
import lombok.Getter;
import lombok.experimental.FieldDefaults;
import org.springframework.http.HttpStatus;
import org.springframework.http.HttpStatusCode;

@Getter
@FieldDefaults(level = AccessLevel.PRIVATE, makeFinal = true)
public enum ErrorCode {
    UNCATEGORIZED(9999, "Uncategorized", HttpStatus.INTERNAL_SERVER_ERROR),

    USER_NOT_EXISTED(1000, "User is not exists", HttpStatus.NOT_FOUND),
    USER_EXISTED(1000, "User already exists", HttpStatus.BAD_REQUEST),

    EMAIL_EXISTED(1000, "Email already exists", HttpStatus.BAD_REQUEST),
    INVALID_OTP_OR_EXPIRED(1003, "OTP code is invalid or expired", HttpStatus.BAD_REQUEST),

    USERNAME_INVALID(1001, "This field must be least 3 characters", HttpStatus.BAD_REQUEST),
    PASSWORD_INVALID(1002, "Password must be at least 8 characters", HttpStatus.BAD_REQUEST),

    UNAUTHENTICATED(1003, "Unauthenticated", HttpStatus.UNAUTHORIZED),
    UNAUTHORIZED(1004, "You do not have permission", HttpStatus.FORBIDDEN),

    USER_ALREADY_ACTIVE(1005, "User already active account", HttpStatus.BAD_REQUEST),
    INVALID_EXPIRED_TOKEN(1005, "Token is invalid.", HttpStatus.BAD_REQUEST),
    REVIEW_NOT_FOUND(404, "Review not found",HttpStatus.BAD_REQUEST),
    REVIEW_ALREADY_EXISTS(409, "User has already reviewed this product",HttpStatus.BAD_REQUEST),
    PRODUCT_NOT_FOUND(404, "Product not found",HttpStatus.BAD_REQUEST),
    VALIDATION_ERROR(400, "Validation error",HttpStatus.BAD_REQUEST);

    ;

    ErrorCode(int code, String message, HttpStatusCode httpStatusCode) {
        this.code = code;
        this.message = message;
        this.httpStatusCode = httpStatusCode;
    }

    int code;
    String message;
    HttpStatusCode httpStatusCode;
}
