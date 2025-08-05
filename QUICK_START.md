# Quick Start Guide - Function Selector

## 🚀 Khởi động nhanh

### 1. Function Selector Mode (Recommended)
```bash
python main.py java-test-project2/src
```
- Mở giao diện web để chọn functions
- Tạo graph với chỉ những functions quan tâm
- URL: http://localhost:8000/function_selector.html

### 2. Direct Mode  
```bash
python main.py java-test-project2/src --direct
```
- Tạo graph với tất cả functions ngay lập tức
- Không có bước lựa chọn

### 3. Demo Script
```bash
python demo.py
```
- Hướng dẫn interactive để test các options

## 🎯 Workflow với Function Selector

1. **Khởi động**: Chạy lệnh với function selector mode
2. **Browse**: Xem danh sách tất cả classes, services, methods
3. **Search**: Tìm kiếm functions cần thiết
4. **Filter**: Lọc theo loại (Classes/Services/Methods)
5. **Select**: Click để chọn/bỏ chọn functions
6. **Generate**: Click "Tạo Dependency Graph"
7. **View**: Tự động chuyển đến graph viewer

## 🔍 Tips

### Phân tích Service Layer:
- Filter → Services
- Chọn các *Service classes
- Tạo graph để xem service dependencies

### Focus vào một tính năng:
- Search → "Order" hoặc "User" 
- Chọn các classes liên quan
- Tạo graph để hiểu luồng xử lý

### Debug circular dependencies:
- Chọn các classes có vấn đề
- Xem graph để tìm vòng lặp dependency

## 📊 Thống kê Test Project

- **Total Classes**: 50
- **Total Method Calls**: 61  
- **Total Files**: 23
- **Top Callers**: Address(10), AppConfig(9), UserService(8)

## 🛠️ Troubleshooting

### Port đã được sử dụng:
```bash
python main.py java-test-project2/src --port 8001
```

### Graph trống:
- Đảm bảo đã chọn ít nhất 1 function
- Thử chọn thêm các related classes

### Server không khởi động:
- Kiểm tra Graphviz đã được cài đặt
- Kiểm tra port có available không
