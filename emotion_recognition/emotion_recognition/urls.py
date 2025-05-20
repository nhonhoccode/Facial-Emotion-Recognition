"""
URL configuration for emotion_recognition project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from face_emotion.video_serve import serve_video_file
from face_emotion.direct_file_serve import serve_direct_file
from face_emotion.simple_video_server import serve_processed_video

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("face_emotion.urls")),
    # Simple direct route to serve processed videos by filename
    path("videos/processed/<str:filename>", serve_processed_video, name="serve_processed_video"),
]

# For other static files, use Django's built-in static file server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

