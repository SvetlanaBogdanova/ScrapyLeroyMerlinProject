import scrapy
from scrapy.http import HtmlResponse
from goodsparser.items import GoodsparserItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']")
        if next_page:
            yield response.follow(next_page[0], callback=self.parse)
        links = response.xpath("//div[@class='phytpj4_plp largeCard']/a")
        for link in links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=GoodsparserItem(), response=response)

        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('images', "//img[@slot='thumbs']/@src")
        loader.add_value('url', response.url)
        loader.add_xpath('property_names', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('property_values', "//dd[@class='def-list__definition']/text()")
        loader.add_xpath('_id', "//span[@slot='article']/@content")
        yield loader.load_item()
