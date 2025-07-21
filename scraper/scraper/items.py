from scrapy import Item, Field
from itemloaders.processors import MapCompose, TakeFirst


# class ScraperItem(Item):
#     title = Field(output_processor = TakeFirst())
#     text = Field()
#     # tags = Field()
#     created_at = Field(output_processor = TakeFirst())
#     # writer = Field(output_processor = TakeFirst())
