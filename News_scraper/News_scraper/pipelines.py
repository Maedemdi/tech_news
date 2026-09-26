import os
import django
import sys
import asyncio

from dotenv import load_dotenv
from itemadapter import ItemAdapter
from django.db import transaction, close_old_connections
from pathlib import Path

from News_app.models import News, Tag

load_dotenv()


BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "TechNews.settings"
)

django.setup()


class NewsScraperPipeline:

    async def process_item(self, item, spider):
        return await asyncio.to_thread(
            self.save_item, item, spider
        )

    def save_item(self, item, spider):
        adapter = ItemAdapter(item)

        close_old_connections()

        try:
            with transaction.atomic():
                news, created = News.objects.update_or_create(
                    url=adapter["url"],
                    defaults={
                        "title": adapter.get("title"),
                        "content": adapter.get("content"),
                        "date": adapter.get("date"),
                        "author": adapter.get("author"),
                    }
                )

                tags = []
                for tag_name in adapter.get("tags", []):
                    tag, _ = Tag.objects.get_or_create(
                        label=tag_name.strip()
                    )
                    tags.append(tag)
                news.tags.set(tags)

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

        return item