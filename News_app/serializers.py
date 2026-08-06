from rest_framework import serializers

from .models import Tag, News


class TagSerializer(serializers.ModelSerializer):
    # label = serializers.CharField()

    class Meta:
        model = Tag
        fields = ('label',)


class NewsSerializerList(serializers.ModelSerializer):
    # title = serializers.CharField(max_length=70)
    # content = serializers.CharField(max_length=None)
    # date = serializers.DateField()
    # author = serializers.CharField(max_length=100)
    # url = serializers.URLField()
    tags = serializers.SlugRelatedField(
        slug_field='label', read_only = True, many=True)

    class Meta:
        model = News
        fields = ('title', 'content', 'date', 'author', 'url', 'tags')

class NewsSerializerPost(serializers.ModelSerializer):
    # title = serializers.CharField(max_length=70)
    # content = serializers.CharField(max_length=None)
    # date = serializers.DateField()
    # author = serializers.CharField(max_length=100)
    # url = serializers.URLField()
    # tags = serializers.SlugRelatedField(
    #     slug_field='label', query_set=Tag.objects.all(), many=True)

    class Meta:
        model = News
        fields = ('title', 'content', 'date', 'author', 'url', 'tags')