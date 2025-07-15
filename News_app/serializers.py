from rest_framework import serializers

from . import models


class TagSerializer(serializers.ModelSerializer):
    """Handles the serialization of the Tag model instances"""
    class Meta:
        model = models.Tag
        fields = ['id', 'caption']


class NewsItemSerializer(serializers.ModelSerializer):
    """Handles the serialization of the Tag model instances"""
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.Tag.objects.all()
    )
    class Meta:
        model = models.NewsItem
        fields = ('id', 'title', 'text', 'tags', 'source')


