from scrapy.cmdline import execute
import os 
os.chdir(os.path.join("dingdian"))
execute(['scrapy', 'crawl', 'dingdian'])

