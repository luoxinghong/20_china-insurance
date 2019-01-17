# -*- coding: utf-8 -*-
from lxml import etree
import requests
import re


class zixun_spider(object):
    def __init__(self, subname, page_number, path):
        self.subname = subname
        self.page_number = page_number
        self.path = path
        self.url_temp = "http://www.china-insurance.com/news-center/moreItem.asp?subname=" + subname + "&page={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

    # 构造url列表
    def get_url_list(self):
        url_list = [self.url_temp.format(i) for i in range(1, self.page_number)]
        return url_list

    # 发送请求，获取响应
    def parse_url(self, url):
        html = requests.get(url, headers=self.headers).content
        return html.decode("GBK", "ignore")

    # 保存网页的html字符串
    def save_news(self, html):
        news_url_list = etree.HTML(html).xpath("//a[contains(@href,'newslist.asp?id=')]/@href")
        for url in news_url_list:
            html = self.parse_url("http://www.china-insurance.com/news-center/" + url)
            date = re.findall(r'\d*', etree.HTML(html).xpath("//tr[@bgcolor='EEF5FF']/td/text()")[0])
            date = date[2] + '{:0>2}'.format(date[4]) + '{:0>2}'.format(date[6])
            name = etree.HTML(html).xpath("//p[@class='f20b']/text()")[0]
            rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
            name = re.sub(rstr, "_", name)
            content = etree.HTML(html).xpath("//font[@id='zoom']//text()")
            print(url)
            with open(self.path + date + "-" + name + '.txt', 'w', encoding='utf-8') as f:
                for i in content:
                    f.write(i.strip())
            f.close()

    # 实现主流程
    def run(self):
        url_list = self.get_url_list()
        for url in url_list:
            try:
                html = self.parse_url(url)
                self.save_news(html)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    qiye_spider = zixun_spider("%C6%F3%D2%B5%D7%CA%D1%B6", 2,"./企业资讯/")
    qiye_spider.run()
    # hangye_spider = zixun_spider("%D0%D0%D2%B5%D7%CA%D1%B6", 2, "./行业资讯/")
    # hangye_spider.run()
