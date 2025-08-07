package com.example.demo.model;


import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.*;
import lombok.experimental.FieldDefaults;

//Đào Thanh Tú - 22110452
//Trịnh Trung Hào - 22110316


@JsonInclude(JsonInclude.Include.NON_NULL)
@Data
@Builder
@FieldDefaults(level = AccessLevel.PRIVATE)
@AllArgsConstructor
@NoArgsConstructor
public class ApiResponse<T> {

    int code;
    String message;
    T result;
}
