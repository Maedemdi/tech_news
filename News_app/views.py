from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import News, Tag
from .serializers import NewsSerializerPost, NewsSerializerList, TagSerializer
from .filters import NewsFilter


class NewsViewset(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializerPost
    filter_backends = [DjangoFilterBackend,]
    filterset_class = NewsFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return NewsSerializerList
        return NewsSerializerPost


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
