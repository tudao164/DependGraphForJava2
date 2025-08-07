package com.example.demo.service;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

//Đào Thanh Tú - 22110452
//Trịnh Trung Hào - 22110316


@Service
public class EmailService {

    @Autowired
    private JavaMailSender mailSender;

    private final String sender = "Test";

    @Async
    public void sendSimpleMail(String to, String subject, String content) {
        try {
            SimpleMailMessage mailMessage = new SimpleMailMessage();

            mailMessage.setFrom(sender);
            mailMessage.setTo(to);
            mailMessage.setSubject(subject);
            mailMessage.setText(content);

            mailSender.send(mailMessage);
        } catch (Exception e) {
            e.getMessage();
        }
    }
}
