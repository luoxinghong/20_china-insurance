# -*- coding: utf-8 -*-
from lxml import etree
import requests
import re


class anli_spider(object):
    def __init__(self, subject_name_list, url_list):
        self.subject_name_list = subject_name_list
        self.url_list = url_list
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

    # 构造subject page列表
    def get_page_list(self, subject_url):
        html = self.parse_url(subject_url)
        page_number_str = etree.HTML(html).xpath("//td[@colspan='6']/text()")
        page_url_list = [subject_url + "&PageNo={}".format(i) for i in
                         range(1, int(re.findall("\d+", page_number_str[0])[0]) + 1)]
        return page_url_list

    # 发送请求，获取响应
    def parse_url(self, url):
        html = requests.get(url, headers=self.headers).content
        return html.decode("GBK", "ignore")

    # 实现主流程
    def run(self):
        for i, temp_url in enumerate(self.url_list):
            try:
                path = "./案例/" + subject_name_list[i] + "/"
                page_url_list = self.get_page_list(temp_url)
                print(page_url_list)
                print("page_url_list   changdu", len(page_url_list))
                for j in page_url_list:
                    print('当前页数', j)
                    html = self.parse_url(j)
                    news_url_list = etree.HTML(html).xpath("//a[contains(@href,'/news-center/newslist.asp?id=')]/@href")
                    for k in news_url_list:
                        content = self.parse_url("http://www.china-insurance.com" + k)
                        date = re.findall(r'\d*', etree.HTML(content).xpath("//tr[@bgcolor='EEF5FF']/td/text()")[0])
                        date = date[2] + '{:0>2}'.format(date[4]) + '{:0>2}'.format(date[6])
                        name = etree.HTML(content).xpath("//p[@class='f20b']/text()")[0]
                        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
                        name = re.sub(rstr, "_", name)
                        text = etree.HTML(content).xpath("//font[@id='zoom']//text()")
                        with open(path + date + "-" + name + '.txt', 'w', encoding='utf-8') as f:
                            for i in text:
                                f.write(i.strip())
                        f.close()
                        print(k)
            except Exception as e:
                print(e)
            continue


if __name__ == "__main__":
    subject_name_list = ["产险案例", "寿险案例", "保险与欺诈", "热点追踪", "相关案例"]
    url_list = ["http://www.china-insurance.com/case/moreItem.asp?subject=%B1%A3%CF%D5%B0%B8%C0%FD&zsid={}".format(i)
                for i in range(11, 16)]
    spider = anli_spider(subject_name_list, url_list)
    spider.run()
