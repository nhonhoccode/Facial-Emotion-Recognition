from django.http import FileResponse, HttpResponse
import os
import mimetypes
from django.conf import settings

def serve_direct_file(request, file_path):
    """
    Serve a file directly using FileResponse
    This function bypasses the usual Django file serving mechanisms
    and is intended only for development use.
    """
    # Log what we're trying to serve
    print(f"[DIRECT SERVE] Attempting to serve: {file_path}")
    
    # Construct the absolute path
    abs_path = os.path.join(settings.MEDIA_ROOT, file_path)
    print(f"[DIRECT SERVE] Absolute path: {abs_path}")
    
    # Check if file exists
    if not os.path.exists(abs_path):
        print(f"[DIRECT SERVE] File not found: {abs_path}")
        return HttpResponse(f"File not found: {file_path}", status=404)
    
    # Determine the content type
    content_type, encoding = mimetypes.guess_type(abs_path)
    if content_type is None and file_path.endswith('.mp4'):
        content_type = 'video/mp4'
    elif content_type is None and file_path.endswith('.avi'):
        content_type = 'video/x-msvideo'
    
    print(f"[DIRECT SERVE] Serving with content type: {content_type}")
    
    # Open the file and serve it
    try:
        file = open(abs_path, 'rb')
        response = FileResponse(file, content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
        response['Accept-Ranges'] = 'bytes'
        
        # Add CORS headers for better compatibility
        response['Access-Control-Allow-Origin'] = '*'
        
        return response
    except Exception as e:
        print(f"[DIRECT SERVE] Error: {str(e)}")
        return HttpResponse(f"Error serving file: {str(e)}", status=500)
