import scrapy
from scrapy_playwright.page import PageMethod

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechNews_project.settings')

import django
django.setup()

from News_app.models import Source


class ZoomitSpiderSpider(scrapy.Spider):
    name = "zoomit_spider"
    allowed_domains = ["zoomit.ir"]
    start_urls = ["https://www.zoomit.ir/archive/?sort=Newest&publishDate=All&readingTime=All&pageNumber=1"]
    visited_urls = list(Source.objects.values_list("url", flat=True))
    current_page = 1
    parse_details_count = 0


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url = url,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                    PageMethod("wait_for_selector", 'div.flex div a.cursor-pointer'),
                    ],
                    "playwright_page_goto_kwargs": {
                        "timeout": 60000
                    },
                },
            )
    def parse(self, response):

        urls = response.css('div.flex div a.cursor-pointer::attr(href)').getall()
        for url in urls: 
            if url in self.visited_urls:
                continue
            else: 
                yield scrapy.Request(
                    url= url,
                    meta={
                            "playwright": True,
                            "playwright_page_goto_kwargs": {
                            "wait_until": "domcontentloaded", 
                            "timeout": 60000
                            },
                            },
                        callback= self.parse_details
                    )  

        if self.current_page < 1: 
            self.current_page += 1
            yield scrapy.Request(
                    url=response.url,
                    dont_filter=True,
                    meta={
                        "playwright": True,
                        "playwright_page_methods": [
                            PageMethod("click", "button.sc-9bfa8572-0.jbTKNm.sc-7273a243-1.hnOzQz"),
                            PageMethod("wait_for_selector", "div.flex div a.cursor-pointer"),
                        ],
                        "playwright_page_goto_kwargs": {
                            "timeout": 60000
                        }
                    },
                    callback=self.parse
                )



    def parse_details(self, response):

        
        self.parse_details_count += 1  
        print("++++++++++++++++++++++++++++++++++++++ PARSE DETAILS COUNT +++++++++++++++++++++++++++++++++++++ = ", self.parse_details_count)

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
