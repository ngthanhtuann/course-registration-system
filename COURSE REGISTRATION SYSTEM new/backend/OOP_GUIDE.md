# Backend hướng đối tượng trong kiến trúc Client–Server

Kiến trúc hệ thống vẫn là **Client–Server**: React gửi HTTP API tới Flask; server xử lý nghiệp vụ và truy cập PostgreSQL. Thư mục `domain/` tổ chức các đối tượng nghiệp vụ bên trong server, không chuyển hệ thống sang MVC.

## Cách đọc mã nguồn

1. `student.py`, `lecturer.py`, `admin.py`, `auth.py`: nhận HTTP, kiểm tra quyền qua decorator, truyền dữ liệu tới đối tượng nghiệp vụ rồi trả JSON.
2. `domain/`: chứa 11 lớp theo Class Diagram. Các lớp nhận dictionary/tham số thông thường, không sử dụng `request` hoặc `jsonify` của Flask.
3. `database.py`: mở kết nối, thực thi SQL có tham số, commit/rollback và đóng kết nối.
4. `credentials.py`: băm mật khẩu, kiểm tra mật khẩu và tạo JWT.
5. `security.py`: xác thực JWT và kiểm tra quyền tại API.
6. `http_support.py`: đọc JSON object và chuyển kết quả nghiệp vụ thành phản hồi HTTP.

Mỗi lớp, hàm và phương thức viết tay đều có docstring tiếng Việt ngay dưới phần khai báo. Docstring là phần giải thích gắn trực tiếp với lớp/hàm trong Python, có thể xem bằng IDE hoặc `help()`.

## Cách viết mã để dễ học

Các lớp dùng `class` và hàm khởi tạo `__init__` thông thường. Ví dụ `Student(User)` nghĩa là Student kế thừa User; `self.studentID` là mã của đối tượng sinh viên hiện tại. `super().__init__(identity)` gọi phần khởi tạo của User để sinh viên cũng có các thông tin tài khoản chung.

Route được viết thành từng bước, ví dụ:

```python
current_user = get_current_user()      # Lấy người dùng đang đăng nhập
student = Student(current_user)       # Tạo đối tượng sinh viên
data = read_json_object()             # Đọc dữ liệu gửi từ giao diện
result = student.registerCourse(data) # Gọi chức năng đăng ký học phần
return api_response(result)           # Trả kết quả về giao diện
```

Trong các hàm nghiệp vụ, `data` là dữ liệu gửi lên, `query` là tham số lọc trên URL, `db` là kết nối cơ sở dữ liệu và `student_record` là một hàng thông tin sinh viên đọc từ database. `return {"error": "..."}, 400` trả thông báo lỗi cùng mã HTTP 400.

`try` chứa thao tác có thể gặp lỗi; `except` xử lý khi lỗi xảy ra; `finally` luôn chạy để đóng kết nối. `commit()` xác nhận lưu các thay đổi; `rollback()` hủy các thay đổi chưa xác nhận. Không bỏ các bước này vì chúng bảo vệ dữ liệu đăng ký.

Bắt đầu đọc từ `student.py`, sau đó tới `domain/student.py` và hàm `registerCourse()`. Hàm này có chú thích theo từng bước xử lý. Công cụ `checks/static_check.py` chỉ phục vụ kiểm tra mã, không thuộc luồng nghiệp vụ của hệ thống.

## Đối chiếu Class Diagram

| Lớp | Tệp | Trách nhiệm đã triển khai |
|---|---|---|
| User | `domain/user.py` | Thuộc tính tài khoản; login, viewAccountInfo, updateProfile, changePassword, logout. Mật khẩu không lưu dạng rõ trong đối tượng. |
| Administrator(User) | `domain/administrator.py` | Quản lý người dùng, ngành, chương trình, học phần, học kỳ, đợt đăng ký, báo cáo và phân công. |
| Student(User) | `domain/student.py` | Xem học phần, đăng ký, hủy đăng ký, xem trạng thái và điểm; hồ sơ có studentID, dateOfBirth và ngành. |
| Lecturer(User) | `domain/lecturer.py` | Xem học phần được phân công, sinh viên đăng ký và quản lý điểm. |
| Major | `domain/major.py` | Ngành học và kiểm tra học phần thuộc chương trình của ngành. |
| Course | `domain/course.py` | Thông tin học phần, checkPrerequisite, checkCapacity, kiểm tra số nguyên dương. |
| Semester | `domain/semester.py` | Thời gian học kỳ và checkOverlap khi tạo/cập nhật. |
| RegistrationPeriod | `domain/registration_period.py` | Trạng thái upcoming/open/closed tính từ ngày; được dùng khi hủy đăng ký. |
| Registration | `domain/registration.py` | saveRegistration và updateRegistrationStatus trong giao dịch do Student quản lý. |
| GradeRecord | `domain/grade_record.py` | Điểm và calculateResultStatus; được Lecturer gọi khi cập nhật điểm. |
| TeachingAssignment | `domain/teaching_assignment.py` | Liên kết giảng viên–học phần–học kỳ; kiểm tra chuyên môn và lưu phân công. |

Các phương thức `manage...` trong sơ đồ là nhóm chức năng. API danh sách gọi các phương thức tương ứng; thao tác thêm/sửa/xóa được triển khai thành các phương thức cụ thể như `create_course`, `update_course`, `delete_course` trong cùng đối tượng Administrator. `manageStudent` và `manageLecturer` cung cấp danh sách theo vai trò; API `/admin/users` hiện vẫn trả chung các vai trò như frontend đang sử dụng.

Sơ đồ dùng kiểu trả về khái quát như boolean/list/void. Ở mã triển khai, nghiệp vụ trả dictionary/list hoặc cặp `(payload, status)` để mô tả cả kết quả và lỗi; `api_response()` chuyển dữ liệu đó sang JSON. Các phương thức kiểm tra như `checkPrerequisite`, `checkCapacity`, `checkOverlap` trả boolean.

## Ví dụ luồng đăng ký

`POST /api/student/registrations` → kiểm tra quyền student → `Student.registerCourse()` → khóa hàng Course và đợt đăng ký → `Major.includesCourse()` → kiểm tra đăng ký trùng/môn đã đạt → `Course.checkPrerequisite()` → `Course.checkCapacity()` → `Registration.saveRegistration()` → commit → JSON.

Khóa hàng được giữ trên cùng kết nối đến khi commit hoặc rollback; các đối tượng con không tự mở kết nối mới trong luồng đăng ký. `Database.close()` đóng giao dịch chưa commit nếu thoát sớm.

## Ánh xạ dữ liệu và các quy ước triển khai

- Quan hệ giữa các đối tượng được lưu bằng mã định danh/khóa ngoại; không phải mỗi đối tượng đều được tải toàn bộ từ database ngay khi khởi tạo.
- `Student`, `Lecturer`, `Administrator` kế thừa User trong Python; các bảng vai trò tiếp tục liên kết tới bảng users bằng user_id.
- Quan hệ nhiều–nhiều Major–Course dùng bảng curriculum. `Course.recommendedSemester` là thông tin theo chương trình, không phải thuộc tính chung bắt buộc trong bảng courses.
- Ngữ cảnh học kỳ của Course được xác định qua đợt đăng ký hoặc phân công, không bổ sung cột semester vào courses.
- GradeRecord được lưu trong `registrations.grade` và `registrations.result_status`; không tạo bảng mới. Đăng ký chưa có điểm tương ứng không có kết quả điểm.
- RegistrationPeriod.registrationStatus được tính theo ngày, không lưu cột có thể trở nên lỗi thời.
- TeachingAssignment.assignmentID dùng chuỗi vì schema/API hiện tại dùng varchar. Phân công tồn tại được xem là active; gỡ phân công vẫn xóa hàng theo chức năng hiện tại, không bổ sung lịch sử trạng thái.
- Tên `manageStudentGrade` dùng đúng nghĩa quản lý điểm (sơ đồ ghi `managaStudentGrade`).

Các quy ước này là ánh xạ giữa thiết kế khái niệm và schema/API đang dùng; không phải khẳng định mọi kiểu dữ liệu trong sơ đồ được sao chép nguyên văn.

## Thay đổi hành vi có chủ đích

- Theo trang 36 của đặc tả, cập nhật điểm chỉ được chấp nhận khi các đợt đăng ký của học kỳ đã kết thúc. Nếu chưa kết thúc, API trả 400 với `registration period has not ended`. Nếu một học kỳ có nhiều đợt thì phải chờ tất cả các đợt kết thúc.
- GradeRecord từ chối NaN/infinity và điểm ngoài 0–10; điểm từ 5 là passed, thấp hơn là not passed, chưa nhập là None.
- Tạo/cập nhật học phần từ chối tín chỉ và sĩ số không phải số nguyên dương với mã 400.
- Ngày không hợp lệ khi tạo/cập nhật học kỳ và đợt đăng ký trả 400.
- JSON body phải là object, không chấp nhận mảng/chuỗi làm dữ liệu biểu mẫu.
- API hồ sơ sinh viên bổ sung trường dob; các trường cũ vẫn giữ nguyên.
- Bổ sung `POST /api/logout` để gọi User.logout. Frontend hiện đang xóa JWT ở client và vẫn hoạt động như cũ. Endpoint này không thu hồi JWT đã cấp; client vẫn phải xóa token, token cũ hết hạn theo cấu hình.
- Database.execute và execute_query trả số hàng tác động thay vì trả cursor đã bị đóng. Các nơi gọi hiện tại không dùng giá trị trả về này.

## Kiểm tra tĩnh

Chạy từ thư mục dự án:

```powershell
python backend/checks/static_check.py
python -m ruff check backend --select E9,F,B
python -m ruff format --check backend
```

Ruff là công cụ phát triển tùy chọn; cài bằng `python -m pip install ruff`. Chương trình `static_check.py` chỉ dùng thư viện chuẩn Python và không cần database.

`static_check.py` kiểm tra cú pháp bằng AST/compile, docstring, import nội bộ và vòng import, lớp/phương thức UML, kế thừa, 51 route cũ (đường dẫn, HTTP method, decorator phân quyền và tham số), chữ ký phương thức được route gọi, và số placeholder SQL có thể xác định tĩnh. Snapshot API trước khi sửa nằm trong `checks/route_contract.json`.

Kiểm tra tĩnh không chứng minh truy vấn đúng với database đang chạy, tất cả yêu cầu chức năng đã đạt, hoặc hệ thống xử lý đồng thời đúng trong mọi tình huống. Chưa chạy kiểm thử tích hợp Flask/PostgreSQL hoặc giao diện trong lần chỉnh sửa này.
