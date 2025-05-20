# Facial Emotion Recognition Django Application

This Django application uses a pre-trained hybrid CNN-SIFT model to detect and recognize emotions in facial images.

## Features

- Upload images and detect faces with emotion recognition
- Uses a hybrid CNN-SIFT model for improved accuracy
- Display results with annotated images
- Clean and responsive UI

## Requirements

- Python 3.8+
- Django 5.2+
- TensorFlow 2.19+
- OpenCV 4.11+
- Scikit-learn 1.6+
- NumPy 2.1+
- Pillow 11.2+

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Facial-Emotion-Recognition
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
cd emotion_recognition
python manage.py migrate
```

4. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

## Running the Application

Start the Django development server:
```bash
python manage.py runserver
```

Access the application at: http://127.0.0.1:8000/

## Admin Interface

The admin interface is available at: http://127.0.0.1:8000/admin

## Model Directory Structure

The application expects pre-trained models in the `model_deep/` directory:
- `cnn.h5`: CNN model
- `sift.h5`: SIFT model
- `ds.h5`: DSIFT model
- `km_sift.joblib`: KMeans model for SIFT
- `km_dsift.joblib`: KMeans model for DSIFT
- `sc_s.joblib`: Scaler for SIFT
- `sc_d.joblib`: Scaler for DSIFT

## Usage

1. Navigate to the home page
2. Upload an image containing one or more faces
3. The system will process the image and display the detected emotions
4. View the results with emotion labels

## License

[Add your license information here]
