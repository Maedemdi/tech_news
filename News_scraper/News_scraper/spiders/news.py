from scrapy import Spider, Request, Selector
from scrapy.loader import ItemLoader
from News_scraper.items import NewsItem
from urllib.parse import urljoin

import os
import sys
import django

# Add the project root (TechNews_dir) to Python's import path
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)
sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TechNews.settings")
django.setup()

from News_app.models import News, Tag

class NewsSpider(Spider):
    name = "news_spider"

    async def start(self):
        yield Request(
            "https://www.zoomit.ir/archive?sort=Newest&publishDate=All&readingTime=All&pageNumber=1",
            meta={
                "playwright": True,
                # to access the actual browser page, saved in meta dict
                "playwright_include_page": True,
                "playwright_page_goto_kwargs": {
                    "wait_until": "domcontentloaded",   # waits for the initial html document
                    "timeout": 60000,
                },
            },
        )

    async def parse(self, response):
        # Playwright Page object - Represents the browser tab
        page = response.meta["playwright_page"]
        url = "https://www.zoomit.ir/"

        news_items_locator = page.locator("div.scroll-m-16")
        # waits until the first matching element becomes visible
        await news_items_locator.first.wait_for()

        # convert rendered Playwright HTML to Scrapy Selector
        selector = Selector(text=await page.content())
        news_items = selector.css("div.scroll-m-16")

        print("News found in this page:", len(news_items))

        for news_item in news_items:
            link = news_item.css(
                "a.cursor-pointer.no-underline.decoration-0::attr(href)"
            ).get()
            yield Request(
                url=urljoin(url, link),
                callback=self.parse_details
            )

        await page.close()

    def parse_details(self, response):
        loader = ItemLoader(
            item=NewsItem(), selector=response.css("article.contents"))
        loader.add_css("title", "h1.eTcJxy::text")
        loader.add_css("author", "span.flJYlr::text")
        loader.add_value("url", response.url)
        loader.add_css("content", "p.article-lead::text")
        loader.add_css("content", "p.hahzmx::text")
        loader.add_css("date", "time::attr(datetime)")
        loader.add_css("tags", "li.goGvvZ a span.hBZvuY::text")
        yield loader.load_item()
