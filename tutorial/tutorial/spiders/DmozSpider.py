import scrapy

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["www.ganji.com"]
    start_urls = [
        "http://sz.ganji.com/fang1/"
    ]

    def parse(self, response):
        filename  = response.url.split("/")[-2]
        with open(filename, "wb") as f:
            f.write(response.body)