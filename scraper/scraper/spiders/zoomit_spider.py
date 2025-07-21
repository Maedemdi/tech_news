import scrapy
from scrapy_playwright.page import PageMethod

class ZoomitSpiderSpider(scrapy.Spider):
    name = "zoomit_spider"
    allowed_domains = ["zoomit.ir"]
    start_urls = ["https://www.zoomit.ir/archive/?sort=Newest&publishDate=All&readingTime=All&pageNumber=1"]


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url = url,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                    PageMethod("wait_for_selector", 'a.cursor-pointer')
                ],
                },
            )
        
    def parse(self, response):
        current_page = 1

        urls = response.css('div.flex div a::attr(href)').getall()
        for url in urls: 
            yield scrapy.Request(
                url= url,
                meta={
                        "playwright": True,
                        "playwright_page_methods": [
                        PageMethod("wait_for_selector", 'a.cursor-pointer')],
                        "playwright_page_goto_kwargs": {
                        "timeout": 60000,
                        "wait_until": "domcontentloaded",
                    },},
                    callback= self.parse_details
                )
            
        if current_page < 6 and response.css("button.sc-9bfa8572-0.jbTKNm.sc-7273a243-1.hnOzQz"):
            current_page += 1
            yield scrapy.Request(
                url=response.url,
                callback=self.parse,
                dont_filter=True,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("click", "button.sc-9bfa8572-0.jbTKNm.sc-7273a243-1.hnOzQz"),
                        PageMethod("wait_for_selector", "div.flex div a"),
                    ],
                },
            )



    def parse_details(self, response):
        news = response.css("main.bg-background2.border-grey6.relative.pb-12")
        title = news.css("div h1.sc-9996cfc-0::text").get()
        text_selectors = news.css("div.sc-481293f7-1.jrhnOU span.sc-9996cfc-0::text").getall()
        content = "\n".join(text_selectors)
        created_at = news.css("span.sc-9996cfc-0.inKOvi.fa::text").get()
        tags = news.css("a span.sc-9996cfc-0.NawFH::text").getall()
        writer = news.css("div.sc-a11b1542-0.GGjpx span::text").get()

        news_item = {
                    "title": title,
                    "text": content,
                    "created_at": created_at,
                    "tags": tags,
                    "writer": writer,
                    "source": response.url
                }
        
        
        yield news_item
