from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class ImageRemoveBackground(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='remove_bg_requests')
    image = models.ImageField(upload_to='imgen/remove_bg/')
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
class ImageLadiVton(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ladi_vton_requests')
    category = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='imgen/ladi_vton/')
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)