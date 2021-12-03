from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from goodsparser import settings
from goodsparser.spiders.leroymerlinru import LeroymerlinruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    query = input('Поиск: ')
    process.crawl(LeroymerlinruSpider, query=query)
    process.start()
