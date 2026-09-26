import os
import django
import sys
import asyncio

from itemadapter import ItemAdapter
from django.db import transaction, close_old_connections
from pathlib import Path

from News_app.models import News, Tag

BASE_DIR = Path(__file__).resolve().parents[2]  # path object

sys.path.insert(0, str(BASE_DIR))   # adding BASE_DIR to the beginning of python's import path

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "TechNews.settings"
)

django.setup()


class NewsScraperPipeline:

    async def process_item(self, item, spider):
        return await asyncio.to_thread( # runs self.save_item(item, spider) in another thread
            self.save_item, item, spider
        )

    def save_item(self, item, spider):  # synchronous
        adapter = ItemAdapter(item)

        close_old_connections()

        try:
            with transaction.atomic():
                news, created = News.objects.update_or_create(
                    url=adapter["url"], #required field
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

            spider.logger.info(
                f"News {'created' if created else 'updated'}: "
                f"{news.url}"
            )
            spider.logger.info(
                f"Scraped tags for {adapter.get('url')}: "
                f"{adapter.get('tags')}"
            )

        except Exception:
            spider.logger.exception(
                f"Failed to save news: {adapter.get('url')}"
            )
            raise

        finally:
            close_old_connections()

        return item     # received by the following pipeline
