from rest_framework import serializers
from .models import Board, Image, Like
from user.serializers import UserSerializer

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ["id", "board"]

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ["id", "board"]

class BoardSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = "__all__"
    
    def get_image(self, obj):
        images = obj.image.all()
        return ImageSerializer(images, many=True).data
    
    def get_like(self, obj):
        return [like.user.username for like in obj.like.all()]
