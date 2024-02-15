from rest_framework import serializers
from .models import Board, Images, Likes
from user.serializers import UserSerializer

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['image']
        
class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['user']
        
class BoardSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    images = ImagesSerializer(many=True, read_only=True)
    Likes = LikesSerializer(many=True, read_only=True)
    
    class Meta:
        model = Board
        fields = "__all__"
