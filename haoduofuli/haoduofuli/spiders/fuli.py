from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from haoduofuli.items import HaoduofuliItem
from scrapy import FormRequest


account = "帐号"
password = "密码"

class myspider(CrawlSpider):
    name = "haoduofuli"
    allowed_domains = ["haoduofuli.wang"]
    start_urls = ["http://www.haoduofuli.wang/wp-login.php"]


    def parse_start_url(self, response):
        """
        如果你登录的有验证码之类的，你就可以在此处加入各种处理方法；
        比如提交给打码平台，或者自己手动输入、再或者pil处理之类的
        """
        formdate = {
            "log" : account,
            "pwd" : password,
            "remenberme" : "forever",
            "wp-submit" : "登录",
            "redirect_to" : "http://www.haoduofuli.wang/wp-admin/",
            "testcooke" : "1"
        }
        return [FormRequest.from_response(response, formdata = formdate, callback=self.after_login)]

    def after_login(self, response):
        #可以在此处加上判断来确认是否登录成功、进行其他动作。
        lnk = "http://www.haoduofuli.wang"
        return Request(lnk)

    rules = [
        Rule(LinkExtractor(allow=('\.html',)), callback='parse_item', follow=True),
    ]

    def parse_item(self, response):
        item = HaoduofuliItem()
        item["url"] = response.url
        item["category"] = response.xpath("//*[@id='content']/div[1]/div[1]/span[2]/a/text()").extract()[0]
        item["title"] = response.xpath("//*[@id='content']/div[1]/h1/text()").extract()[0]
        item["imgurl"] = response.xpath("//*[@id='post_content]/p/img/@src'").extract()
        return item