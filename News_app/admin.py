from django.contrib import admin
from .models import NewsItem, Tag, Source


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

class SourceAdmin(admin.ModelAdmin):
    list_display = ('url',)


admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(Tag)
admin.site.register(Source, SourceAdmin)
