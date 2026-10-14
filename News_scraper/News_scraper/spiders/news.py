from scrapy import Spider, Request, Selector
from scrapy.loader import ItemLoader
from News_scraper.items import NewsItem
from urllib.parse import urljoin


class NewsSpider(Spider):
    name = "news_spider"
    page_count = 1

    async def start(self):
        yield self.page_request(self.page_count)
    
    def page_request(self, page_count):
        url = "https://www.zoomit.ir/archive?sort=Newest&publishDate=All&readingTime=All&pageNumber="
        return Request(
            url + str(page_count),
            callback=self.parse,
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

        print(f"News found in page {self.page_count}:", len(news_items))

        for news_item in news_items:
            link = news_item.css(
                "a.cursor-pointer.no-underline.decoration-0::attr(href)"
            ).get()
            yield Request(
                url=urljoin(url, link),
                callback=self.parse_details
            )

        await page.close()

        self.page_count += 1
        if self.page_count <= 3:
            yield self.page_request(self.page_count)

    def parse_details(self, response):
        loader = ItemLoader(
            item=NewsItem(), selector=response.css("article.contents"))
        loader.add_css("title", "header.ArticleHeader__TemplateStandard-sc-e19b71f8-5 h1.typography__StyledDynamicTypographyComponent-sc-c97798ae-0::text")
        loader.add_css("author", "span.wrMhL::text")
        loader.add_value("url", response.url)
        loader.add_css("content", "p.article-lead::text")
        loader.add_css("content", "p.typography__StyledDynamicTypographyComponent-sc-c97798ae-0.ParagraphElement__ParagraphBase-sc-e00494a0-0::text")
        loader.add_css("date", "time::attr(datetime)")
        loader.add_css("tags", "li.ArticleCategory__BreadcrumbItem-sc-4ed7a5f6-1 a span.typography__StyledDynamicTypographyComponent-sc-c97798ae-0::text")
        yield loader.load_item()
