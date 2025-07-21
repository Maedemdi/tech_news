import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechNews_project.settings')

import django
django.setup()

    
from News_app.models import NewsItem, Tag, Source

# class SaveNewsToDBPipeline:
#     def process_item(self, item, spider):
        
#         source_item = Source.objects.create(
#             name = "Zoomit.ir",
#             url = item['source']
#         )

#         news_item = NewsItem.objects.create(
#                     title=item['title'],
#                     content=item['content'],
#                     created_at = item['created_at'],
#                     source = source_item
#                 )
        
#         for tag in item['tags']:
#             tag_item = Tag.objects.create(
#                 caption = tag
#             )
#             news_item.tag.add(tag_item)

#         return item
        
from django.db import close_old_connections
from twisted.internet.threads import deferToThread
from twisted.internet.defer import inlineCallbacks

class SaveNewsToDBPipeline:

    def __init__(self):
        self.existing_urls = set()

    @inlineCallbacks
    def open_spider(self, spider):
        close_old_connections()
        self.existing_urls = yield deferToThread(self._load_existing_urls)

    def _load_existing_urls(self):
        return set(NewsItem.objects.values_list('source__url', flat=True)) 

    def process_item(self, item, spider):
        return deferToThread(self._save_to_db, item)

    def _save_to_db(self, item):

        if item['source'] in self.existing_urls:
            return "The remaining items were previously saved."
        

        source_item,_=Source.objects.get_or_create(
            name="Zoomit.ir",
            url=item['source']
        )
        news_item = NewsItem.objects.create(
            title=item['title'],
            text=item['text'],
            created_at=item['created_at'],
            source=source_item
        )
        for tag in item['tags']:
            tag_item,_ = Tag.objects.get_or_create(caption=tag)
            news_item.tags.add(tag_item)

        self.existing_urls.add(item['source'])
        return item