from django.db import models

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=100, null = False, blank = False)
    content = models.TextField(null = False, blank = False)
    category = models.CharField(max_length=100)
    author = models.ForeignKey("user.User", on_delete=models.CASCADE)
    price = models.IntegerField(default=0, null = False, blank = False)
    gender = models.CharField(max_length=100, default="not-set")
    size = models.CharField(max_length=100, default="not-set")
    esg_water = models.IntegerField(default=0)
    esg_co2 = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ("-created_at",)
        
        
class Like(models.Model):
    board = models.ForeignKey(Board, related_name = 'likes', on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("user", "board")
        
        
class Image(models.Model):
    board = models.ForeignKey(Board, related_name = 'images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="", null = False, blank = False)
    reference_id = models.CharField(max_length=100, null = True, blank = True)
    kind = models.CharField(max_length=100, null = False, blank = False)