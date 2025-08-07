package com.example.demo.service;


import com.example.demo.entity.UserEntity;
import com.example.demo.repository.IUserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

//Đào Thanh Tú - 22110452
//Trịnh Trung Hào - 22110316


@Service
public class AuthService {

    @Autowired
    private IUserRepository userRepository;

    public int verifyUser(String email, String otp) {
        UserEntity foundUser = userRepository.findByEmail(email);
        if (foundUser == null) {
            return -1; // Không tìm thấy User
        }
        if (!foundUser.getOtp().equals(otp)) {
            return 0; // Otp không đúng
        }

        foundUser.setIsActive(1);
        userRepository.save(foundUser);
        return 1; // Success
    }
}
