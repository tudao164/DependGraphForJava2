# HTML Functions → Java Backend Integration Demo

## 🎯 Tính năng hoàn thành

✅ **PostgreSQL Database Integration**
- Database: `graph`, Table: `public.html_function` 
- 20 HTML functions phù hợp với Java project structure
- Password: `123456`

✅ **HTML-Only Selection Mode**
- Chọn chỉ HTML functions từ database
- Tự động map đến Java controllers/services tương ứng
- Auto-add dependencies (Services, DTOs, Models, etc.)

✅ **Smart Mapping Logic**
```
User Login Form → UserController + dependencies
Create New Order → OrderController + dependencies  
Product Search → Product + ProductRepository
Payment Processing → PaymentService
Notification Settings → NotificationService
Address Management → Address + UserService
```

## 🚀 Demo Usage

### 1. Khởi động Server
```bash
python main.py java-test-project2
```

### 2. Truy cập Function Selector  
- URL: http://localhost:8000/function_selector.html
- Hiển thị: 20 HTML functions từ PostgreSQL + 50 Java classes

### 3. HTML-Only Selection
1. **Chỉ chọn HTML functions** (không chọn Java)
2. Click "Generate Graph"
3. Hệ thống tự động:
   - Map HTML → Java components
   - Add dependencies (Services, DTOs, Repositories)
   - Generate dependency graph

### 4. Ví dụ Mapping

**Chọn: "User Login Form"**
```
📱 User Login Form → 🔧 UserController
   ➕ Added dependency: UserDTO
   ➕ Added dependency: StringUtils  
   ➕ Added dependency: UserService
   ➕ Added dependency: User
   ➕ Added dependency: InvalidInputException
```

**Chọn: "Create New Order"**  
```
📱 Create New Order → 🔧 OrderController
   ➕ Added dependency: OrderDTO
   ➕ Added dependency: OrderService
   ➕ Added dependency: Order
   ➕ Added dependency: Product
```

## 📊 Current Status

✅ **Working Features:**
- PostgreSQL connection với 20 HTML functions
- Function selector UI hiển thị HTML + Java functions
- HTML-only selection mode
- Auto Java mapping với dependencies
- Graph generation cho full stack view

✅ **Test Results:**
```bash
python test_html_selection.py

🧪 Test 1: User functions → UserController + 6 dependencies
🧪 Test 2: Order functions → OrderController mapping  
🧪 Test 3: Single function → Auto dependencies
```

## 🎯 HTML Functions Database

20 realistic functions được map như sau:

| HTML Function | Java Component | Dependencies |
|---------------|----------------|--------------|
| User Login Form | UserController | UserService, UserDTO, User |
| User Registration | UserController | UserService, UserDTO |
| Create New Order | OrderController | OrderService, OrderDTO |
| Order Status Tracking | OrderController | OrderService, Order |
| Product Search | Product | ProductRepository |
| Payment Processing | PaymentService | PaymentValidator |
| Notification Settings | NotificationService | - |
| Manage Addresses | Address | UserService |
| User Dashboard | UserRepository | User, UserDTO |
| Order Dashboard | OrderRepository | Order, OrderDTO |

## 💡 Workflow Summary

1. **HTML Functions**: Stored trong PostgreSQL với function_id và function_name
2. **Function Selector**: Load HTML functions từ database + Java functions từ source
3. **HTML-Only Mode**: User chỉ chọn HTML functions
4. **Auto Mapping**: HTML functions → Java controllers theo convention  
5. **Dependency Resolution**: Auto-add Services, DTOs, Models liên quan
6. **Graph Generation**: Tạo dependency graph cho full stack

## 🔧 Key Files Updated

- `html_db.py`: PostgreSQL connector với mapping logic
- `analyzer.py`: HTML-only mode với auto dependency resolution
- `server.py`: API endpoints cho HTML functions
- `recreate_html_data.py`: Sample data phù hợp với Java project
- `test_html_selection.py`: Demo script

## ✨ Demo Result

**Input**: Chọn "User Login Form" + "User Registration"
**Output**: Dependency graph với UserController + UserService + UserDTO + User + InvalidInputException + StringUtils

**Input**: Chọn "Create New Order" + "Order Status"  
**Output**: Dependency graph với OrderController + OrderService + OrderDTO + Order

👉 **Chỉ cần chọn HTML functions, hệ thống tự vẽ đường nối với Java backend!**
