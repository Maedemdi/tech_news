import scrapy
from scraper.items import ScraperItem
from scrapy.loader import ItemLoader


class ZoomitSpiderSpider(scrapy.Spider):
    name = "zoomit_spider"
    allowed_domains = ["zoomit.ir"]
    start_urls = ["https://www.zoomit.ir/"]


    def parse(self, response):
        urls = response.css("a[href^='https://www.zoomit.ir/']::attr(href)").getall()

        for url in urls:
            yield scrapy.Request(
                url= url,
                meta= {
                    "playwright": True,
                },
                callback= self.parse_details
            )


    def parse_details(self, response):
        news = response.css("main.bg-background2.border-grey6.relative.pb-12")
        title = news.css("div.fjdwzl h1.sc-9996cfc-0::text").get()
        text_selectors = news.css(".sc-481293f7-1.jrhnOU .sc-9996cfc-0::text").getall()
        created_at = news.css("span.sc-9996cfc-0.inKOvi.fa::text").get()
        tags = news.css("a span.sc-9996cfc-0.NawFH::text").getall()
        writer = news.css("div.sc-a11b1542-0.GGjpx span::text").get()

        content = ''
        for text in text_selectors:
            content += text

        if title is not None:
            yield {
                    "title": title,
                    "text": content,
                    "created_at": created_at,
                    "tags": tags,
                    "writer": writer,
                    "source": response.url
                }
