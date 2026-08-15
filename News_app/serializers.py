from rest_framework import serializers

from .models import Tag, News


class TagSerializer(serializers.ModelSerializer):
    # label = serializers.CharField()

    class Meta:
        model = Tag
        fields = ('label',)


class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        queryset = Tag.objects.all(), slug_field='label', many=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'date', 'author', 'url', 'tags')
    
