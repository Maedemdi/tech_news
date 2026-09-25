<<<<<<< HEAD


=======
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import News, Tag
from .serializers import NewsSerializer, TagSerializer
from .filters import NewsFilter


class NewsViewset(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = NewsFilter


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
>>>>>>> Challenge-1
