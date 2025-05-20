import cv2
import numpy as np
import tensorflow as tf
import joblib
import os

class EmotionRecognizer:
    def __init__(self, models_dir):
        self.IMG_SIZE = 48
        self.DICT_SIZE = 2048
        self.models_dir = models_dir
        
        # Load pre-trained models
        self.cnn = tf.keras.models.load_model(os.path.join(models_dir, "cnn.h5"))
        self.sift = tf.keras.models.load_model(os.path.join(models_dir, "sift.h5"))
        self.ds = tf.keras.models.load_model(os.path.join(models_dir, "dsift.h5"))
        
        # Load KMeans and Scaler models
        self.km_sift = joblib.load(os.path.join(models_dir, "km_sift.joblib"))
        self.km_dsift = joblib.load(os.path.join(models_dir, "km_dsift.joblib"))
        self.sc_s = joblib.load(os.path.join(models_dir, "sc_s.joblib"))
        self.sc_d = joblib.load(os.path.join(models_dir, "sc_d.joblib"))
        
        # Initialize SIFT extractor
        self.sift_extractor = cv2.SIFT_create()
        
        # Define emotion labels
        self.emotion_labels = ["Anger", "Contempt", "Disgust", "Fear", "Happy", "Sad", "Surprise"]
    
    def rsift(self, gray):
        kps = self.sift_extractor.detect((gray*255).astype("uint8"), None)
        _, d = self.sift_extractor.compute((gray*255).astype("uint8"), kps)
        return d
    
    def dsift(self, gray):
        step = 12
        kps = [cv2.KeyPoint(x, y, 12) for y in range(0, self.IMG_SIZE, step) 
               for x in range(0, self.IMG_SIZE, step)]
        _, d = self.sift_extractor.compute((gray*255).astype("uint8"), kps)
        return d
    
    def bow(self, km, desc):
        if desc is None: 
            return np.zeros(self.DICT_SIZE, "float32")
        h = np.bincount(km.predict(desc), minlength=self.DICT_SIZE).astype("float32")
        return h / (h.sum() + 1e-6)
    
    def detect_emotions(self, image_path):
        """
        Detect emotions in an image and return annotated image and results
        """
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            return None, {"error": "Could not read image"}
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        results = []
        
        # Process each detected face
        for (x, y, w, h) in faces:
            # Extract and resize face region
            face_roi = cv2.resize(gray[y:y+h, x:x+w], (self.IMG_SIZE, self.IMG_SIZE))
            
            # Prepare input for CNN
            c_in = face_roi[None, ..., None] / 255.
            
            # Extract features for SIFT and DSIFT
            bs = self.sc_s.transform(self.bow(self.km_sift, self.rsift(face_roi)).reshape(1, -1))
            bd = self.sc_d.transform(self.bow(self.km_dsift, self.dsift(face_roi)).reshape(1, -1))
            
            # Ensemble prediction
            pred = (self.cnn(c_in, training=False) + 
                    self.sift([c_in, bs], training=False) +
                    self.ds([c_in, bd], training=False)) / 3
            
            # Get the predicted emotion label
            emotion_idx = int(np.argmax(pred))
            emotion = self.emotion_labels[emotion_idx]
            confidence = float(pred[0][emotion_idx])
            
            # Draw rectangle and label on the image
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            results.append({
                "position": (x, y, w, h),
                "emotion": emotion,
                "confidence": confidence
            })
        
        return img, results
