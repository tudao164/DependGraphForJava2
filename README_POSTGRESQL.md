# PostgreSQL Database Setup

## Cấu hình Database

### 1. Tạo Database và Table

```sql
-- Kết nối vào PostgreSQL và tạo database
CREATE DATABASE graph;

-- Chuyển sang database graph
\c graph;

-- Tạo table html_function
CREATE TABLE public.html_function (
    function_id VARCHAR(255) PRIMARY KEY,
    function_name VARCHAR(255) NOT NULL
);

-- Thêm sample data (optional)
INSERT INTO public.html_function (function_id, function_name) VALUES
('login_form', 'loginForm()'),
('user_list', 'displayUsers()'),
('order_submit', 'submitOrder()'),
('product_search', 'searchProducts()'),
('payment_process', 'processPayment()'),
('user_register', 'registerUser()'),
('order_list', 'displayOrders()'),
('product_detail', 'showProductDetail()'),
('cart_add', 'addToCart()'),
('checkout_process', 'processCheckout()');
```

### 2. Cấu hình Connection

#### Option 1: Environment Variables (Recommended)
```powershell
# Windows PowerShell
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"
$env:DB_NAME = "graph"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "your_actual_password"
$env:DB_SCHEMA = "public"
```

#### Option 2: Sửa db_config.py
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'graph',
    'user': 'postgres',
    'password': 'your_actual_password',  # ⚠️ Sửa password này
    'schema': 'public'
}
```

### 3. Test Connection

```bash
# Test database config
python db_config.py

# Test HTML function database
python html_db.py
```

### 4. Chạy Application

```bash
# Chạy function selector với PostgreSQL integration
python main.py
```

## Troubleshooting

### Lỗi Connection
- Kiểm tra PostgreSQL service đang chạy
- Kiểm tra username/password đúng chưa
- Kiểm tra database 'graph' đã tạo chưa
- Kiểm tra port 5432 có bị block không

### Lỗi Table
- Chạy SQL script tạo table ở trên
- Kiểm tra schema 'public' có đúng không

### Lỗi Permission
- Đảm bảo user PostgreSQL có quyền đọc database 'graph'
- Grant permissions nếu cần:
  ```sql
  GRANT ALL PRIVILEGES ON DATABASE graph TO postgres;
  GRANT ALL PRIVILEGES ON TABLE public.html_function TO postgres;
  ```

## Usage trong Application

Sau khi cấu hình xong:

1. **Function Selector**: HTML functions sẽ được load từ PostgreSQL và hiển thị cùng với Java functions
2. **Graph Generation**: Chọn HTML functions sẽ tạo dependency graph với Java controllers tương ứng
3. **HTML→Java Mapping**: Convention-based mapping từ HTML function tên đến Java controllers

Example:
- `login_form` → `UserController`
- `order_submit` → `OrderController`  
- `product_search` → `ProductController`
