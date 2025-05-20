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
        
        if output_path:
            # Get the output video URL - make sure it's relative to MEDIA_ROOT
            media_root_path = os.path.abspath(settings.MEDIA_ROOT)
            output_abs_path = os.path.abspath(output_path)
            
            # Ensure the path is relative to MEDIA_ROOT
            if output_abs_path.startswith(media_root_path):
                rel_path = os.path.relpath(output_abs_path, media_root_path)
                # Replace backslashes with forward slashes for URL
                rel_path = rel_path.replace('\\', '/')
                output_url = settings.MEDIA_URL + rel_path
            else:
                # Fallback if path is outside MEDIA_ROOT
                output_url = settings.MEDIA_URL + 'videos/processed/' + os.path.basename(output_path)
            
            print(f"Video processing complete. Output URL: {output_url}")
            
            # Return the processed video page
            context = {
                'video_url': output_url,
                'original_name': video_file.name,
                # Add an additional direct download URL to improve compatibility
                'download_url': output_url
            }
            
            return render(request, 'face_emotion/video_result.html', context)
        else:
            return render(request, 'face_emotion/error.html', {
                'error': 'Không thể xử lý video. Vui lòng thử lại với video khác.'
            })
    
    return redirect('video_upload')
