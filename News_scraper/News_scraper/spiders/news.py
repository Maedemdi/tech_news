from scrapy import Spider, Request, Selector
from scrapy.loader import ItemLoader
from News_scraper.items import NewsItem


class NewsSpider(Spider):
    name = "news_spider"

    async def start(self):
        yield Request(
            "https://www.zoomit.ir/archive?sort=Newest&publishDate=All&readingTime=All&pageNumber=1",
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_goto_kwargs": {
                    "wait_until": "domcontentloaded",
                    "timeout": 60000,
                },
            },
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        url = "https://www.zoomit.ir/"

        # Wait for the news items to appear
        news_items_locator = page.locator("div.scroll-m-16")
        await news_items_locator.first.wait_for()

        # Convert rendered Playwright HTML to Scrapy Selector
        selector = Selector(text=await page.content())
        news_items = selector.css("div.scroll-m-16")

        print("count", len(news_items))

        for news_item in news_items:
            print(news_item.css("::text").getall())

            link = news_item.css(
                "a.cursor-pointer.no-underline.decoration-0::attr(href)"
            ).get()

            print("[[[[[[URL]]]]]]", url + link)

            yield Request(
                url=url + link,
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
        