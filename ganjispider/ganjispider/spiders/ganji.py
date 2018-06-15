import scrapy
from ..items import GanjispiderItem

class GanjiSpider(scrapy.Spider):
    name = "zufang"
    start_urls = ["http://sz.ganji.com/fang1/longgang/"]
    
    def parse(self, response):
        print(response)
        title_list = response.xpath("//*[@class='f-list-item ershoufang-list']/dl/dd[1]/a/text()").extract()
        price_list = response.xpath("//*[@class='f-list-item ershoufang-list']/dl/dd[5]/div/span[1]/text()").extract()
        item = GanjispiderItem()

        for t, p in zip(title_list, price_list):
            item["title"] = t
            item["price"] = p
            #print(t, "-----------------------", p)
            yield item
