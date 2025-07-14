from rest_framework import serializers

from . import models


class TagSerializer(serializers.ModelSerializer):
    """Handles the serialization of the Tag model instances"""
    class Meta:
        model = models.Tag
        fields = ['id', 'caption']


class NewsItemSerializer(serializers.ModelSerializer):
    """Handles the serialization of the Tag model instances"""
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = models.NewsItem
        fields = '__all__' 


