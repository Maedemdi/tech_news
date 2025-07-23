from celery import shared_task
import subprocess
import os

@shared_task
def test_task():
    print("+++++++++++++ CELERY IS WORKING!! ++++++++++++++++++")
    return "Test completed"


@shared_task
def run_scraper():

    scrapy_path = os.path.join(os.path.dirname(__file__), '..', 'scraper')

    result = subprocess.run(
        ['scrapy', 'crawl', 'zoomit_spider'],
        cwd= scrapy_path,
        capture_output=True,
        text=True
        )

    if result.returncode == 0 :
        return "Scrapy executed successfully!"
    else: 
        return "Scrapy failed!"