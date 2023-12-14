# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import os

class MongodbPipeline:
    collections_name = 'transcript'
    def open_spider(self, spider):
        a = 1
        self.client = pymongo.MongoClient(f"mongodb+srv://{os.environ.get('mangodb_username')}:{os.environ.get('mangodb_password')}@cluster0.lyryivk.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['My_Database']
    def close_spider(self, spider):
        a = 1
        self.spider.close()
    def process_item(self, item, spider):

        self.db[self.collections_name].insert(item)
        return item
