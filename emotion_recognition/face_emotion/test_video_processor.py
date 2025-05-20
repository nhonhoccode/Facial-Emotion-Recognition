import os
import cv2
import numpy as np
from pathlib import Path

def test_video_processing(input_video_path):
    """Test the video processing functionality without Django dependencies"""
    print(f"Testing video processing with: {input_video_path}")
    
    # Make sure input file exists
    if not os.path.exists(input_video_path):
        print(f"Input file not found: {input_video_path}")
        return False
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(input_video_path), "test_output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up output path
    base_name = os.path.basename(input_video_path)
    output_path = os.path.join(output_dir, f"test_processed_{base_name}")
    
    # Try to open the input video
    cap = cv2.VideoCapture(str(input_video_path))
    if not cap.isOpened():
        print(f"Failed to open input video: {input_video_path}")
        return False
    
    try:
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Try DIVX codec for Windows (most compatible)
        if os.name == 'nt':  # Windows
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            output_path = output_path.replace(os.path.splitext(output_path)[1], '.avi')
            
        else:  # Linux/Mac
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            output_path = output_path.replace(os.path.splitext(output_path)[1], '.avi')
            
        print(f"Creating output video: {output_path}")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        if not out.isOpened():
            print("Failed to create output video writer")
            return False
        
        # Process a few frames
        max_frames = 100  # Process only 100 frames for testing
        frame_count = 0
        
        while cap.isOpened() and frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            
            # Add a simple overlay for testing - draw frame count
            cv2.putText(
                frame, 
                f"Frame: {frame_count}", 
                (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                (0, 255, 0), 
                2
            )
            
            # Write the frame
            out.write(frame)
            
        # Release resources
        cap.release()
        out.release()
        
        # Check if output file was created
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Successfully created output video: {output_path}")
            return True
        else:
            print(f"Output file missing or empty: {output_path}")
            return False
            
    except Exception as e:
        import traceback
        print(f"Error processing video: {str(e)}")
        print(traceback.format_exc())
        cap.release()
        return False

if __name__ == "__main__":
    # Find a video file in the media directory
    media_dir = Path("d:/Year 3_University_Semester II/Project/ML/Facial-Emotion-Recognition/emotion_recognition/media/videos")
    
    # List video files
    video_files = list(media_dir.glob("*.mp4"))
    
    if video_files:
        # Test with the first video file found
        test_video = str(video_files[0])
        print(f"Testing with video: {test_video}")
        test_video_processing(test_video)
    else:
        print("No video files found in the media directory")
