# Java Dependency Graph Generator với Function Selector

## Tính năng mới: Function Selector Interface

### Mô tả
Bây giờ bạn có thể lựa chọn các classes, services, và methods cụ thể trước khi tạo dependency graph, giúp tạo ra các biểu đồ có mục tiêu và dễ hiểu hơn.

### Cách sử dụng

#### 1. Chế độ Function Selector (Mặc định)
```bash
python main.py path/to/java/source
```

Điều này sẽ:
- Phân tích tất cả file Java trong thư mục
- Mở giao diện web để bạn lựa chọn functions
- Cho phép tạo graph với chỉ những functions đã chọn

#### 2. Chế độ Direct (Tạo graph ngay)
```bash
python main.py path/to/java/source --direct
```

Tạo graph với tất cả functions ngay lập tức như phiên bản cũ.

#### 3. Tự động mở web interface
```bash
python main.py path/to/java/source --web
python main.py path/to/java/source --direct --web
```

### Giao diện Function Selector

#### Tính năng chính:
1. **Tìm kiếm Functions**: Tìm kiếm theo tên class, method, hoặc đường dẫn file
2. **Lọc theo loại**: 
   - Tất cả
   - Classes
   - Methods  
   - Services
3. **Lựa chọn hàng loạt**:
   - Chọn tất cả
   - Bỏ chọn tất cả
4. **Hiển thị thông tin chi tiết**: File path, số lượng dependencies cho mỗi function

#### Các loại Functions:
- **Classes**: Tất cả các class Java
- **Services**: Classes có tên kết thúc bằng "Service"
- **Methods**: Các method calls giữa các classes

### Workflow sử dụng:

1. **Khởi động**: Chạy `python main.py java-test-project2/src`
2. **Chọn Functions**: Sử dụng giao diện web để lựa chọn
   - Tìm kiếm functions cần thiết
   - Sử dụng filter để thu hẹp danh sách
   - Click vào các function cards để chọn/bỏ chọn
   - Kiểm tra số lượng đã chọn trong summary
3. **Tạo Graph**: Click "Tạo Dependency Graph"
4. **Xem kết quả**: Tự động chuyển đến trang dependency graph

### Ví dụ sử dụng thực tế:

#### Phân tích Service Layer:
1. Khởi động function selector
2. Filter theo "Services"
3. Chọn các Service classes quan tâm
4. Tạo graph để xem dependencies giữa các services

#### Phân tích một feature cụ thể:
1. Tìm kiếm theo tên feature (ví dụ: "Order")
2. Chọn tất cả classes liên quan đến Order
3. Tạo graph để xem luồng xử lý

#### Debug dependency issues:
1. Chọn các classes có vấn đề
2. Chọn thêm các classes liên quan
3. Xem graph để hiểu mối quan hệ

### Lợi ích:

1. **Graph có mục tiêu**: Chỉ hiển thị những gì bạn quan tâm
2. **Dễ hiểu hơn**: Ít noise, tập trung vào phần quan trọng
3. **Phân tích từng phần**: Chia nhỏ hệ thống lớn thành các phần dễ quản lý
4. **Interactive**: Có thể thử nghiệm nhiều tổ hợp khác nhau

### Cấu trúc file mới:

```
DependGraphForJava2/
├── main.py                     # Updated với function selector
├── analyzer.py                 # Added filter_by_selection method
├── server.py                   # Rebuilt với API endpoints mới
├── function_selector.html      # NEW: Giao diện lựa chọn functions
├── dependencies.html           # Graph viewer (như cũ)
├── dependency_template3.html   # Template (như cũ)
└── java-test-project2/         # Test project (như cũ)
```

### API Endpoints mới:

- `GET /api/functions`: Lấy danh sách tất cả functions
- `POST /api/generate`: Tạo graph với functions đã chọn
- `POST /api/edit`: Edit graph (như cũ)

### Troubleshooting:

#### Không thấy functions nào:
- Đảm bảo đường dẫn source directory đúng
- Kiểm tra có file .java trong thư mục không

#### Graph trống sau khi generate:
- Kiểm tra đã chọn ít nhất một function
- Thử chọn thêm các functions liên quan

#### Kết quả khác nhau giữa Function Selector và Direct mode:
- ✅ **Đã được sửa**: Khi chọn "Tất cả" trong Function Selector, kết quả giờ đây giống hệt Direct mode
- Function Selector tự động nhận diện khi ≥80% classes được chọn và giữ nguyên full graph
- Chỉ filter khi có selective choices để tạo focused graphs

#### Server không khởi động:
- Kiểm tra port 8000 có bị chiếm không
- Thử port khác với `--port 8001`

### Notes:
- Function Selector hiện hiển thị tối đa 100 methods để tránh UI quá tải
- Classes và Services được hiển thị đầy đủ
- Filter hoạt động real-time khi gõ
- **Smart Filtering**: Tự động detect "select all" scenarios và preserve full graph
- Services được classify riêng nhưng vẫn dùng chung ID format với classes
