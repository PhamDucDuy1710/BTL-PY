# HỆ THỐNG ĐIỂM DANH SINH VIÊN BẰNG NHẬN DIỆN KHUÔN MẶT

> **Môn học:** Bài tập lớn Lập trình Python  
> **Công nghệ lõi:** Python, Flask, OpenCV, Dlib / Face Recognition, SQLite3

---

## 1. MÔ TẢ DỰ ÁN

### 1.1. Bối cảnh & Mục tiêu

Điểm danh truyền thống bằng cách gọi tên hoặc truyền tay danh sách giấy gây mất thời gian giảng dạy, dễ nhầm lẫn và tiềm ẩn tình trạng điểm danh hộ.

Dự án xây dựng một **hệ thống điểm danh tự động dựa trên thị giác máy tính và nhận diện khuôn mặt theo thời gian thực (Real-time Face Recognition)**.

Sinh viên chỉ cần đi qua vùng quét của camera, hệ thống sẽ đối soát định danh và lưu trữ bằng chứng ra vào vào cơ sở dữ liệu.

### 1.2. Các tính năng cốt lõi

- **Kiosk quét điểm danh trực tiếp:** Màn hình Live Video Stream nhận diện khuôn mặt, vẽ bounding box, hiển thị thông tin sinh viên vừa quét và lịch sử ra/vào tức thì.
- **Quản trị sinh viên & lớp học:** Thêm, xóa, tìm kiếm danh sách sinh viên theo lớp.
- **Đăng ký khuôn mặt trực tuyến:** Tích hợp camera WebRTC trên giao diện web để chụp ảnh mẫu và gửi về máy chủ.
- **Huấn luyện tăng dần (Incremental Learning):** Khi thêm sinh viên mới, hệ thống trích xuất vector chạy nền qua `threading.Thread`, cập nhật `embeddings.pickle` mà không làm gián đoạn luồng video.
- **Debounce & Snapshot bằng chứng:** Cooldown 60 giây chống ghi log trùng lặp. Hệ thống tự động crop khuôn mặt thực tế tại thời điểm quét để lưu ảnh bằng chứng.
- **Bảo mật:** Mật khẩu quản trị viên được băm bằng `scrypt`/`pbkdf2:sha256`, route quản trị được bảo vệ bằng Session và dữ liệu động được lọc bằng `escapeHtml()` để hạn chế XSS.

---

## 2. CÔNG NGHỆ SỬ DỤNG

| Công nghệ | Vai trò |
|---|---|
| **Python** | Ngôn ngữ lập trình chính |
| **Flask** | Xây dựng Web Server và REST API |
| **OpenCV** | Xử lý hình ảnh và video từ camera |
| **Dlib / Face Recognition** | Phát hiện và nhận diện khuôn mặt |
| **SQLite3** | Lưu trữ dữ liệu hệ thống |
| **HTML/CSS/JavaScript** | Xây dựng giao diện Web |
| **WebRTC** | Truy cập camera trên trình duyệt |
| **Threading** | Xử lý tác vụ nền |
| **Pickle** | Lưu trữ vector đặc trưng khuôn mặt |

---

## 3. CẤU TRÚC THƯ MỤC

```text
├── database/
│   └── attendance.db
│
├── datasets/
│   ├── data/
│   │   └── <student_id>/...
│   │
│   └── face_features/
│       └── embeddings.pickle
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   ├── dashboard.js
│   │   └── attendance.js
│   │
│   ├── snapshots/
│   │
│   ├── attendance.html
│   ├── classes.html
│   ├── dashboard.html
│   ├── history.html
│   ├── login.html
│   └── students.html
│
├── add_persons.py
├── api.py
├── camera_manager.py
├── capture_face.py
├── check_attendance_table.py
├── db_config.py
├── recognize.py
└── requirements.txt
```

### Vai trò các tệp chính

| Tệp | Chức năng |
|---|---|
| `api.py` | Flask Server, HTTP routes, REST API, camera stream |
| `db_config.py` | Kết nối SQLite, tạo bảng và quản lý database |
| `camera_manager.py` | Quản lý webcam và đồng bộ luồng đọc frame |
| `recognize.py` | Phát hiện, trích xuất và so khớp khuôn mặt |
| `add_persons.py` | Trích xuất/cập nhật vector đặc trưng |
| `capture_face.py` | Công cụ chụp ảnh khuôn mặt thủ công |
| `check_attendance_table.py` | Kiểm tra nhanh dữ liệu database |
| `dashboard.js` | Logic giao diện quản trị và kích hoạt training |
| `attendance.js` | Polling dữ liệu điểm danh realtime |
| `requirements.txt` | Danh sách thư viện Python cần cài |

---

## 4. KIẾN TRÚC HỆ THỐNG

```text
                    ┌──────────────────────┐
                    │      Web Browser     │
                    │ HTML/CSS/JavaScript  │
                    └──────────┬───────────┘
                               │
                HTTP / REST API│ WebRTC
                               ▼
                    ┌──────────────────────┐
                    │      Flask API       │
                    │       api.py         │
                    └───────┬───────┬──────┘
                            │       │
              ┌─────────────┘       └──────────────┐
              ▼                                    ▼
    ┌───────────────────┐                 ┌──────────────────┐
    │ Camera Manager    │                 │   SQLite3 DB     │
    │ camera_manager.py │                 │ attendance.db    │
    └─────────┬─────────┘                 └──────────────────┘
              │
              ▼
    ┌───────────────────┐
    │ Face Recognition  │
    │   recognize.py    │
    └─────────┬─────────┘
              │
              ▼
    ┌───────────────────┐
    │ Face Embeddings   │
    │ embeddings.pickle │
    └───────────────────┘
```

---

## 5. MỐI LIÊN KẾT GIỮA CÁC MODULE

### 5.1. Khởi tạo & kết nối CSDL

```text
db_config.py
     │
     │ init_db()
     ▼
 attendance.db
     │
     ├── admins
     ├── classes
     ├── students
     └── access_logs
     ▲
     │
   api.py
```

- `db_config.py` quản lý 4 bảng:
  - `admins`
  - `classes`
  - `students`
  - `access_logs`
- Kích hoạt `PRAGMA foreign_keys = ON`.
- `api.py` gọi `init_db()` khi server khởi động.
- Hệ thống có tài khoản quản trị mặc định:

```text
Username: admin
Password: password
```

> Khuyến nghị thay đổi mật khẩu mặc định trước khi triển khai thực tế.

---

### 5.2. Đăng ký khuôn mặt

```text
students.html
      │
      │ WebRTC Camera
      ▼
Base64 Image
      │
      ▼
POST /api/students/register_face
      │
      ▼
     api.py
      │
      ├──────────────► SQLite
      │
      └──────────────► datasets/data/<student_id>/
                              │
                              ▼
                    extract_and_update_features()
                              │
                              ▼
                     embeddings.pickle
```

Khi sinh viên đăng ký khuôn mặt:

1. Người dùng bật camera trên trình duyệt.
2. WebRTC chụp ảnh mẫu.
3. Ảnh được chuyển thành dữ liệu Base64.
4. Gửi đến Flask API.
5. Server lưu thông tin sinh viên vào SQLite.
6. Ảnh được lưu vào thư mục tương ứng.
7. Luồng nền trích xuất vector đặc trưng.
8. Vector mới được cập nhật vào `embeddings.pickle`.

---

### 5.3. Streaming & nhận diện trực tiếp

```text
Webcam
   │
   ▼
camera_manager.py
   │
   ▼
generate_frames()
   │
   ▼
recognize.py
   │
   ├── Face Detection
   ├── Face Encoding
   ├── Distance Matching
   └── Attendance Check
   │
   ▼
JPEG Frame
   │
   ▼
/video_feed
   │
   ▼
attendance.html
```

Đồng thời giao diện Kiosk sử dụng JavaScript Polling:

```text
attendance.js
      │
      ├──► /api/current-detected
      │
      └──► /api/access-logs
                  │
                  ▼
          Cập nhật giao diện
             theo thời gian thực
```

---

# 6. NGUYÊN LÝ THUẬT TOÁN NHẬN DIỆN

Hệ thống áp dụng phương pháp **Deep Metric Learning**, gồm 4 giai đoạn chính.

## 6.1. Face Detection

Khung hình được giảm kích thước còn `1/4`:

```python
small_frame = cv2.resize(
    frame,
    (0, 0),
    fx=0.25,
    fy=0.25
)
```

Sau đó chuyển từ BGR sang RGB và sử dụng bộ phát hiện khuôn mặt của thư viện `face_recognition`.

Quá trình này giúp giảm lượng tính toán và tăng tốc độ xử lý video realtime.

---

## 6.2. Feature Extraction

Mỗi khuôn mặt được chuyển thành một vector đặc trưng có **128 chiều (128-d embedding)**.

```text
Face Image
    │
    ▼
Face Detection
    │
    ▼
Facial Landmarks
    │
    ▼
Face Encoding
    │
    ▼
128-dimensional Vector
```

Vector này đại diện cho đặc điểm hình học/đặc trưng của khuôn mặt và được sử dụng để so sánh giữa các cá nhân.

---

## 6.3. So khớp khoảng cách

Hệ thống sử dụng khoảng cách Euclidean:

$$
d(\vec{x}, \vec{y}) =
\sqrt{
\sum_{i=1}^{128}(x_i-y_i)^2
}
$$

Trong đó:

- `x`: vector khuôn mặt vừa được camera phát hiện.
- `y`: vector khuôn mặt mẫu trong cơ sở dữ liệu.
- `d(x, y)`: khoảng cách giữa hai khuôn mặt.
- Khoảng cách càng nhỏ → hai khuôn mặt càng giống nhau.

### Min-Distance

Nếu một sinh viên có nhiều ảnh mẫu, hệ thống lấy khoảng cách nhỏ nhất của sinh viên đó:

```text
Student A:
    Image 1 → distance = 0.61
    Image 2 → distance = 0.43
    Image 3 → distance = 0.49

Min distance của A = 0.43
```

Sau đó sử dụng giá trị này để xếp hạng ứng viên.

---

## 6.4. Ngưỡng nhận diện

Ứng viên gần nhất phải thỏa mãn:

$$
top_1 \leq 0.52
$$

Nếu khoảng cách lớn hơn ngưỡng:

```text
→ Không xác định
```

### Top-2 Margin Check

Ngoài khoảng cách tuyệt đối, hệ thống kiểm tra sự khác biệt giữa hai ứng viên gần nhất:

$$
margin = top_2 - top_1
$$

Nếu:

$$
margin < 0.05
$$

thì hai ứng viên quá giống nhau và hệ thống từ chối nhận diện:

```text
→ Không xác định
```

Cơ chế này giúp giảm nguy cơ nhận diện nhầm khi hai khuôn mặt có vector tương đối gần nhau.

---

# 7. CƠ CHẾ CHỐNG GHI ĐIỂM DANH TRÙNG

Hệ thống sử dụng **Cooldown / Debounce 60 giây**.

```text
Sinh viên được nhận diện
        │
        ▼
Kiểm tra lần điểm danh gần nhất
        │
        ├── < 60 giây ──► Không ghi log mới
        │
        └── >= 60 giây ─► Ghi điểm danh
                              │
                              ├── Lưu snapshot
                              └── Ghi access_logs
```

Ví dụ:

```text
10:00:00 → Điểm danh ✓
10:00:20 → Bỏ qua
10:00:45 → Bỏ qua
10:01:00 → Có thể điểm danh lại
```

Cơ chế này tránh việc một sinh viên đứng trước camera trong nhiều giây tạo ra hàng chục bản ghi.

---

# 8. SNAPSHOT BẰNG CHỨNG

Khi điểm danh thành công, hệ thống crop khuôn mặt trực tiếp từ frame hiện tại và lưu vào:

```text
static/snapshots/
```

Snapshot có thể được sử dụng để:

- Đối soát lịch sử điểm danh.
- Kiểm tra trường hợp nhận diện sai.
- Hiển thị bằng chứng trên trang lịch sử.
- Hỗ trợ quản trị viên kiểm tra dữ liệu.

---

# 9. DATABASE

Hệ thống sử dụng **SQLite3** với 4 bảng chính:

```text
┌──────────────┐
│    admins    │
└──────────────┘

┌──────────────┐
│    classes   │
└──────────────┘
        │
        ▼
┌──────────────┐
│   students   │
└──────────────┘
        │
        ▼
┌──────────────┐
│  access_logs │
└──────────────┘
```

### Các bảng

| Bảng | Mục đích |
|---|---|
| `admins` | Tài khoản quản trị |
| `classes` | Danh sách lớp học |
| `students` | Thông tin sinh viên |
| `access_logs` | Lịch sử điểm danh |

Khóa ngoại được bật bằng:

```sql
PRAGMA foreign_keys = ON;
```

---

# 10. BẢO MẬT

### 10.1. Password Hashing

Mật khẩu quản trị viên không được lưu trực tiếp dưới dạng plaintext mà được băm bằng:

```text
scrypt
```

hoặc:

```text
pbkdf2:sha256
```

---

### 10.2. Session Authentication

Các route quản trị yêu cầu người dùng đăng nhập trước khi truy cập.

```text
Login
  │
  ▼
Session
  │
  ├── Valid ──► Dashboard
  │
  └── Invalid ► Login
```

---

### 10.3. Chống XSS

Dữ liệu động hiển thị trên giao diện được xử lý thông qua:

```javascript
escapeHtml()
```

nhằm hạn chế việc chèn HTML/JavaScript độc hại vào giao diện.

---

# 11. CÀI ĐẶT

## 11.1. Yêu cầu môi trường

- Python **3.10 hoặc 3.11**
- Windows 10/11, macOS hoặc Linux
- Webcam kết nối với máy tính

> Python 3.10/3.11 được khuyến nghị vì các thư viện liên quan đến `dlib`/`face_recognition` có thể gặp vấn đề tương thích trên các phiên bản Python mới hơn.

---

## 11.2. Clone project

```bash
git clone <YOUR_REPOSITORY_URL>
cd <PROJECT_FOLDER>
```

---

## 11.3. Tạo Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 11.4. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Lưu ý trên Windows

Nếu gặp lỗi khi cài đặt `dlib`, có thể cần cài:

- CMake
- Visual Studio C++ Build Tools

Sau đó chạy lại:

```bash
pip install -r requirements.txt
```

---

# 12. KHỞI CHẠY

## 12.1. Khởi động Flask Server

```bash
python api.py
```

Nếu server khởi động thành công, truy cập:

### Bảng quản trị

```text
http://127.0.0.1:5001/login
```

Tài khoản mặc định:

```text
Username: admin
Password: password
```

### Kiosk điểm danh

```text
http://127.0.0.1:5001/attendance
```

---

# 13. QUY TRÌNH SỬ DỤNG

## Bước 1 — Đăng nhập quản trị

Truy cập:

```text
http://127.0.0.1:5001/login
```

Đăng nhập bằng tài khoản quản trị.

---

## Bước 2 — Quản lý lớp học

Quản trị viên có thể:

- Thêm lớp.
- Xóa lớp.
- Xem danh sách lớp.
- Quản lý sinh viên theo từng lớp.

---

## Bước 3 — Thêm sinh viên

Nhập thông tin sinh viên và thực hiện đăng ký khuôn mặt bằng camera WebRTC.

Ảnh mẫu được lưu tại:

```text
datasets/data/<student_id>/
```

---

## Bước 4 — Cập nhật Face Embedding

Hệ thống tự động chạy tác vụ nền:

```text
extract_and_update_features()
```

để tạo/cập nhật:

```text
datasets/face_features/embeddings.pickle
```

---

## Bước 5 — Điểm danh

Mở:

```text
http://127.0.0.1:5001/attendance
```

Sinh viên đứng trước camera.

Hệ thống thực hiện:

```text
Camera
  ↓
Face Detection
  ↓
Face Encoding
  ↓
Distance Matching
  ↓
Top-1 + Margin Check
  ↓
Cooldown Check
  ↓
Attendance Log
  ↓
Snapshot
```

---

# 14. LUỒNG XỬ LÝ TỔNG QUÁT

```text
                    START
                      │
                      ▼
              Khởi động Flask
                      │
                      ▼
                 init_db()
                      │
                      ▼
               Mở Camera
                      │
                      ▼
              Đọc Frame liên tục
                      │
                      ▼
              Phát hiện khuôn mặt
                      │
                 Có khuôn mặt?
                 /          \
               Không         Có
                │             │
                └──────┐      ▼
                       │   Face Encoding
                       │      │
                       │      ▼
                       │  So khớp Embedding
                       │      │
                       │      ▼
                       │  Kiểm tra Threshold
                       │      │
                       │   Hợp lệ?
                       │   /       \
                       │ Không      Có
                       │  │          │
                       │  ▼          ▼
                       │ Unknown  Kiểm tra Margin
                       │             │
                       │          Hợp lệ?
                       │          /     \
                       │        Không    Có
                       │         │        │
                       │         ▼        ▼
                       │      Unknown  Cooldown
                       │                    │
                       │                 >= 60s?
                       │                /       \
                       │              Không      Có
                       │               │          │
                       │               ▼          ▼
                       │            Bỏ qua    Ghi Log
                       │                          │
                       │                          ▼
                       │                      Snapshot
                       │
                       └──────────────► Hiển thị Frame
```

---

# 15. HIỆU NĂNG & XỬ LÝ ĐA LUỒNG

Hệ thống sử dụng `threading.Thread` cho các tác vụ cần thời gian xử lý lớn như cập nhật face embedding.

```text
Main Thread
    │
    ├── Camera
    ├── Video Streaming
    └── API Requests

Background Thread
    │
    └── Feature Extraction
```

Nhờ đó, việc thêm sinh viên hoặc tạo embedding mới không cần khóa toàn bộ luồng camera.

`camera_manager.py` sử dụng:

```python
threading.Lock
```

để hạn chế tình trạng nhiều luồng cùng truy cập webcam.

---

# 16. API CHÍNH

Một số endpoint tiêu biểu:

| Endpoint | Phương thức | Chức năng |
|---|---|---|
| `/login` | `GET/POST` | Đăng nhập quản trị |
| `/attendance` | `GET` | Trang Kiosk điểm danh |
| `/video_feed` | `GET` | Video stream từ camera |
| `/api/current-detected` | `GET` | Sinh viên đang được nhận diện |
| `/api/access-logs` | `GET` | Lấy lịch sử điểm danh |
| `/api/students/register_face` | `POST` | Đăng ký khuôn mặt |
| Các API quản lý lớp | `GET/POST/...` | Quản lý lớp học |
| Các API quản lý sinh viên | `GET/POST/...` | Quản lý sinh viên |

> Danh sách endpoint có thể thay đổi tùy theo phiên bản triển khai thực tế của `api.py`.

---

# 17. CẤU TRÚC DỮ LIỆU EMBEDDING

File:

```text
datasets/face_features/embeddings.pickle
```

lưu các vector đặc trưng khuôn mặt cùng thông tin định danh sinh viên.

Mô hình khái niệm:

```text
Student ID
    │
    ├── Face Embedding 1 → [128 values]
    ├── Face Embedding 2 → [128 values]
    └── Face Embedding 3 → [128 values]
```

Khi nhận diện:

```text
Camera Face
     │
     ▼
128-d Embedding
     │
     ▼
So sánh với Embeddings
     │
     ▼
Student ID gần nhất
```

---

# 18. XỬ LÝ XÓA SINH VIÊN

Khi xóa sinh viên, hệ thống cần đồng bộ nhiều loại dữ liệu:

```text
Delete Student
      │
      ├──► Xóa record trong SQLite
      │
      ├──► Xóa datasets/data/<student_id>/
      │
      └──► Xóa/cập nhật embedding tương ứng
```

Điều này giúp tránh dữ liệu khuôn mặt cũ tiếp tục được sử dụng để nhận diện.

---

# 19. HẠN CHẾ CỦA HỆ THỐNG

Một số yếu tố có thể ảnh hưởng đến độ chính xác:

- Ánh sáng quá yếu hoặc quá mạnh.
- Khuôn mặt bị che bởi khẩu trang hoặc vật thể.
- Góc quay khuôn mặt quá lớn.
- Camera có độ phân giải thấp.
- Hai người có ngoại hình tương đối giống nhau.
- Chất lượng ảnh mẫu không tốt.
- Ngưỡng `0.52` và margin `0.05` cần được hiệu chỉnh tùy môi trường triển khai.

Hệ thống hiện tại phù hợp với **môi trường lớp học/phòng học có camera cố định** hơn là môi trường ngoài trời hoặc có số lượng người rất lớn.

---

# 20. HƯỚNG PHÁT TRIỂN

Một số hướng có thể phát triển trong tương lai:

- [ ] Thêm phân quyền nhiều cấp: Admin / Teacher / Student.
- [ ] Xuất lịch sử điểm danh ra Excel/CSV.
- [ ] Thống kê tỷ lệ chuyên cần theo sinh viên/lớp.
- [ ] Thêm biểu đồ thống kê trên Dashboard.
- [ ] Cải thiện khả năng nhận diện trong điều kiện ánh sáng khác nhau.
- [ ] Hỗ trợ nhiều camera.
- [ ] Tối ưu tốc độ nhận diện GPU.
- [ ] Thêm Docker để triển khai dễ dàng.
- [ ] Xây dựng REST API hoàn chỉnh.
- [ ] Thêm logging và monitoring.
- [ ] Cải thiện cơ chế chống giả mạo khuôn mặt (Anti-Spoofing/Liveness Detection).
- [ ] Tách frontend/backend thành kiến trúc độc lập.

---

# 21. KẾT QUẢ ĐẠT ĐƯỢC

Dự án đã xây dựng được một hệ thống điểm danh tự động với các thành phần chính:

- Nhận diện khuôn mặt realtime.
- Quản lý sinh viên.
- Quản lý lớp học.
- Đăng ký khuôn mặt qua WebRTC.
- Lưu trữ embedding 128 chiều.
- Điểm danh và lưu lịch sử vào SQLite.
- Snapshot khuôn mặt làm bằng chứng.
- Cooldown chống ghi nhận trùng.
- Dashboard quản trị.
- Xác thực Session.
- Hash mật khẩu.
- Xử lý tác vụ nền bằng Threading.
- Giao tiếp giữa frontend và Flask thông qua REST API.

---

# 22. TÁC GIẢ

**Sinh viên thực hiện:** 

**Môn học:** Bài tập lớn Lập trình Python

**Định hướng:** Computer Vision / AI / Software Engineering

---

## LICENSE

Dự án được thực hiện phục vụ mục đích **học tập và nghiên cứu**.
