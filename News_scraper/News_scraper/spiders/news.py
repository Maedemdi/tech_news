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
        yield loader.load_item()
        # content = resoponse.css("p.typography__StyledDynamicTypographyComponent-sc-4caf251e-0.jkVxA-D.ParagraphElement__ParagraphBase-sc-867699c3-0.hahzmx").getall()
        # author = resoponse.css("span.flJYlr::text").get()
        # date = resoponse.css("time[datetime].attr(datetime)").get()
        # url = resoponse.url
        # tags = resoponse.css("a span.typography__StyledDynamicTypographyComponent-sc-4caf251e-0.hBZvuY")
