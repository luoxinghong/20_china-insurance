# -*- coding: utf-8 -*-
import os
from lxml import etree
import shutil
import requests
from urllib.request import quote, unquote


def parse_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    }
    html = requests.get(url, headers=headers).content
    return html.decode("GBK", "ignore")


def make_folders(folders_list):
    for path in folders_list:
        folder = os.path.exists(path)
        if not folder:
            os.mkdir(path)
        else:
            shutil.rmtree(path)
            os.mkdir(path)


# 获取保险大分类url_list，创建对应的文件夹
def get_insurance_type_and_mkdir(url):
    html = parse_url(url)
    insurance_type_url_list = etree.HTML(html).xpath('//a[@target="_self"]/@href')
    insurance_type_folder_list = [i.split("=")[-1] for i in insurance_type_url_list]
    insurance_type_folder_list.remove("综合保险")
    url_list = ["http://www.china-insurance.com/xianzhongdaquan/xianzhongcx.asp?id=" + quote(i, encoding='gbk') for i in
                insurance_type_folder_list]
    insurance_type_folder_list = ['./人身保险大全/' + str(insurance_type_folder_list.index(i)) + i for i in
                                  insurance_type_folder_list]
    make_folders(insurance_type_folder_list)
    return insurance_type_folder_list, url_list


# 获取每种分类所有保险的id和险种产品名称
def get_insurance_url(url):
    html = parse_url(url)
    total_insurance_number = etree.HTML(html).xpath("//font[@color='#ff0000']/text()")[0]

    if (int(total_insurance_number) % 25) != 0:
        page_number = int(total_insurance_number) // 25 + 1
    else:
        page_number = int(total_insurance_number) // 25

    page_url_list = []

    for i in range(1, page_number + 1):
        page_url = url + "&page={}".format(i)
        page_url_list.append(page_url)
    insurance_total_url_List = []
    insurance_total_url_name = []
    for j in page_url_list:
        html = parse_url(j)
        temp_insurance_total_url_List = etree.HTML(html).xpath('//a[contains(@href,"xiangxitiaokuan.asp?id=")]/@href')
        temp_insurance_total_url_List = [i.split("=")[-1][:-2] for i in temp_insurance_total_url_List]
        insurance_total_url_List = insurance_total_url_List + temp_insurance_total_url_List

        temp_insurance_total_url_name = etree.HTML(html).xpath('//a[contains(@href,"chanpin.asp?id=")]/text()')
        insurance_total_url_name = insurance_total_url_name + temp_insurance_total_url_name
    return insurance_total_url_List, insurance_total_url_name


def save_clause_text(insurance_total_url_List, insurance_total_url_name, i):
    url_list = ["http://www.china-insurance.com/xianzhongdaquan/xiangxitiaokuan.asp?id={}".format(i) for i in
                insurance_total_url_List]
    for j, url in enumerate(url_list):
        html = parse_url(url)
        content = etree.HTML(html).xpath("//div[@style='overflow:auto;height:310;']/text()")
        print(url + " is saving")
        with open(insurance_type_folder_list[i] + "/" + "{:0>3}_".format(j) + insurance_total_url_name[j] + ".txt", "w",
                  encoding='utf-8') as f:
            for j in content:
                f.write(j)
            f.close()


if __name__ == '__main__':

    insurance_type_folder_list, url_list = get_insurance_type_and_mkdir(
        "http://www.china-insurance.com/xianzhongdaquan/xianzhongcx.asp?id=%B1%A3%D5%CF%B1%A3%CF%D5")
    for i, url in enumerate(url_list):
        insurance_total_url_List, insurance_total_url_name = get_insurance_url(url)
        save_clause_text(insurance_total_url_List, insurance_total_url_name, i)
