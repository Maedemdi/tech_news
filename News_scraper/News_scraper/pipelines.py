
import os
import django
import sys
import asyncio

from itemadapter import ItemAdapter
from django.db import transaction, close_old_connections
from .items import NewsItem

# adds the project root (TechNews_dir) to Python's import path
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

print("BASE_DIR:", BASE_DIR)
print("TechNews exists:", os.path.isdir(os.path.join(BASE_DIR, "TechNews")))

sys.path.insert(0, BASE_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "TechNews.settings"
)

django.setup()

from News_app.models import News, Tag

class NewsScraperPipeline:

    async def process_item(self, item, spider):
        print(isinstance(item, NewsItem))
        return await asyncio.to_thread(  # runs self.save_item(item, spider) in another thread
            self.save_item, item, spider
        )

    def save_item(self, item, spider):  # synchronous
        adapter = ItemAdapter(item)

        close_old_connections()

        try:
            with transaction.atomic():
                news, created = News.objects.update_or_create(
                    url=adapter["url"],  # required field
                    defaults={
                        "title": adapter["title"],  # required field
                        "content": adapter.get("content"),
                        "date": adapter.get("date"),
                        "author": adapter.get("author"),
                    }
                )

                tags = []
                for tag_label in adapter.get("tags", []):
                    tag, _ = Tag.objects.get_or_create(
                        label=tag_label.strip()
                    )
                    tags.append(tag)
                news.tags.set(tags)  # could be done with add too

            # spider.logger.info(
            #     f"News {'created' if created else 'updated'}: "
            #     f"{news.url}"
            # )
            # spider.logger.info(
            #     f"Scraped tags for {adapter.get('url')}: "
            #     f"{adapter.get('tags')}"
            # )

        except Exception:
            spider.logger.exception(
                f"Failed to save news: {adapter.get('url')}"
            )
            raise

        finally:
            close_old_connections()

        #return item     # received by the following pipeline
