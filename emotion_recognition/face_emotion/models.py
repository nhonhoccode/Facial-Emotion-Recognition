from django.db import models
import os
import uuid

# Create your models here.
class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image {self.id} uploaded at {self.uploaded_at}"
        
    def filename(self):
        return os.path.basename(self.image.name)
