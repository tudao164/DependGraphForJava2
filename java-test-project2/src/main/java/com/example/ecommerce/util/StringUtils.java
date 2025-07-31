package com.example.ecommerce.util;

public class StringUtils {
    
    public static boolean isEmpty(String str) {
        return str == null || str.trim().isEmpty();
    }
    
    public static String sanitize(String str) {
        if (isEmpty(str)) {
            return "";
        }
        return str.trim().replaceAll("[^a-zA-Z0-9\\s@._-]", "");
    }
    
    public static String capitalize(String str) {
        if (isEmpty(str)) {
            return str;
        }
        return str.substring(0, 1).toUpperCase() + str.substring(1).toLowerCase();
    }
}
