from rest_framework import viewsets

from .models import News, Tag
from .serializers import NewsSerializerPost, NewsSerializerList, TagSerializer


class NewsViewset(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializerPost

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return NewsSerializerList
        return NewsSerializerPost


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
