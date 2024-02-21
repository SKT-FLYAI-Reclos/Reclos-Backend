from rest_framework import serializers
from .models import Board, Images, Likes
from user.serializers import UserSerializer

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        exclude = ["id", "board"]

class BoardSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = "__all__"
    
    def get_images(self, obj):
        images = Images.objects.filter(board=obj)
        return ImagesSerializer(images, many=True).data
    
    def get_likes(self, obj):
        return [like.user.username for like in obj.likes.all()]
