from django.contrib import admin

from .models import Tag, News

class TagAdmin(admin.ModelAdmin):
    pass

class NewsAdmin(admin.ModelAdmin): 
    pass

admin.site.register(Tag, TagAdmin)
admin.site.register(News, NewsAdmin)
