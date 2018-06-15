from downloader import request
from bs4 import BeautifulSoup
import os
from pymongo import MongoClient
import datetime

""" headers= {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）

all_url = "http://www.mzitu.com/all"
start_html = requests.get(all_url, headers = headers)

Soup = BeautifulSoup(start_html.text, "lxml")
all_a = Soup.find("div", class_="all").find("ul").find_all("a")
for a in all_a:
    title = a.get_text()
    href = a["href"]
    
    html= requests.get(href, headers=headers)
    #print(html.text)
    html_soup = BeautifulSoup(html.text, "lxml")
    caption = html_soup.find("h2", class_="main-title").get_text()
    isExists=os.path.exists(caption)
    if not isExists:
        os.makedirs(caption)
    max_span = html_soup.find("div", class_="pagenavi").find_all("span")[-2].get_text()
    print(href,"max",max_span)
    for page in range(1, int(max_span)+1):
        page_url = href + "/" + str(page)
        headers["Referer"] = page_url
        img_html = requests.get(page_url, headers=headers)
        img_soup = BeautifulSoup(img_html.text, "lxml")
        img_url = img_soup.find("div", class_="main-image").find("img")["src"]
        name = img_url[-9:-4] ##取URL 倒数第四至第九位 做图片的名字
        img = requests.get(img_url)
        filename = caption+ "/" +name + ".jpg"
        f = open(filename, "ab")
        f.write(img.content)
        f.close()
        print(filename + " complete!!!")
         """

class meizitu():

    def __init__(self):
        client = MongoClient()
        db = client["meinvxiezhenji"]
        self.meizitu_collection = db["meizitu"]
        self.title = ""
        self.url= ""
        self.img_urls = []
     
    def all_url(self, url):
        html = request.get(url)
        all_a = BeautifulSoup(html.text, "lxml").find("div", class_="all").find("ul").find_all("a")
        for a in all_a:
            title = a.get_text()
            print("开始保存:", title)
            path = str(title).replace("?", "_")
            self.mkdir(path)
            os.chdir("D:\mzitu\\"+path)
            href = a["href"]
            self.url = href
            if self.meizitu_collection.find_one({"主题页面":href}):
                print(u"这个页面已经爬取过了")
            else:
                self.html(href)
            self.html(href)

    def html(self, href):
        print(href)
        html = request.get(href)
        max_span = BeautifulSoup(html.text, "lxml").find_all("span")[10].get_text()
        paeg_num = 0
        for page in range(1, int(max_span)+1):
            paeg_num = paeg_num +1
            page_url = href + "/" + str(page)
            self.img(page_url, max_span, paeg_num)

    def img(self, page_url, max_span, page_num):
        img_html = request.get(page_url)
        img_url = BeautifulSoup(img_html.text, "lxml").find("div", class_="main-image").find("img")["src"]
        self.img_urls.append(img_url)
        if int(max_span) == page_num:
            self.save(img_url)
            post = {
                "标题":self.title,
                "主题页面":self.url,
                "图片地址":self.img_urls,
                "获取时间":datetime.datetime.now()
            }
            self.meizitu_collection.save(post)
        else:
            self.save(img_url)
        
    
    def save(self, img_url):
        name = img_url[-9:-4]
        print("开始保存：", img_url)
        img = request.get(img_url)
        f = open(name + ".jpg", "ab")
        f.write(img.content)
        f.close()

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(os.path.join("D:\mzitu", path))
        if not isExists:
            print(u" 新建了一个名字叫做", path, u"的文件夹")
            os.makedirs(os.path.join("D:\mzitu",path))
            return True
        else:
            print(u"名字叫做,", path, u"的文件夹已经存在了")
            return False

Mzitu = meizitu()
Mzitu.all_url("http://www.mzitu.com/all")

""" import pymongo
from pymongo  import MongoClient
client = MongoClient()
db = client["meinvxiezhenji"]
doc = db["crawl_queue"]
for d in doc.find():
    print(d) """