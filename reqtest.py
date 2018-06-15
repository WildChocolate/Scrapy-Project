import requests
from bs4 import BeautifulSoup
import os


headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）}
all_url = "http://www.mzitu.com/all"
start_html = requests.get(all_url, headers=headers)
