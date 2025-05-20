# Facial Emotion Recognition

Một dự án Machine Learning nhận diện cảm xúc từ khuôn mặt người dùng mô hình học sâu kết hợp CNN-SIFT. Dự án bao gồm phần huấn luyện mô hình và ứng dụng web Django để nhận diện cảm xúc theo thời gian thực.

## Tổng quan

Dự án này sử dụng các kỹ thuật học máy để nhận diện bảy cảm xúc cơ bản:
- Giận dữ (Anger)
- Khinh miệt (Contempt)
- Ghê tởm (Disgust)
- Sợ hãi (Fear)
- Vui vẻ (Happy)
- Buồn bã (Sad)
- Ngạc nhiên (Surprise)

Hệ thống sử dụng phương pháp mô hình hybrid kết hợp Convolutional Neural Networks (CNN), Scale-Invariant Feature Transform (SIFT), và Dense SIFT (DSIFT) để đạt độ chính xác cao trong nhận diện cảm xúc khuôn mặt trong các điều kiện ánh sáng và góc độ khác nhau.

## Cấu trúc dự án

```
Facial-Emotion-Recognition/
├── demo.ipynb               # Jupyter notebook demo tương tác với webcam
├── model.ipynb              # Notebook huấn luyện và đánh giá mô hình
├── model_deep/              # Thư mục chứa các mô hình đã huấn luyện
│   ├── cnn.h5               # Mô hình CNN 
│   ├── sift.h5              # Mô hình SIFT
│   ├── dsift.h5             # Mô hình DSIFT
│   ├── km_sift.joblib       # KMeans cho đặc trưng SIFT
│   ├── km_dsift.joblib      # KMeans cho đặc trưng DSIFT
│   ├── sc_s.joblib          # Scaler cho đặc trưng SIFT
│   └── sc_d.joblib          # Scaler cho đặc trưng DSIFT
├── media/                   # Ảnh và video mẫu
└── emotion_recognition/     # Ứng dụng web Django
    ├── face_emotion/        # Mã nguồn chính của ứng dụng
    ├── static/              # Tệp tĩnh (CSS, JS)
    ├── media/               # Thư mục lưu files tải lên và kết quả xử lý
    ├── templates/           # Các mẫu HTML
    ├── manage.py            # Script quản lý Django
    ├── requirements.txt     # Các thư viện Python cần thiết
    └── run_app.bat          # File batch để chạy ứng dụng (cho Windows)
```

## Các tính năng

- **Nhận diện cảm xúc từ ảnh**: Tải lên ảnh chứa khuôn mặt và nhận kết quả dự đoán cảm xúc
- **Xử lý video**: Tải lên video để phân tích cảm xúc theo từng khung hình
- **Phân tích trực tiếp từ webcam**: Nhận diện cảm xúc theo thời gian thực từ webcam
- **Mô hình hybrid**: Kết hợp CNN, SIFT và DSIFT để cải thiện độ chính xác
- **Giao diện thân thiện**: UI rõ ràng, dễ sử dụng

## Công nghệ sử dụng

- **Python 3.8+**
- **TensorFlow 2.19+**: Triển khai mô hình CNN
- **OpenCV 4.11+**: Xử lý ảnh và phát hiện khuôn mặt
- **Scikit-learn 1.6+**: Các thành phần học máy
- **Django 5.2+**: Framework ứng dụng web
- **NumPy 2.1+**: Xử lý số học
- **Pillow 11.2+**: Xử lý ảnh

## Cài đặt

### Yêu cầu

- Python 3.8 trở lên
- Git

### Các bước cài đặt

1. Clone repository:
```bash
git clone https://github.com/nhonhoccode/Facial-Emotion-Recognition.git
cd Facial-Emotion-Recognition
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r emotion_recognition/requirements.txt
```

3. Chuẩn bị ứng dụng Django:
```bash
cd emotion_recognition
python manage.py migrate
```

4. Chạy ứng dụng:
```bash
python manage.py runserver
```

Hoặc với Windows, chỉ cần chạy file `run_app.bat`.

## Cách sử dụng

### Ứng dụng Web

1. Khởi động server Django
2. Truy cập ứng dụng tại http://127.0.0.1:8000/
3. Sử dụng giao diện để:
   - Tải lên ảnh để nhận diện cảm xúc
   - Sử dụng webcam để nhận diện theo thời gian thực
   - Tải lên video để phân tích cảm xúc

### Jupyter Notebooks

Repository bao gồm hai Jupyter notebooks:

- `model.ipynb`: Mô tả quá trình huấn luyện mô hình và đánh giá hiệu suất
- `demo.ipynb`: Cung cấp demo đơn giản về nhận diện cảm xúc theo thời gian thực qua webcam

Để chạy các notebooks:
```bash
jupyter notebook
```

## Chi tiết về mô hình

### Các mô hình Machine Learning được sử dụng

Dự án kết hợp nhiều phương pháp machine learning khác nhau để đạt hiệu quả tối ưu:

1. **KNN (K-Nearest Neighbors)**:
   - Sử dụng scikit-learn's KNeighborsClassifier
   - Tối ưu hóa siêu tham số với GridSearchCV để tìm số neighbors và trọng số tối ưu
   - Đánh giá bằng accuracy và classification report
   - Hiệu suất: Độ chính xác ~85% trên tập dữ liệu CK+

2. **SVM (Support Vector Machine)**:
   - Sử dụng SVC từ scikit-learn với kernel RBF
   - Tối ưu hóa siêu tham số C, kernel và gamma
   - Cài đặt cả phiên bản OneVsRestSVM tùy chỉnh với Mini-Batch Gradient Descent và Momentum
   - Hiệu suất: Độ chính xác ~88-90% trên tập dữ liệu CK+

3. **CNN (Convolutional Neural Network)**: 
   - Mạng neural tích chập gồm 6 lớp tích chập và 2 lớp fully connected
   - Hiệu quả trong việc nắm bắt các đặc trưng không gian trong khuôn mặt
   - Kiến trúc: 3 khối gồm 2 lớp Conv2D, 1 lớp MaxPooling2D và Dropout (0.25)
   - Sử dụng lớp Dense 2048 units với activation ReLU, Dropout (0.5)
   - Lớp đầu ra softmax 7 units tương ứng với 7 cảm xúc
   - Hiệu suất: Độ chính xác ~91% độ chính xác

4. **Hybrid Models**:
   - **CNN + SIFT**: Kết hợp CNN với SIFT features (~93% độ chính xác)
   - **CNN + DSIFT**: Kết hợp CNN với Dense SIFT features (~94% độ chính xác)
   - **Ensemble Hybrid**: Kết hợp cả ba mô hình (~95% độ chính xác)

### Phương pháp trích xuất đặc trưng

Dự án sử dụng nhiều phương pháp trích xuất đặc trưng:

1. **HOG (Histogram of Oriented Gradients)**:
   - Trích xuất thông tin về hướng gradient trong ảnh
   - Cấu hình: 9 orientations, 8x8 pixels per cell, 2x2 cells per block
   - Hiệu quả trong việc mô tả hình dạng và cấu trúc của khuôn mặt

2. **DCT (Discrete Cosine Transform)**:
   - Chuyển đổi không gian ảnh sang không gian tần số
   - Giữ 8x8 hệ số tần số thấp nhất (góc trên bên trái)
   - Hiệu quả trong việc nén thông tin và loại bỏ nhiễu

3. **SIFT (Scale-Invariant Feature Transform)**:
   - Trích xuất đặc trưng bền vững với sự thay đổi về tỷ lệ, ánh sáng và góc độ
   - Sử dụng hai phương pháp:
     - **Regular SIFT**: Phát hiện keypoints tự động trên khuôn mặt
     - **Dense SIFT**: Tạo keypoints trên lưới đều đặn với bước nhảy 12 pixel

4. **Bag of Visual Words (BoW)**:
   - Xây dựng từ điển hình ảnh bằng K-Means (K=2048)
   - Biểu diễn ảnh dưới dạng histogram tần suất xuất hiện của các "visual words"
   - Chuẩn hóa vector đặc trưng với StandardScaler
   - Áp dụng cho cả SIFT và Dense SIFT

### Kỹ thuật tiền xử lý

1. **Face Detection**: Sử dụng Haar Cascade của OpenCV để phát hiện khuôn mặt

2. **Face Alignment**:
   - Sử dụng dlib để phát hiện 68 điểm landmark
   - Xoay và căn chỉnh khuôn mặt dựa trên vị trí của hai mắt

3. **Histogram Equalization**: 
   - Tăng cường độ tương phản của ảnh
   - Làm nổi bật các đặc trưng quan trọng trong các vùng tối hoặc sáng

4. **Data Augmentation**:
   - Lật ngang ảnh
   - Xoay ngẫu nhiên (-30° đến 30°)
   - Cắt ngẫu nhiên từ các vị trí khác nhau
   - Biến đổi affine (thay đổi hình dạng)

5. **Chuẩn hóa và giảm chiều**:
   - Chuẩn hóa đặc trưng với StandardScaler
   - Giảm chiều với PCA, giữ 90-95% phương sai giải thích

### Mô hình kết hợp cuối cùng

Quy trình dự đoán của mô hình đề xuất:

1. Tiền xử lý ảnh đầu vào
2. Phát hiện khuôn mặt sử dụng Haar Cascade
3. Cho mỗi khuôn mặt phát hiện được:
   - Chạy ảnh qua mô hình CNN đơn thuần để có dự đoán thứ nhất
   - Trích xuất đặc trưng SIFT, mã hóa bằng BoW, và kết hợp với CNN cho dự đoán thứ hai
   - Trích xuất đặc trưng Dense SIFT, mã hóa BoW, và kết hợp với CNN cho dự đoán thứ ba
4. Lấy trung bình kết quả của ba mô hình để có dự đoán cuối cùng
5. Gán nhãn cảm xúc và độ tin cậy cho mỗi khuôn mặt

Phương pháp kết hợp này cho phép hệ thống tận dụng điểm mạnh của từng phương pháp, tăng độ chính xác và khả năng chống nhiễu.

## Dữ liệu huấn luyện

Mô hình được huấn luyện trên bộ dữ liệu CK+ (Extended Cohn-Kanade), bao gồm các biểu hiện khuôn mặt được gán nhãn cho bảy cảm xúc mà hệ thống có thể nhận diện. Dữ liệu được tăng cường (augmented) bằng các kỹ thuật:
- Lật ngang ảnh
- Xoay ngẫu nhiên (-30° đến 30°)
- Cắt ngẫu nhiên
- Biến đổi affine

## Hiệu suất

Mô hình đạt được độ chính xác cao trong nhận diện cảm xúc trên tập dữ liệu CK+:
- Mô hình CNN đơn lẻ: ~91% độ chính xác
- Mô hình kết hợp CNN-SIFT: ~93% độ chính xác 
- Mô hình kết hợp CNN-DSIFT: ~94% độ chính xác
- Mô hình kết hợp cuối (ensemble): ~95% độ chính xác

## Cải tiến trong tương lai

- Nâng cao độ chính xác trong điều kiện ánh sáng khó khăn
- Thêm hỗ trợ cho các cảm xúc phức tạp và tinh tế hơn
- Tối ưu hóa xử lý video để đạt hiệu suất tốt hơn
- Triển khai theo dõi cảm xúc theo thời gian
- Thêm hỗ trợ xử lý hàng loạt nhiều ảnh

## Các trường hợp áp dụng

- Các ứng dụng trợ lý ảo tương tác
- Kiểm tra mức độ tương tác của người dùng trong học trực tuyến
- Hệ thống giám sát an ninh
- Nghiên cứu tâm lý và ứng dụng lâm sàng
- Phân tích cảm xúc trong tiếp thị và nghiên cứu thị trường

## Giấy phép

[Thêm thông tin giấy phép của bạn tại đây]

## Người đóng góp

- MAXIMUS_NHON

## Lời cảm ơn

- Nhà cung cấp bộ dữ liệu CK+
- Cộng đồng TensorFlow và OpenCV
- Các bài báo và tài liệu nghiên cứu về nhận diện cảm xúc
- Các thành viên trong nhóm đã hỗ trợ trong quá trình phát triển dự án
```
