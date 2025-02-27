# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from .settings import *
import pymysql
import redis
import re
from scrapy.exceptions import DropItem

TBL_NAME_Liepin = 'liepin'

class Job51RedisPipepline:
    def open_spider(self, spider):
        self.redis = redis.Redis(host='127.0.0.1')

    def process_item(self, item, spider):
        if self.redis.sadd(spider.name,item['coid']):
            return item
        raise DropItem


class Job51MysqlPipeline:
    def open_spider(self,spider):
        self.conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset=MYSQL_CHARSET
        )
        self.curror = self.conn.cursor()


    def close_spider(self,spider):
        self.curror.close()
        self.conn.close()


    def process_item(self, item, spider):
        keys, values = zip(*item.items())
        sql = "insert into job51 ({}) values ({}) ON DUPLICATE KEY UPDATE {}".format(
            # item.table_name,
            ','.join(keys),
            ','.join(['%s'] * len(values)),
            ','.join(['`{}`= %s'.format(k) for k in keys])
        )
        try:
            self.curror.execute(sql, values * 2)
            self.conn.commit()
            print(item)
            return item
        except Exception as e:
            print(e)
