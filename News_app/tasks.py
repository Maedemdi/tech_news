import os
import subprocess
from celery import shared_task
from django.core.cache import cache

from .models import News
from .serializers import NewsSerializer

@shared_task
def run_spider():
    spider_path = os.path.join(os.path.dirname(__file__), '..', 'News_scraper')
    print(spider_path)
    result = subprocess.run(
        ["scrapy", "crawl", "news_spider"],
        cwd=spider_path,
        capture_output=True,
        text=True,
        )
    
    print("STDOUT:", result.stdout)   # The normal output produced by Scrapy
    print("STDERR:", result.stderr)   # Error output produced by Scrapy
    print("Return code:", result.returncode)    # The process's exit code
    if result.returncode == 0 :
        return "Scrapy executed successfully!"
    else: 
        return "Scrapy failed!"
    

@shared_task
def cache_news(news_id):
    cache_key = f"news:{news_id}"
    news = (
        News.objects
        .prefetch_related("tags")
        .get(id=news_id)
    )
    data = NewsSerializer(news).data
    cache.set(cache_key, data, timeout=120)

    print(f"Cached news with id {news_id}")
    return data