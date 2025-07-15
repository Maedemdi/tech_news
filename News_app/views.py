from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from . import models, serializers, filters


class NewsItemViewSet(viewsets.ModelViewSet):
    """ Handles visiting and searching among news """
    queryset = models.NewsItem.objects.all()
    serializer_class = serializers.NewsItemSerializer
    filter_backends = (DjangoFilterBackend, filters.CustomSearchFilter,)
    filterset_class = filters.TagsFilter
    search_fields = ('title', 'text')