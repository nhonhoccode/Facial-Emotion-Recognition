from django.http import FileResponse, HttpResponse
import os
from django.conf import settings

def serve_processed_video(request, filename):
    """
    Simple function to directly serve a processed video file by filename
    """
    # Construct the full path to the file
    file_path = os.path.join(settings.MEDIA_ROOT, 'videos', 'processed', filename)
    print(f"[SIMPLE SERVER] Attempting to serve: {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"[SIMPLE SERVER] File not found: {file_path}")
        return HttpResponse(f"Video file not found: {filename}", status=404)
    
    # Set content type based on file extension
    content_type = 'video/mp4' if filename.endswith('.mp4') else 'video/x-msvideo'
    
    # Open the file in binary mode
    try:
        file = open(file_path, 'rb')
        response = FileResponse(file, content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        response['Accept-Ranges'] = 'bytes'
        response['Access-Control-Allow-Origin'] = '*'
        print(f"[SIMPLE SERVER] Successfully serving: {filename} as {content_type}")
        return response
    except Exception as e:
        print(f"[SIMPLE SERVER] Error: {str(e)}")
        return HttpResponse(f"Error opening video file: {str(e)}", status=500)
