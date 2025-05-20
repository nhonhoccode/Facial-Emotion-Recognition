from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from .forms import ImageUploadForm
from .models import UploadedImage
from .emotion_detector import EmotionRecognizer
import os
import cv2
import tempfile

# Initialize the emotion recognizer with the path to our model files
MODEL_DIR = os.path.join(settings.BASE_DIR.parent, 'model_deep')
emotion_recognizer = EmotionRecognizer(MODEL_DIR)

def home(request):
    """Homepage with image upload form"""
    form = ImageUploadForm()
    return render(request, 'face_emotion/home.html', {'form': form})

def detect_emotion(request):
    """Process the uploaded image and detect emotions"""
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image
            uploaded_image = form.save()
            
            # Get the image path
            image_path = uploaded_image.image.path
            
            # Redirect to the result page
            return redirect('show_result', filename=uploaded_image.filename())
    else:
        form = ImageUploadForm()
    
    return render(request, 'face_emotion/home.html', {'form': form})

def show_result(request, filename):
    """Display the results of emotion detection"""
    # Find the uploaded image record
    try:
        image = UploadedImage.objects.filter(image__contains=filename).first()
        if not image:
            return redirect('home')
        
        image_path = image.image.path
        
        # Perform emotion detection
        result_img, results = emotion_recognizer.detect_emotions(image_path)
        
        # Create a path for the annotated image
        result_filename = f"result_{os.path.basename(image_path)}"
        result_path = os.path.join(settings.MEDIA_ROOT, result_filename)
        
        # Save the annotated image
        cv2.imwrite(result_path, result_img)
        
        # Get the URL for the annotated image
        result_url = f"{settings.MEDIA_URL}{result_filename}"
        
        # Prepare the context for the template
        context = {
            'original_image': image.image.url,
            'result_image': result_url,
            'results': results,
            'no_face': len(results) == 0
        }
        
        return render(request, 'face_emotion/result.html', context)
    
    except Exception as e:
        return render(request, 'face_emotion/error.html', {'error': str(e)})
models_dir = os.path.join(settings.BASE_DIR.parent, 'model_deep')
emotion_recognizer = EmotionRecognizer(models_dir)

def home(request):
    """Home page view with upload form"""
    form = ImageUploadForm()
    return render(request, 'face_emotion/home.html', {'form': form})

def detect_emotion(request):
    """Handle image upload and emotion detection"""
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image
            image_obj = form.save()
            
            # Get the image path
            image_path = image_obj.image.path
            
            return redirect('show_result', filename=image_obj.filename())
    
    return redirect('home')

def show_result(request, filename):
    """Display the result of emotion detection"""
    # Find the uploaded image
    image = UploadedImage.objects.filter(image__contains=filename).first()
    
    if not image:
        return HttpResponse("Image not found", status=404)
    
    # Process the image
    image_path = image.image.path
    processed_img, results = emotion_recognizer.detect_emotions(image_path)
    
    if processed_img is None:
        return HttpResponse("Failed to process image", status=500)
    
    # Save the processed image with annotations
    result_dir = os.path.join(settings.MEDIA_ROOT, 'results')
    os.makedirs(result_dir, exist_ok=True)
    
    result_filename = f"result_{filename}"
    result_path = os.path.join(result_dir, result_filename)
    
    cv2.imwrite(result_path, processed_img)
    
    # Prepare result for the template
    result_url = os.path.join(settings.MEDIA_URL, 'results', result_filename)
    
    context = {
        'original_image': image.image.url,
        'result_image': result_url,
        'results': results,
        'filename': filename
    }
    
    return render(request, 'face_emotion/result.html', context)
