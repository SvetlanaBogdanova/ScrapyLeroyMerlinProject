# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def process_url(url):
    return url.replace('w_82', 'w_400').replace('h_82', 'h_400')


class GoodsparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(lambda x: float(x.replace(' ', ''))))
    url = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field(input_processor=MapCompose(process_url))
    property_names = scrapy.Field(input_processor=MapCompose(lambda x: x.strip()))
    property_values = scrapy.Field(input_processor=MapCompose(lambda x: x.strip()))
    properties = scrapy.Field()
    _id = scrapy.Field(output_processor=TakeFirst())
