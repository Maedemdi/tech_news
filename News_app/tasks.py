import os
from celery import shared_task
import subprocess

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
    
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("Return code:", result.returncode)
    if result.returncode == 0 :
        print(result.stdout)
        return "Scrapy executed successfully!"
    else: 
        return "Scrapy failed!"