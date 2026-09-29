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
    
    print("STDOUT:", result.stdout)   # The normal output produced by Scrapy
    print("STDERR:", result.stderr)   # Error output produced by Scrapy
    print("Return code:", result.returncode)    # The process's exit code
    if result.returncode == 0 :
        return "Scrapy executed successfully!"
    else: 
        return "Scrapy failed!"