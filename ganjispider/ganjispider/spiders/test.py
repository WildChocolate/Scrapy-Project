import re


sites= '''
    <loc href="dfdfdf">http://www.baidu.com</loc>
    <loc>http://www.taobao.com</loc>
    <loc>http://www.jd.com</loc>
    <loc>http://www.youku.com</loc>
'''

links = re.findall("<loc (?:href=\".+\")>(.+)</loc>", sites)
for lnk in links:
    print(lnk)