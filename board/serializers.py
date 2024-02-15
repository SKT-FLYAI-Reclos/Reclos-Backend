from rest_framework import serializers
from .models import Board, Images, Likes
from user.serializers import UserSerializer
        
class BoardSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = "__all__"
    
    def get_images(self, obj):
        return [image.image.url for image in obj.images.all()]
    
    def get_likes(self, obj):
        return [like.user.username for like in obj.likes.all()]
