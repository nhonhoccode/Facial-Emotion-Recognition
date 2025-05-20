# Ứng dụng Nhận Diện Cảm Xúc Khuôn Mặt

Ứng dụng Django cho phép nhận diện cảm xúc khuôn mặt sử dụng mô hình học máy hybrid CNN-SIFT.

## Các tính năng chính

### 1. Nhận diện cảm xúc từ ảnh tải lên
- Tải lên ảnh có chứa khuôn mặt
- Phát hiện các khuôn mặt trong ảnh
- Nhận diện cảm xúc cho từng khuôn mặt
- Hiển thị kết quả với ảnh đã được đánh dấu

### 2. Nhận diện cảm xúc theo thời gian thực qua webcam
- Sử dụng webcam của máy tính
- Phát hiện khuôn mặt và nhận diện cảm xúc theo thời gian thực
- Hiển thị kết quả trực tiếp trên video stream

### 3. Xử lý video
- Tải lên video có chứa khuôn mặt
- Xử lý video để phát hiện và nhận diện cảm xúc
- Tạo video mới với các khuôn mặt được đánh dấu và gán nhãn cảm xúc

## Công nghệ sử dụng

- **Backend**: Django 5.2
- **Xử lý ảnh**: OpenCV 4.11
- **Mô hình học máy**: TensorFlow 2.19, Scikit-learn 1.6
- **Frontend**: Bootstrap 5

## Cách cài đặt và chạy ứng dụng

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

2. Chạy các migrations:
```bash
python manage.py migrate
```

3. Chạy ứng dụng:
```bash
python manage.py runserver
```

Hoặc sử dụng file `run_app.bat` để chạy nhanh ứng dụng (Windows).

## Mô hình nhận diện cảm xúc

Ứng dụng sử dụng mô hình hybrid kết hợp:
- CNN (Convolutional Neural Network)
- SIFT (Scale-Invariant Feature Transform)
- Dense SIFT

Kết hợp 3 mô hình này giúp tăng độ chính xác trong việc nhận diện cảm xúc, đặc biệt trong các điều kiện ánh sáng và góc độ khác nhau.

Các cảm xúc được nhận diện:
1. Giận dữ (Anger)
2. Khinh miệt (Contempt)
3. Ghê tởm (Disgust)
4. Sợ hãi (Fear)
5. Vui vẻ (Happy)
6. Buồn bã (Sad)
7. Ngạc nhiên (Surprise)

## Lưu ý

- Ứng dụng hoạt động tốt nhất với ảnh/video có khuôn mặt nhìn thẳng, đủ ánh sáng.
- Xử lý video có thể mất thời gian tùy thuộc vào độ dài và độ phức tạp của video.
- Webcam sẽ hoạt động trên trình duyệt hỗ trợ webcam và có cấp quyền truy cập.

## Phát triển trong tương lai

- Cải thiện độ chính xác của mô hình
- Hỗ trợ nhận diện nhiều cảm xúc phức tạp hơn
- Tối ưu hiệu suất xử lý video
- Thêm tính năng theo dõi cảm xúc theo thời gian
