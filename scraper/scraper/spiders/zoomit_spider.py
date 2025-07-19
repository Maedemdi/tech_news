import scrapy


class ZoomitSpiderSpider(scrapy.Spider):
    name = "zoomit_spider"
    allowed_domains = ["zoomit.ir"]
    start_urls = ["https://zoomit.ir"]

    def parse(self, response):
        pass
