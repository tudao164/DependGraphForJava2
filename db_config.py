#!/usr/bin/env python3
"""
PostgreSQL database configuration cho HTML functions
"""

import os

# PostgreSQL connection configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'graph'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '123456'),
    'schema': os.getenv('DB_SCHEMA', 'public')
}

# Hướng dẫn cấu hình
SETUP_INSTRUCTIONS = """
🔧 PostgreSQL Setup Instructions:

1. Đảm bảo PostgreSQL đang chạy
2. Tạo database 'graph' nếu chưa có:
   CREATE DATABASE graph;

3. Tạo table html_function:
   CREATE TABLE public.html_function (
       function_id VARCHAR(255) PRIMARY KEY,
       function_name VARCHAR(255) NOT NULL
   );

4. Thêm sample data (optional):
   INSERT INTO public.html_function (function_id, function_name) VALUES
   ('login_form', 'loginForm()'),
   ('user_list', 'displayUsers()'),
   ('order_submit', 'submitOrder()'),
   ('product_search', 'searchProducts()'),
   ('payment_process', 'processPayment()');

5. Cấu hình connection bằng environment variables:
   set DB_HOST=localhost
   set DB_PORT=5432
   set DB_NAME=graph
   set DB_USER=postgres
   set DB_PASSWORD=your_password
   set DB_SCHEMA=public

   Hoặc sửa trực tiếp trong db_config.py
"""

def print_setup_instructions():
    """In hướng dẫn setup"""
    print(SETUP_INSTRUCTIONS)

def validate_config():
    """Kiểm tra config có đầy đủ không"""
    required_fields = ['host', 'port', 'database', 'user', 'password']
    missing = []
    
    for field in required_fields:
        if not DB_CONFIG[field] or DB_CONFIG[field] == 'your_password_here':
            missing.append(field)
    
    if missing:
        print(f"❌ Missing database configuration: {', '.join(missing)}")
        print_setup_instructions()
        return False
    
    print(f"✅ Database configuration OK: {DB_CONFIG['user']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    return True

if __name__ == "__main__":
    print("🔍 Checking database configuration...")
    validate_config()
