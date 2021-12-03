# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from urllib.parse import urlparse

import scrapy
from scrapy.pipelines.images import ImagesPipeline

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class GoodsparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.goods

    def process_item(self, item, spider):
        item['properties'] = self.process_properties(item['property_names'], item['property_values'])
        del item['property_names'], item['property_values']

        collection = self.mongo_base[spider.name]
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            pass

        return item

    def process_properties(self, names, values):
        properties_dict = {}
        for i in range(len(names)):
            properties_dict[names[i]] = values[i]
        return properties_dict


class GoodsImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images']:
            for img in item['images']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['images'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f"{item['_id']}/{os.path.basename(urlparse(request.url).path)}"
