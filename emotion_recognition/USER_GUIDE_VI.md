# Hướng dẫn sử dụng ứng dụng nhận diện cảm xúc khuôn mặt

## Giới thiệu

Ứng dụng nhận diện cảm xúc khuôn mặt là một ứng dụng web Django cho phép người dùng tải lên hình ảnh và nhận diện cảm xúc của khuôn mặt trong ảnh. Ứng dụng sử dụng mô hình học máy hybrid CNN-SIFT để nhận diện 7 cảm xúc cơ bản: giận dữ, khinh miệt, ghê tởm, sợ hãi, vui vẻ, buồn bã và ngạc nhiên.

## Cài đặt và chạy ứng dụng

### Yêu cầu hệ thống

- Python 3.8+
- Django 5.2+
- TensorFlow 2.19+
- OpenCV 4.11+
- Scikit-learn 1.6+
- NumPy 2.1+
- Pillow 11.2+

### Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd Facial-Emotion-Recognition
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r emotion_recognition/requirements.txt
```

3. Chạy các migrations để khởi tạo cơ sở dữ liệu:
```bash
cd emotion_recognition
python manage.py migrate
```

4. Tạo tài khoản admin (tùy chọn):
```bash
python manage.py createsuperuser
```

5. Chạy ứng dụng:
```bash
python manage.py runserver
```

6. Truy cập ứng dụng tại địa chỉ: http://127.0.0.1:8000/

## Hướng dẫn sử dụng

### Trang chủ

1. Khi truy cập ứng dụng, bạn sẽ thấy trang chủ với form tải ảnh lên.
2. Nhấn vào nút "Choose File" để chọn ảnh từ máy tính của bạn.
3. Chọn ảnh có chứa khuôn mặt (hỗ trợ định dạng JPG, PNG, JPEG).
4. Nhấn nút "Phân tích cảm xúc" để bắt đầu quá trình nhận diện.

### Trang kết quả

Sau khi xử lý, ứng dụng sẽ hiển thị trang kết quả với:

1. Ảnh gốc bạn đã tải lên.
2. Ảnh đã được xử lý với các khuôn mặt được đánh dấu và gán nhãn cảm xúc.
3. Bảng chi tiết kết quả, hiển thị:
   - Số thứ tự của khuôn mặt
   - Cảm xúc được nhận diện
   - Độ tin cậy của kết quả

Nếu không phát hiện được khuôn mặt nào trong ảnh, ứng dụng sẽ hiển thị thông báo tương ứng.

### Quản lý

Bạn có thể truy cập trang quản lý tại http://127.0.0.1:8000/admin/ với tài khoản admin đã tạo để xem và quản lý các ảnh đã tải lên.

## Cấu trúc thư mục mô hình

Ứng dụng sử dụng các mô hình đã được huấn luyện trước trong thư mục `model_deep/`:
- `cnn.h5`: Mô hình CNN
- `sift.h5`: Mô hình SIFT
- `ds.h5`: Mô hình DSIFT
- `km_sift.joblib`: Mô hình KMeans cho SIFT
- `km_dsift.joblib`: Mô hình KMeans cho DSIFT
- `sc_s.joblib`: Scaler cho SIFT
- `sc_d.joblib`: Scaler cho DSIFT

## Lưu ý

- Ứng dụng hoạt động tốt nhất với ảnh có khuôn mặt nhìn thẳng, đủ ánh sáng và không bị che khuất.
- Thời gian xử lý phụ thuộc vào kích thước ảnh và số lượng khuôn mặt trong ảnh.
- Ứng dụng sử dụng bộ phát hiện khuôn mặt của OpenCV, nên có thể không phát hiện được khuôn mặt khi góc nghiêng nhiều.

## Tùy chỉnh mở rộng

Bạn có thể mở rộng ứng dụng bằng cách:
1. Thêm khả năng xử lý video
2. Thêm khả năng nhận diện khuôn mặt trực tiếp qua webcam
3. Thêm khả năng nhận diện cảm xúc từ URL ảnh trực tuyến

## Hỗ trợ

Nếu bạn gặp vấn đề trong quá trình cài đặt hoặc sử dụng, vui lòng tạo issue trên GitHub hoặc liên hệ qua email.
