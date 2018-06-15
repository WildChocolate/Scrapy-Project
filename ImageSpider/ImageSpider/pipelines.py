# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ImagespiderPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
    #     return item

    def get_media_requests(self, item, info):
        for image_url in item["imgUrl"]:
            print(image_url)
            yield Request(image_url)

    
