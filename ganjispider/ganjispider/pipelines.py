# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class GanjispiderPipeline(object):
    def open_spider(self, spider):
        self.conn = sqlite3.connect("zufang.sqlite")
        self.cur = self.conn.cursor()
        #self.cur.execute("create table zufang (title varchar(512), price varchar(100)) ")

    def process_item(self, item, spider):
        print(spider.name)
        print(item["title"], "--------------------", item["price"])
        insert_sql = "insert into zufang(title, price) values ('{}', '{}')".format(item["title"], item["price"])
        print(insert_sql)
        self.cur.execute(insert_sql)
        self.conn.commit()
        return item

    def spider_close(self, spider):
        self.cur.close()
        self.conn.close()