# filepath: d:\Year 3_University_Semester II\Project\ML\Facial-Emotion-Recognition\emotion_recognition\face_emotion\urls.py
from django.urls import path, re_path
from . import views
from .webcam_new import webcam_view, webcam_feed, stop_webcam
from .video_processor import video_upload_view, process_video
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.home, name='home'),
    path('detect/', views.detect_emotion, name='detect_emotion'),
    path('detect_image/<str:filename>/', views.show_result, name='show_result'),
    # Webcam routes
    path('webcam/', webcam_view, name='webcam'),
    path('webcam/feed/', webcam_feed, name='webcam_feed'),
    path('webcam/stop/', stop_webcam, name='stop_webcam'),
    # Video processing routes
    path('video/', video_upload_view, name='video_upload'),
    path('video/process/', process_video, name='process_video'),
    # Remove custom video serving route as it's now handled by the main urls.py
]
