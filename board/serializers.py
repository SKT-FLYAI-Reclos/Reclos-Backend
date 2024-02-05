from rest_framework import serializers
from .models import Board
from user.serializers import UserSerializer

class BoardSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Board
        fields = "__all__"