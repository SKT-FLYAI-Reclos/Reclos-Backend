from django.db import models

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=100, null = False, blank = False)
    content = models.TextField(null = False, blank = False)
    image = models.ImageField(upload_to="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey("user.User", on_delete=models.CASCADE)
    
    class Meta:
        ordering = ("-created_at",)