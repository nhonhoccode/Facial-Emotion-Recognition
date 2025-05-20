import os
import cv2
import time
import numpy as np
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .emotion_detector import EmotionRecognizer

# Initialize the emotion recognizer
MODEL_DIR = os.path.join(settings.BASE_DIR.parent, 'model_deep')
emotion_recognizer = EmotionRecognizer(MODEL_DIR)

def video_upload_view(request):
    """Display video upload form"""
    return render(request, 'face_emotion/video_upload.html')

def process_video(request):
    """Process uploaded video for emotion detection"""
    if request.method == 'POST' and request.FILES.get('video'):
        # Get the uploaded file
        video_file = request.FILES['video']
        
        # Save the file to media folder
        fs = FileSystemStorage()
        filename = fs.save(f"videos/{video_file.name}", video_file)
        video_path = fs.path(filename)        
        # Process the video
        output_path = process_video_file(video_path)
        
        if output_path:            # Get the output video URL - make sure it's relative to MEDIA_ROOT
            # Use our new simple URL pattern that bypasses media serving
            video_filename = os.path.basename(output_path)
            output_url = f"/videos/processed/{video_filename}"
            
            print(f"Video processing complete. Using direct URL: {output_url}")
            
            context = {
                'video_url': output_url,
                'original_name': video_file.name,
                # Add an additional direct download URL to improve compatibility
                'download_url': output_url,
                # Add MIME type for the video
                'mime_type': 'video/mp4' if output_path.endswith('.mp4') else 'video/x-msvideo'
            }
            
            return render(request, 'face_emotion/video_result.html', context)
        else:
            return render(request, 'face_emotion/error.html', {
                'error': 'Không thể xử lý video. Vui lòng thử lại với video khác.'
            })
    
    return redirect('video_upload')

def process_video_file(video_path):
    """Process video file and return path to the output video"""
    try:
        # Make sure the videos directory exists
        output_dir = os.path.join(settings.MEDIA_ROOT, 'videos', 'processed')
        os.makedirs(output_dir, exist_ok=True)
        
        # Create output filename
        base_name = os.path.basename(video_path)
        output_path = os.path.join(output_dir, f"processed_{base_name}")
        
        print(f"Input video path: {video_path}")
        print(f"Output video path: {output_path}")
        
        # Open the video
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            print(f"Couldn't open video: {video_path}")
            return None        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)        # Create video writer with a more compatible codec - try many web-friendly options
        output_ext = os.path.splitext(output_path)[1].lower()
        
        # For better web playback compatibility, prioritize MP4 formats
        codec_attempts = []
        
        # Add codec options in order of preference for web compatibility
        if os.name == 'nt':  # Windows
            codec_attempts = [
                ('avc1', '.mp4'),  # H.264 AVC - most compatible with browsers
                ('mp4v', '.mp4'),  # MP4V codec - good compatibility
                ('h264', '.mp4'),  # H264 codec - good compatibility
                ('divx', '.avi'),  # DIVX - fallback for Windows
                ('xvid', '.avi'),  # XVID - another fallback
                ('mjpg', '.avi')   # Motion JPEG
            ]
        else:  # Linux/Mac
            codec_attempts = [
                ('avc1', '.mp4'),  # H.264 AVC - most compatible with browsers
                ('mp4v', '.mp4'),  # MP4V codec
                ('h264', '.mp4'),  # H264 codec
                ('xvid', '.avi'),  # XVID - Linux compatible
                ('mjpg', '.avi')   # Motion JPEG - widely supported
            ]
        
        # Try codecs in order until one works
        out = None
        for codec, ext in codec_attempts:
            try:
                # Try this codec
                output_path_temp = output_path.replace(output_ext, ext)
                if codec == 'avc1':
                    # Special handling for H.264 AVC codec
                    fourcc = cv2.VideoWriter_fourcc(*'avc1')
                else:
                    fourcc = cv2.VideoWriter_fourcc(*codec)
                
                out = cv2.VideoWriter(output_path_temp, fourcc, fps, (width, height))
                
                # Test if the writer opened successfully
                if out.isOpened():
                    output_path = output_path_temp
                    print(f"Using {codec} codec with {ext} extension - good web compatibility")
                    break
                else:
                    out.release()
                    print(f"Codec {codec} opened but failed verification")
            except Exception as e:
                print(f"Codec {codec} failed: {str(e)}")
                if out:
                    out.release()
                    out = None
                    
        # Last resort if all previous attempts failed
        if not out or not out.isOpened():
            print("All codecs failed, trying uncompressed AVI...")
            output_path = output_path.replace(output_ext, '.avi')
            fourcc = 0  # Uncompressed
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        print(f"Using final output path: {output_path}")
        
        if not out or not out.isOpened():
            print("Could not open output video writer")
            return None
        
        names = ["Anger", "Contempt", "Disgust", "Fear", "Happy", "Sad", "Surprise"]
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        frame_count = 0
        processed_time = time.time()
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            
            # Process every other frame for speed (adjust as needed)
            if frame_count % 2 != 0:
                out.write(frame)
                continue
                
            # Process for emotion detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                roi = cv2.resize(gray[y:y+h, x:x+w], (emotion_recognizer.IMG_SIZE, emotion_recognizer.IMG_SIZE))
                c_in = roi[None, ..., None] / 255.
                
                bs = emotion_recognizer.sc_s.transform(
                    emotion_recognizer.bow(emotion_recognizer.km_sift, emotion_recognizer.rsift(roi)).reshape(1, -1)
                )
                bd = emotion_recognizer.sc_d.transform(
                    emotion_recognizer.bow(emotion_recognizer.km_dsift, emotion_recognizer.dsift(roi)).reshape(1, -1)
                )
                
                p = (emotion_recognizer.cnn(c_in, training=False) + 
                     emotion_recognizer.sift([c_in, bs], training=False) +
                     emotion_recognizer.ds([c_in, bd], training=False)) / 3
                     
                label = names[int(np.argmax(p))]
                
                # Draw rectangle and label
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # Calculate and display FPS
            current_time = time.time()
            elapsed = current_time - processed_time
            processed_time = current_time
            
            if elapsed > 0:
                processing_fps = 1.0 / elapsed
                cv2.putText(frame, f"{processing_fps:.1f} FPS", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
              # Write the frame
            out.write(frame)
            
        # Release resources
        cap.release()
        out.release()
        
        # Verify the output file was created successfully
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Video processed successfully: {output_path}")
            return output_path
        else:
            print(f"Output video file missing or empty: {output_path}")
            return None
    
    except Exception as e:
        import traceback
        print(f"Error processing video: {str(e)}")
        print(traceback.format_exc())
        return None
