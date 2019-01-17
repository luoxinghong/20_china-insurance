# -*- coding: utf-8 -*-
import requests
import re


class spider(object):
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36", }
        self.total_url_list = []
        self.tiaokuan_url_list = []

    # 获取保险小分类teamp_url_list[健康险，意外险，寿险，旅游险，财产险]
    def get_temp_url_list(self):
        content = requests.get(self.url, self.headers).content.decode()
        teamp_url_list = re.findall(r'<h4><a href="(.*?)" otitle="保险专题页-banner左侧导航栏-位置\d?', content)[0:5]
        teamp_url_list = ["http://www.pingan.com" + i for i in teamp_url_list]
        return teamp_url_list

    # 解析各小分类保险的详细页，得到每种保险的total_url_list
    def parse_temp_url(self, teamp_url_list):
        response = requests.get(teamp_url_list).content.decode()
        # 获得全部保险的总页数
        page_num = int(re.findall(r'<div class="page-total">共(\d)页</div>', response)[0])
        url_list = [teamp_url_list + "&pagenum=%d" % i for i in range(1, page_num + 1)]
        for url in url_list:
            html = requests.get(url, self.headers).content.decode()
            url_list = re.findall(
                r'<a class="prod-btn" href="(.*?)" target="_blank" otitle="保险列表页-产品列表-位置\d" otype="click" data-event-name="保险列表页-产品列表-位置\d',
                html)
            self.total_url_list = self.total_url_list + url_list
        return self.total_url_list

    # 保存保险详情页地址
    def save_data(self, total_url_list):
        with open("./中国平安保险详情页页地址.txt", "w") as f:
            for i, url in enumerate(total_url_list):
                f.write(url + "\n")
                html = requests.get(url).content
                html_name = re.findall(r'<title>(.*?)</title>', html.decode())[0]
                # 保存每种保险详情页的html页面
                with open("./html/{:0>3}_{}.html".format(i + 1, html_name),
                          "wb") as g:
                    g.write(html)
            f.close()
            g.close()

    # 解析各保险的详情页获取条款的url，并下载下来
    def download_tiaokuan(self, total_url_list):
        for i, url in enumerate(total_url_list):
            html = requests.get(url).content
            temp_tiaokuan_url = re.findall(r'href="(.*?.pdf)"', html.decode())
            self.tiaokuan_url_list = self.tiaokuan_url_list + temp_tiaokuan_url
        self.tiaokuan_url_list = sorted(set(self.tiaokuan_url_list), key=self.tiaokuan_url_list.index)
        # 去除不合规范的url
        self.tiaokuan_url_list = [i for i in self.tiaokuan_url_list if not i.startswith("../")]
        for i, url in enumerate(self.tiaokuan_url_list):
            # pdf_name = url.split("/")[-1]
            pdf_name = re.sub('[\/:*?"<>|]', '-', url.split("/")[-1])
            if url.startswith("/cshi-internet"):
                html = requests.get("https://health.pingan.com" + url).content
                with open("./pdf/{:0>3}_{}".format(i + 1, pdf_name), "wb") as f:
                    f.write(html)
                    f.close()
            elif url.startswith("/upload"):
                html = requests.get("http://baoxian.pingan.com" + url).content
                with open("./pdf/{:0>3}_{}".format(i + 1, pdf_name), "wb") as f:
                    f.write(html)
                    f.close()
            elif url.startswith("http"):
                html = requests.get(url).content
                with open("./pdf/{:0>3}_{}".format(i + 1, pdf_name), "wb") as f:
                    f.write(html)
                    f.close()
            else:
                print(url+"!!!download pdf fail")

    # 解析各险种的详情页，获取它的产品详情 、常见问题、重要声明等
    def get_details(self, total_url_list):
        pass

    def run(self):
        temp_url_list = self.get_temp_url_list()
        for temp_url in temp_url_list:
            total_url_list = self.parse_temp_url(temp_url)
        self.save_data(total_url_list)
        self.download_tiaokuan(total_url_list)
        print("success")


if __name__ == "__main__":
    url = "http://www.pingan.com/official/insurance"
    spider_taipingyang = spider(url)
    spider_taipingyang.run()
