# Course Registration System

Application source: [COURSE REGISTRATION SYSTEM new](<COURSE REGISTRATION SYSTEM new/README.md>).

## Đọc project từ đâu?

```text
COURSE REGISTRATION SYSTEM new/
├── frontend/src/       # Giao diện React và lời gọi API
│   ├── main.tsx        # Khởi động React
│   ├── App.tsx         # Định tuyến và phiên đăng nhập
│   ├── api.ts          # Gửi yêu cầu đến backend
│   ├── components/    # Thành phần giao diện dùng chung
│   └── pages/         # Các trang admin, giảng viên, sinh viên
├── backend/
│   ├── main.py        # Khởi động Flask
│   ├── auth.py        # API tài khoản
│   ├── admin.py       # API quản trị viên
│   ├── student.py     # API sinh viên
│   ├── lecturer.py    # API giảng viên
│   ├── domain/        # Các lớp xử lý nghiệp vụ
│   ├── database.py    # Truy cập PostgreSQL
│   ├── migrations/    # Nâng cấp database cũ
│   └── checks/        # Kiểm tra mã và API
├── dbschema.sql       # Cấu trúc database cài mới
└── README.md          # Hướng dẫn cài đặt và chạy chi tiết
```

Luồng xử lý: **Trang React → api.ts → route Flask → lớp domain → PostgreSQL**.

Ví dụ đăng ký môn: đọc `frontend/src/pages/student/CourseRegistration.tsx`,
`frontend/src/api.ts`, `backend/student.py`, rồi `backend/domain/student.py`.
Hai file `student.py` đảm nhiệm nhận HTTP và xử lý nghiệp vụ riêng biệt.

Các thư mục `.venv` và `node_modules` là môi trường/thư viện, không cần đọc để hiểu mã ứng dụng.

## Run on Windows (from this folder)

Backend in one PowerShell window:

```powershell
cd ".\COURSE REGISTRATION SYSTEM new\backend"
& "..\..\.venv\Scripts\python.exe" main.py
```

Frontend in a second PowerShell window:

```powershell
cd ".\COURSE REGISTRATION SYSTEM new\frontend"
npm.cmd run dev
```

Open http://localhost:8443. Existing PostgreSQL configuration stays in `backend/.env`.
For a fresh clone, follow the application README to install dependencies and initialize the database.
