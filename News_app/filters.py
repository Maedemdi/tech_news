from rest_framework import filters
from django.db.models import Q
from django_filters import FilterSet, ModelMultipleChoiceFilter

from . import models


class TagsFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name = 'tags__caption',
        to_field_name = 'caption',
        queryset = models.Tag.objects.all(),
        conjoined = True
        )
    
    class Meta:
        model= models.NewsItem
        fields = ('tags',)



class CustomSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_query = request.query_params.get(self.search_param, '')

        if not search_query:
            return queryset

        include_terms = []
        exclude_terms = []

        terms = search_query.split()
        for term in terms:
            if term.startswith('-'):
                exclude_terms.append(term[1:].lower())
            else:
                include_terms.append(term.lower())

        # Initialize queries
        include_query = Q()
        exclude_query = Q()

        for term in include_terms:
            include_query |= Q(title__icontains=term) | Q(text__icontains=term)
        for term in exclude_terms:
            exclude_query |= Q(title__icontains=term) | Q(text__icontains=term)

        if include_terms:
            queryset = queryset.filter(include_query)
        if exclude_terms:
            queryset = queryset.exclude(exclude_query)

        return queryset