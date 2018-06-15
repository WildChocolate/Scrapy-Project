import scrapy
from ImageSpider.items import ImagespiderItem


class ImgspiderSpider(scrapy.Spider):
    name = "ImgSpider"
    allow_domains = ["lab.scrapyd.cn"]
    start_urls = [
        "http://lab.scrapyd.cn/archives/55.html"
    ]

    def parse(self, response):
        item = ImagespiderItem()
        imgUrls = response.css(".post img::attr(src)").extract()
        item["imgUrl"] = imgUrls
        yield item
        pass