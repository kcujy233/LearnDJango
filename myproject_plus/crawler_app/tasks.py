import os
import sys
import requests
from celery import shared_task
from django.conf import settings
import matplotlib.pyplot as plt
import re
import jieba
from lxml import etree
import matplotlib


def requ_for_web(job='', page=1, headers=None):
    qual_dict = {}
    salary_dict = {}
    stop_dict = {}

    # 定义请求参数
    params = {
        "keyword": job,  # 搜索关键词
        "page": page  # 搜索结果页数
    }
    # 发送GET请求，获取搜索结果页面的HTML代码
    response = requests.get("https://s.gxrc.com/sJob", params=params, headers=headers)
    html = response.text
    tree = etree.HTML(html)
    results = tree.xpath('//*[@id="posList"]/div[@class="rlOne"]')
    for result in results:
        # 获取职位
        job_title = result.xpath('./ul[1]/li[1]/h3/a/text()')[0]
        job_title = re.sub('（.*?）', '', job_title)
        seg_lst = jieba.cut(job_title)
        for stop_word in seg_lst:
            if stop_word in stop_dict:
                stop_dict[stop_word] += 1
            else:
                stop_dict[stop_word] = 1
        # 获取公司
        # company_name = result.xpath('./ul[1]/li[2]/a/text()')[0]
        # 获取工资
        try:
            salary = result.xpath('./ul[1]/li[3]/text()')[0]
        except:
            salary = "0"
        salary_min = int(re.search(r'(\d+)', salary)[0])
        if salary_min < 2:
            salary_min = 2
        elif salary_min == 11:
            salary_min = 10
        elif salary_min > 12 and salary_min < 15:
            salary_min = 12
        elif salary_min > 15 and salary_min < 20:
            salary_min = 15
        elif salary_min > 20:
            salary_min = 20
        salary_min = str(salary_min) + 'K/月'
        if salary_min in salary_dict:
            salary_dict[salary_min] += 1
        else:
            salary_dict[salary_min] = 1
        # 获取地址
        # job_address = result.xpath('./ul[1]/li[4]/text()')[0]
        # 获取学历
        try:
            qual = result.xpath('./ul[2]/li[2]/span/text()')[0]
        except:
            qual = "无"
        if qual in qual_dict:
            qual_dict[qual] += 1
        else:
            qual_dict[qual] = 1
        # print(
        #     f"岗位名称：{job_title}\n公司名称：{company_name}\n薪资：{salary}\n工作地点：{job_address}\n学历：{qual}\n")

    return qual_dict, salary_dict, stop_dict

@shared_task
def update_pie_chart_task():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    pages = 2
    qual_dict = {}
    for i in range(1, pages+5):
        qual_data, salary_data, stop_data = requ_for_web(page=i, headers=headers)
        qual_dict.update(qual_data)

    qual_labels = list(qual_dict.keys())
    qual_sizes = list(qual_dict.values())

    BASE_DIR = settings.BASE_DIR
    qual_chart_path = os.path.join(BASE_DIR, 'static/qual_pie_chart.png')

    plt.figure(figsize=(10, 6))
    plt.pie(qual_sizes, labels=qual_labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('企业对学历的要求')
    plt.savefig(qual_chart_path)
    plt.close()
