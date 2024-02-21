from rest_framework import serializers
from .models import User, Closet, Level

class ClosetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Closet
        exclude = ["id", "user"]
        
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        exclude = ["id", "user"]

class UserSerializer(serializers.ModelSerializer):
    closets = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}
    
    def get_closets(self, obj):
        closets = Closet.objects.filter(user=obj)
        return ClosetSerializer(closets, many=True).data
    
    def get_level(self, obj):
        level = Level.objects.filter(user=obj)
        return LevelSerializer(level, many=True).data