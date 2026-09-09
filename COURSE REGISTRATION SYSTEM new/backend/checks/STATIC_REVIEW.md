# Kết quả kiểm tra tĩnh backend

Ngày thực hiện: 08/09/2026.

| Nội dung | Kết quả |
|---|---|
| AST và biên dịch cú pháp 24 tệp Python của ứng dụng | PASS |
| Docstring cho 166 lớp/hàm/phương thức viết tay, gồm cả công cụ kiểm tra | PASS |
| 11 lớp nghiệp vụ và các phương thức đã liệt kê từ Class Diagram | PASS |
| Student, Lecturer, Administrator kế thừa User | PASS |
| Import nội bộ, biểu tượng được import, phát hiện vòng import | PASS |
| 51 route ban đầu: đường dẫn, HTTP method, decorator quyền và tham số | PASS |
| 52 lời gọi phương thức từ route, gồm API logout mới | PASS |
| 84 truy vấn có chuỗi SQL và tuple/list tham số xác định tĩnh | PASS: số placeholder khớp số giá trị |
| Ruff `check --select E9,F,B` | PASS: All checks passed |
| Ruff `format --check` | PASS |

Các lỗi được xử lý trong quá trình kiểm tra: import datetime không dùng; zip trong công cụ kiểm tra cần chỉ rõ strict; phạm vi kiểm tra được giới hạn vào mã ứng dụng, loại môi trường ảo và thư viện ngoài.

Qua đọc mã cũng đã sửa việc trả cursor đã đóng, kiểm tra điểm không hữu hạn, tín chỉ/sĩ số sai kiểu, ngày không hợp lệ và bổ sung kiểm tra đợt đăng ký đã kết thúc khi cập nhật điểm.

Kết quả chỉ áp dụng trong phạm vi kiểm tra tĩnh. Chưa khởi chạy Flask/PostgreSQL, chưa kiểm thử giao diện, chưa xác nhận dữ liệu thật hoặc tính đúng đắn của các giao dịch đồng thời. Kiểm tra placeholder không thay thế việc chạy SQL với schema thật.

Chạy lại kiểm tra không cần cài thư viện ngoài:

```powershell
python backend/checks/static_check.py
```

Lệnh trên chạy từ thư mục `COURSE REGISTRATION SYSTEM new`. Công cụ đọc snapshot `route_contract.json` để đối chiếu các API trước khi tổ chức lại backend.
