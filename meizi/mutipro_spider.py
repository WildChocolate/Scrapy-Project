from downloader import request
from mongodb_queue import MogoQueue
from bs4 import BeautifulSoup


spider_queue  = MogoQueue("meinvxiezhenji", "crawl_queue")
def start(url):
    response = request.get(url)
    Soup = BeautifulSoup(response.text, "lxml")
    all_a = Soup.find("div", class_="all").find("ul").find_all("a")
    for a in all_a:
        title = a.get_text()
        url = a["href"]
        spider_queue.push(url, title)
    """上面这个调用就是把Url写入MongoDB的队列"""


if __name__=="__main__":
    start("http://www.mzitu.com/all")
