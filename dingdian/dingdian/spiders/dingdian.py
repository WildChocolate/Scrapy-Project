import scrapy
import re
from bs4 import BeautifulSoup
from scrapy.http import Request
from dingdian.items import DingdianItem, DcontentItem
from dingdian.mysqlpipelines.sql import Sql

class Spider(scrapy.Spider):
    name = "dingdian"
    allowed_domains = ["23us.so"]
    bash_url = "http://www.23us.so/list/"
    bashurl = ".html"
    def __init__(self):
        self.headers = dict()

    def start_requests(self):
        user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
        self.headers = {"User-Agent":user_agent}
        for i in range(1, 10):
            url = self.bash_url + str(i) + "_1" + self.bashurl
            self.headers["Referer"] = url
            yield Request(url, headers=self.headers, callback=self.parse)
        self.headers["Referer"] = "http://www.23us.so/full.html"
        yield Request("http://www.23us.so/full.html", headers=self.headers, callback=self.parse)

    def parse(self, response):
        max_num = BeautifulSoup(response.text, "lxml").find("div", class_="pagelink").find("a", class_="last").get_text()
        for i in range(1, int(max_num)+1):
            url = self.bash_url + "1_" + str(i) + self.bashurl
            self.headers["Referer"] = url
            yield Request(url, headers=self.headers, callback=self.get_name)

    def get_name(self, response):
        tds = BeautifulSoup(response.text, "lxml").find_all("tr", bgcolor="#FFFFFF")
        for td in tds:
            novelname = td.find("a").get_text()
            novelurl = td.find("a")["href"]
            self.headers["Referer"] = novelurl
            yield Request(novelurl, headers=self.headers, callback=self.get_chapterurl, meta={"name":novelname, "url":novelurl})

    def get_chapterurl(self, response):
        Item = DingdianItem()
        Item["name"] = str(response.meta["name"]).replace("\xa0", "")
        Item["novelUrl"] = response.meta["url"]
        htmlsoup = BeautifulSoup(response.text, "lxml")
        categroy = htmlsoup.find("table").find("a").get_text()
        author = htmlsoup.find("tr").find_all("td")[1].get_text()
        bash_url = htmlsoup.find("p", class_="btnlinks").find("a", class_="read")["href"]
        name_id = bash_url.split("/")[-2]
        Item["category"] = str(categroy).replace("\a0", "")
        Item["author"] = str(author).replace("\a0", "")
        Item["name_id"] = name_id
        yield Item
        yield Request(bash_url, callback=self.get_chapter, meta={"name": name_id})

    def get_chapter(self, response):
        urls = re.findall(r"<td class='L'><a href='(.*?)>(.*?)</a></td>'", response.text)
        num = 0
        for url in urls:
            num = num + 1
            chapterurl = response.url + url[0]
            chaptername = url[1]
            rets = Sql.select_chapter(chapterurl)
            if rets[0] == 1:
                print("章节已经存在了")
                pass
            else:
                yield Request(chapterurl, callback=self.get_chaptercontent, meta={
                                                                            "num" : num,
                                                                            "name_id" : response.meta["name_id"],
                                                                            "chaptername" : chaptername,
                                                                            "chapterurl" : chapterurl
                                                                        })

    
    def get_chaptercontent(self, response):
        item = DcontentItem()
        item["num"] = response.meta["num"]
        item["id_name"] = response.meta["name_id"]
        item["chaptername"] = str(response.meta["chaptername"]).replace("\xa0", "")
        item["chapterurl"] = response.meta["chapterurl"]
        content = BeautifulSoup(response.text, "lxml").find("dd", id="contents").get_text()
        item["chaptercontent"] = str(content).replace("\xa0", "")
        return item