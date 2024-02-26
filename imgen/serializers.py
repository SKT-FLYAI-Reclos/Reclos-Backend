from rest_framework import serializers
from .models import ImageRemoveBackground, ImageLadiVton

class ImageRemoveBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageRemoveBackground
        fields = '__all__'
        read_only_fields = ('created_at',)

class ImageLadiVtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageLadiVton
        fields = '__all__'
        read_only_fields = ('created_at',)
