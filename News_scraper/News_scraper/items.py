from dataclasses import dataclass
from scrapy import Item, Field
from itemloaders.processors import MapCompose, TakeFirst


def get_standard_date(txt):
    return txt[0:10]


class NewsItem(Item):
    title = Field(
        output_processor=TakeFirst())
    # content = Field(
    #     output_processor=TakeFirst())
    # author = Field(
    #     output_processor=TakeFirst())
    # date = Field(
    #     input_processor=MapCompose(get_standard_date),
    #     output_processor=TakeFirst())
    # url = Field(
    #     output_processor=TakeFirst())
    # tags = Field(
    #     output_processor=TakeFirst())
