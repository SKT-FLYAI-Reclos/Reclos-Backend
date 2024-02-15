from django.db import models

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=100, null = False, blank = False)
    content = models.TextField(null = False, blank = False)
    category = models.CharField(max_length=100, null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey("user.User", on_delete=models.CASCADE)
    
    class Meta:
        ordering = ("-created_at",)
        
class Likes(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("user", "board")

class Images(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="", null = False, blank = False)