# filepath: d:\Year 3_University_Semester II\Project\ML\Facial-Emotion-Recognition\emotion_recognition\face_emotion\webcam.py
from django.shortcuts import render
import cv2
import numpy as np
import threading
import tempfile
import os
import time
from django.http import StreamingHttpResponse, JsonResponse
from .emotion_detector import EmotionRecognizer
from django.conf import settings

# Initialize the emotion recognizer
MODEL_DIR = os.path.join(settings.BASE_DIR.parent, 'model_deep')
emotion_recognizer = EmotionRecognizer(MODEL_DIR)

class WebcamVideoStream:
    def __init__(self):
        # Try to open the webcam with multiple camera indices if necessary
        self.stream = None
        self.stopped = False
        self.frame = None
        
        # Try camera indices 0, 1, and 2
        for camera_idx in [0, 1, 2]:
            try:
                print(f"Attempting to open camera index {camera_idx}")
                stream = cv2.VideoCapture(camera_idx)
                if stream.isOpened():
                    self.stream = stream
                    self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    print(f"Successfully opened camera index {camera_idx}")
                    break
                else:
                    stream.release()
            except Exception as e:
                print(f"Error opening camera {camera_idx}: {str(e)}")
        
        if self.stream is None:
            print("Could not open any camera")
            # Create a fallback frame with error message
            self.fallback_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(
                self.fallback_frame, 
                "Camera not available", 
                (120, 240), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                (255, 255, 255), 
                2
            )
            self.frame = self.fallback_frame
    
    def start(self):
        if self.stream is None:
            # No need to start a thread if we don't have a camera
            return self
            
        threading.Thread(target=self.update, args=(), daemon=True).start()
        return self
        
    def update(self):
        while not self.stopped and self.stream is not None:
            try:
                (grabbed, frame) = self.stream.read()
                if not grabbed:
                    print("Failed to grab frame from camera")
                    # If we can't get a frame, create a blank one with an error message
                    error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                    cv2.putText(
                        error_frame, 
                        "No camera signal", 
                        (150, 240), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1, 
                        (255, 255, 255), 
                        2
                    )
                    self.frame = error_frame
                    time.sleep(0.5)  # Don't loop too fast
                else:
                    self.frame = frame
            except Exception as e:
                print(f"Error reading frame: {str(e)}")
                time.sleep(0.5)  # Don't loop too fast
    
    def read(self):
        return self.frame
        
    def stop(self):
        self.stopped = True
        if self.stream is not None:
            self.stream.release()
        
webcam_stream = None

def gen_frames():
    """Generate frames with emotion detection"""
    global webcam_stream
    
    try:
        # Create a reusable error frame function
        def get_error_frame(message="No camera frame available"):
            error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(
                error_frame, 
                message, 
                (100, 240), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, 
                (255, 255, 255), 
                2
            )
            ret, buffer = cv2.imencode('.jpg', error_frame)
            frame_bytes = buffer.tobytes()
            return frame_bytes
            
        if webcam_stream is None:
            webcam_stream = WebcamVideoStream().start()
            # Give camera time to initialize
            time.sleep(1)
            
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        names = ["Anger", "Contempt", "Disgust", "Fear", "Happy", "Sad", "Surprise"]
        
        # For FPS calculation
        prev_time = time.time()
        frame_count = 0
        fps = 0
        
        while True:
            # Check if webcam_stream has been stopped
            if webcam_stream is None or webcam_stream.stopped:
                # Return an error frame but don't fail
                frame_bytes = get_error_frame("Camera stopped")
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                time.sleep(0.5)
                continue
                
            try:
                frame = webcam_stream.read()
                if frame is None:
                    # Create an error frame
                    frame_bytes = get_error_frame("No camera frame available")
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                    time.sleep(0.5)
                    continue
                
                # Calculate FPS
                frame_count += 1
                if frame_count >= 10:  # Update FPS every 10 frames
                    current_time = time.time()
                    elapsed = current_time - prev_time
                    if elapsed > 0:
                        fps = frame_count / elapsed
                        prev_time = current_time
                        frame_count = 0
                
                # Process frame for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    try:
                        # Process face
                        roi = cv2.resize(gray[y:y+h, x:x+w], (emotion_recognizer.IMG_SIZE, emotion_recognizer.IMG_SIZE))
                        
                        # Prepare input for CNN
                        c_in = roi[None, ..., None] / 255.
                        
                        # Extract features for SIFT and DSIFT
                        bs = emotion_recognizer.sc_s.transform(
                            emotion_recognizer.bow(emotion_recognizer.km_sift, emotion_recognizer.rsift(roi)).reshape(1, -1)
                        )
                        bd = emotion_recognizer.sc_d.transform(
                            emotion_recognizer.bow(emotion_recognizer.km_dsift, emotion_recognizer.dsift(roi)).reshape(1, -1)
                        )
                        
                        # Ensemble prediction
                        pred = (emotion_recognizer.cnn(c_in, training=False) + 
                                emotion_recognizer.sift([c_in, bs], training=False) +
                                emotion_recognizer.ds([c_in, bd], training=False)) / 3
                                
                        label = names[int(np.argmax(pred))]
                        
                        # Draw rectangle and emotion label
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    except Exception as e:
                        print(f"Error processing face: {str(e)}")
                
                # Add FPS and help text
                cv2.putText(frame, f"FPS: {fps:.1f} | ESC to exit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                # Encode frame as JPEG
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            except Exception as e:
                print(f"Error in frame processing: {str(e)}")
                # Create an error frame
                error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(
                    error_frame, 
                    f"Error: {str(e)}", 
                    (50, 240), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, 
                    (255, 255, 255), 
                    2
                )
                ret, buffer = cv2.imencode('.jpg', error_frame)
                frame_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                time.sleep(1)  # Don't loop too fast on error
    except Exception as e:
        print(f"Error in gen_frames: {str(e)}")
        # Create an error frame
        error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(
            error_frame, 
            f"Camera error: {str(e)}", 
            (50, 240), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.7, 
            (255, 255, 255), 
            2
        )
        ret, buffer = cv2.imencode('.jpg', error_frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def webcam_feed(request):
    """Video streaming route"""
    try:
        return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Error in webcam_feed: {str(e)}")
        # Create a blank response in case of error
        return StreamingHttpResponse(content_type='multipart/x-mixed-replace; boundary=frame')

def stop_webcam(request):
    """Stop the webcam stream"""
    global webcam_stream
    try:
        if webcam_stream:
            # First mark as stopped to prevent new frame captures
            webcam_stream.stopped = True
            
            # Then safely release the camera
            if hasattr(webcam_stream, 'stream') and webcam_stream.stream is not None:
                try:
                    webcam_stream.stream.release()
                except Exception as e:
                    print(f"Error releasing camera stream: {str(e)}")
                
            # Finally set to None
            webcam_stream = None
            print("Webcam stream stopped successfully")
    except Exception as e:
        print(f"Error stopping webcam: {str(e)}")
    return JsonResponse({"status": "success", "message": "Webcam stopped successfully"})

def webcam_view(request):
    """Webcam page"""
    return render(request, 'face_emotion/webcam.html')
