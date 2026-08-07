import django_filters

from . import models


class NewsFilter(django_filters.FilterSet):
    included_word = django_filters.CharFilter(method='news_inclusion', label = 'Display content including:')
    excluded_word = django_filters.CharFilter(method='news_exclusion', label= 'Display content excluding:')

    class Meta:
        model = models.News
        fields = ['tags']

    def news_inclusion(self, queryset, name, value):
        name = 'Display content including:'
        return queryset.filter(content__icontains=value)

    def news_exclusion(self, queryset, name, value):
        name = 'Display content excluding:'
        return queryset.exclude(content__icontains=value)
