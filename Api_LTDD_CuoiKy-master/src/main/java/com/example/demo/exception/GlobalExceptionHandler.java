package com.example.demo.exception;


import com.example.demo.model.ApiResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import com.example.demo.dto.ResponseDTO;
import org.springframework.web.bind.annotation.ResponseStatus;

import java.nio.file.AccessDeniedException;

//Đào Thanh Tú - 22110452
//Trịnh Trung Hào - 22110316


@ControllerAdvice
public class GlobalExceptionHandler {

    // Lỗi này dùng khi không có một message nào xảy ra khi có lỗi
    @ExceptionHandler(value = Exception.class)
    ResponseEntity<ApiResponse<String>> exceptionHandler(Exception e) {
        ApiResponse<String> apiResponse = new ApiResponse<>();
        apiResponse.setCode(ErrorCode.UNCATEGORIZED.getCode());
        apiResponse.setMessage(ErrorCode.UNCATEGORIZED.getMessage());
        return ResponseEntity.badRequest().body(apiResponse);
    }

    @ExceptionHandler(value = AppException.class)
    ResponseEntity<ApiResponse<String>> appExceptionHandler(AppException e) {
        ApiResponse<String> apiResponse = new ApiResponse<>();
        apiResponse.setCode(e.getErrorCode().getCode());
        apiResponse.setMessage(e.getErrorCode().getMessage());
        return ResponseEntity
                .status(e.getErrorCode().getHttpStatusCode())   // Set HttpStatusCode
                .body(apiResponse);
    }

    // Exception xử lý quyền không đủ quyền để truy cập vào một endpoint (AccessDenied)
    @ExceptionHandler(value = AccessDeniedException.class)
    ResponseEntity<ApiResponse> accessDeniedExceptionHandler(AccessDeniedException e) {
        ErrorCode errorCode = ErrorCode.UNAUTHORIZED;

        return ResponseEntity.status(errorCode.getHttpStatusCode()).body(
                ApiResponse.builder()
                        .code(errorCode.getCode())
                        .message(errorCode.getMessage())
                        .build()
        );
    }

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ResponseDTO<Object>> handleUserNotFoundException(UserNotFoundException ex) {
        return new ResponseEntity<>(
                ResponseDTO.error(ex.getMessage()),
                HttpStatus.NOT_FOUND
        );
    }


    @ResponseStatus(HttpStatus.NOT_FOUND)
    public class RatingNotFoundException extends RuntimeException {
        public RatingNotFoundException(Long id) {
            super("Rating not found with id: " + id);
        }
    }

    @ResponseStatus(HttpStatus.FORBIDDEN)
    public class UnauthorizedRatingActionException extends RuntimeException {
        public UnauthorizedRatingActionException() {
            super("You are not authorized to modify this rating");
        }
    }

    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public class DuplicateRatingException extends RuntimeException {
        public DuplicateRatingException() {
            super("You have already rated this product. Please update your existing rating.");
        }
    }

    @ExceptionHandler(ReviewNotFoundException.class)
    public ResponseEntity<ResponseDTO<Object>> handleReviewNotFoundException(ReviewNotFoundException ex) {
        return new ResponseEntity<>(
                ResponseDTO.error(ex.getMessage()),
                HttpStatus.NOT_FOUND
        );
    }


}
