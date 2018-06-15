import os 
import time
import threading
import multiprocessing
from mongodb_queue import MogoQueue
from downloader import request
from bs4 import BeautifulSoup


SLEEP_TIME = 1 

def mzitu_crawler(max_threads=10):
    crawl_queue = MogoQueue('meinvxiezhenji', 'crawl_queue')

    def pageurl_crawler():
        while True:
            try:
                url = crawl_queue.pop()
                print(url)
            except KeyError:
                print("队列没有数据")
            else:
                img_urls = []
                req = request.get(url, 3).text
                title = crawl_queue.pop_title(url)
                mkdir(title)
                os.chdir("D:\mzitu\\" + title)
                max_span = BeautifulSoup(req, "lxml").find("div", class_="pagenavi").find_all("span")[-2].get_text()
                for page in range(1, int(max_span)+1):
                    page_url = url + "/" +str(page)
                    img_url = BeautifulSoup(request.get(page_url).text, "lxml").find("div", class_="main-image").find("img")["src"]
                    img_urls.append(img_url)
                    save(img_url)
                crawl_queue.complete(url)


    def save(img_url):
        name = img_url[-9:-4]
        print(u"开始保存：", img_url)
        img = request.get(img_url)
        f = open(name + ".jpg", "ab")
        f.write(img.content)
        f.close()

    def mkdir(path):
        paht = path.strip()
        isExits = os.path.exists(os.path.join("D:\mzitu\\", path))
        if not isExits:
            print(u"建了一个名字叫做", path, u"的文件夹!")
            os.makedirs(os.path.join("D:\mzitu\\", path))
            return True
        else:
            print(u"已存在名字叫做", path)
            return False

    threads = []
    while threads or crawl_queue:
        """
        这儿crawl_queue用上了，就是我们__bool__函数的作用，为真则代表我们MongoDB队列里面还有数据
        threads 或者 crawl_queue为真都代表我们还没下载完成，程序就会继续执行
        """

        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads or crawl_queue.peek():
            thread = threading.Thread(target=pageurl_crawler)
            thread.setDaemon(True)##设置守护线程
            thread.start()
            threads.append(thread)
        time.sleep(SLEEP_TIME)



def process_crawler():
    process = []

    num_cpus = multiprocessing.cpu_count()
    print("将会启动进程数为：", num_cpus)
    for i in range(num_cpus):
        p = multiprocessing.Process(target=mzitu_crawler)
        p.start()
        process.append(p)##添加进进程队列
    for p in process:
        p.join()##等待进程队列里面的进程结束)

if __name__=="__main__":
    process_crawler()