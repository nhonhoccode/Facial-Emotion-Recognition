from django.http import StreamingHttpResponse, FileResponse, HttpResponse
import os
import mimetypes
import re
from django.conf import settings

def serve_video_file(request, path):
    """
    Serve video files with proper MIME types
    """
    # Log requested path for debugging
    print(f"[DEBUG] Requested video path: {path}")
    print(f"[DEBUG] Full request path: {request.path}")
    print(f"[DEBUG] HTTP method: {request.method}")
    
    # Fix path separators for Windows
    path = path.replace('/', os.path.sep)
    
    # Construct the absolute path - handle both full path and media-relative path
    if os.path.isabs(path):
        full_path = path
    else:
        # Try finding the file in both MEDIA_ROOT locations
        # First in project-level media
        full_path = os.path.join(settings.MEDIA_ROOT, path)
        
        # If not found, try in app-level media within emotion_recognition folder
        if not os.path.exists(full_path):
            alt_path = os.path.join(settings.BASE_DIR, 'media', path)
            if os.path.exists(alt_path):
                full_path = alt_path
    
    print(f"[DEBUG] Constructed full path: {full_path}")
    
    # Check if the path exists
    if not os.path.exists(full_path):
        print(f"[ERROR] Path does not exist: {full_path}")
        # Detailed debugging for path attempts
        print(f"[DEBUG] MEDIA_ROOT is set to: {settings.MEDIA_ROOT}")
        print(f"[DEBUG] BASE_DIR is set to: {settings.BASE_DIR}")
        
        # Try to list contents of parent directory to help debugging
        parent_dir = os.path.dirname(full_path)
        if os.path.exists(parent_dir):
            print(f"[DEBUG] Parent directory exists: {parent_dir}")
            print(f"[DEBUG] Contents of parent directory:")
            for item in os.listdir(parent_dir):
                print(f"  - {item}")
        else:
            print(f"[DEBUG] Parent directory does not exist: {parent_dir}")
            
        return HttpResponse(f"File not found: {path}", status=404)
        
    # Check if it's a file
    if not os.path.isfile(full_path):
        print(f"[ERROR] Path is not a file: {full_path}")
        return HttpResponse(f"Not a file: {path}", status=404)
    
    # Additional check to ensure it's a video file
    _, ext = os.path.splitext(full_path)
    if ext.lower() not in ['.mp4', '.avi', '.mov']:
        print(f"[WARNING] Not a recognized video format: {full_path}")
    
    # Determine the correct MIME type
    content_type = None
    if full_path.endswith('.mp4'):
        content_type = 'video/mp4'
    elif full_path.endswith('.avi'):
        content_type = 'video/x-msvideo'
    else:
        content_type, _ = mimetypes.guess_type(full_path)
          # Safety check - only serve videos
    if not content_type or not content_type.startswith('video/'):
        content_type = 'application/octet-stream'  # Using normal string
    
    print(f"[DEBUG] Serving file with MIME type: {content_type}")
    
    try:
        # Return the file response with the correct MIME type
        response = FileResponse(open(full_path, 'rb'), content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(full_path)}"'
        
        # Add additional headers for better playback
        response['Accept-Ranges'] = 'bytes'
        
        # Enable Cross-Origin Resource Sharing for better browser compatibility
        response['Access-Control-Allow-Origin'] = '*'
        
        # Add Cache-Control headers to improve playback experience
        response['Cache-Control'] = 'public, max-age=3600'
        
        return response
    except Exception as e:
        print(f"[ERROR] Error serving file: {str(e)}")
        return HttpResponse(f"Error serving file: {str(e)}", status=500)
