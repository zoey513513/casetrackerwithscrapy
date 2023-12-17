# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import os
import sqlite3
class MongodbPipeline:
    collections_name = 'transcript'
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(f"mongodb+srv://{os.environ.get('mangodb_username')}:{os.environ.get('mangodb_password')}@cluster0.lyryivk.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['My_Database']
    def close_spider(self, spider):
        self.spider.close()
    def process_item(self, item, spider):

        self.db[self.collections_name].insert(item)
        return item
class SQLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('transcript.db')
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE transcripts(
                title TEXT,
                plot TEXT
            )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()
    def process_item(self, item, spider):

        self.c.execute('''
        INSERT INTO transcripts (title,plot) VALUES(?,?)
        ''', (
            item.get('title'),
            item.get('plot'),
        ))
        self.connection.commit()
        return item

