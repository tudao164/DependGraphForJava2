# PostgreSQL Integration - HTML Functions Database

## 🎯 Tổng quan

Hệ thống đã được tích hợp thành công với PostgreSQL database để quản lý HTML/JS functions. Người dùng có thể:

1. **Lựa chọn functions**: Cả Java classes/methods và HTML functions từ database
2. **HTML→Java mapping**: HTML functions tự động được map đến Java controllers
3. **Graph generation**: Tạo dependency graph bao gồm cả frontend và backend

## 🗄️ Database Schema

```sql
-- Database: graph
-- Schema: public  
-- Table: html_function

CREATE TABLE public.html_function (
    function_id VARCHAR(255) PRIMARY KEY,
    function_name VARCHAR(255) NOT NULL
);

-- Sample data đã được insert:
-- 10 HTML functions mapping đến các Java controllers
```

## 🔧 Cấu hình

### Database Connection
- **Host**: localhost
- **Port**: 5432  
- **Database**: graph
- **User**: postgres
- **Password**: 123456
- **Schema**: public

### Files được update:
- `html_db.py`: PostgreSQL connector với psycopg2
- `analyzer.py`: Thêm HTML database integration
- `server.py`: API endpoints cho HTML functions
- `db_config.py`: Database configuration
- `insert_sample_data.py`: Script để thêm sample data

## 🚀 Usage

### 1. Khởi động Function Selector
```bash
python main.py java-test-project2
```

### 2. Truy cập Web Interface
- URL: http://localhost:8000/function_selector.html
- Hiển thị: Java classes/methods + HTML functions từ database
- Chọn functions và generate graph

### 3. HTML→Java Mapping Convention

HTML functions được map đến Java controllers theo logic:

```python
# Convention-based mapping
login* → UserController
user* → UserController  
order* → OrderController
product* → ProductController
payment* → PaymentController
address* → UserController
```

## 📊 API Endpoints

### GET /api/functions
Trả về tất cả functions (Java + HTML):
```json
{
  "success": true,
  "functions": [
    {
      "id": "html_1",
      "function_id": 1,
      "name": "loginForm()",
      "file": "Frontend/loginForm()",
      "type": "html",
      "description": "HTML/JS function: loginForm()",
      "dependencies": 1
    },
    {
      "id": "class_UserController", 
      "name": "UserController",
      "type": "class",
      "file": "src/main/java/.../UserController.java",
      "dependencies": 3
    }
  ]
}
```

### POST /api/generate
Generate graph với selected functions:
```json
{
  "selectedFunctions": ["html_1", "html_4", "class_UserController", "class_OrderController"]
}
```

## 🔍 Current Status

✅ **Hoàn thành:**
- PostgreSQL connection với psycopg2
- HTML function database integration  
- Function selector UI hiển thị HTML functions
- HTML→Java controller mapping logic
- API endpoints hoạt động

✅ **Sample Data:**
- 10 HTML functions đã được insert
- Mapping đến UserController, OrderController, ProductController

✅ **Testing:**
- Database connection OK
- API endpoints trả về đúng data
- Function selector hiển thị cả Java và HTML functions

## 🎯 Workflow

1. **Database**: PostgreSQL chứa HTML functions với function_id và function_name
2. **Function Selector**: Web UI load cả Java classes và HTML functions
3. **Selection**: User chọn mix of Java classes và HTML functions  
4. **Mapping**: HTML functions được map đến Java controllers
5. **Graph Generation**: Tạo dependency graph với full stack view

## 🔧 Maintenance

### Thêm HTML Functions mới:
```python
from html_db import HTMLFunctionDatabase

db = HTMLFunctionDatabase()
db.add_function({
    'function_id': '11',
    'function_name': 'newFeature()'
})
```

### Update Mapping Logic:
Sửa method `get_controller_mappings_for_html()` trong `html_db.py`

### Monitor Database:
```bash
python html_db.py  # Test connection
python db_config.py  # Validate config
```

## 💡 Next Steps

Có thể mở rộng:
1. **Advanced Mapping**: Thêm bảng mapping riêng cho HTML→Java
2. **Function Details**: Thêm metadata như endpoints, parameters
3. **Real-time Sync**: Auto-detect HTML functions từ source code
4. **Multi-schema**: Support multiple projects trong cùng database
