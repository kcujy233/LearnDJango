
from django.http import HttpResponse, HttpRequest
import re
import jieba
from wordcloud import WordCloud
import requests
from lxml import etree
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from django.template import loader

matplotlib.rc("font", family='YouYuan')

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

def update_pie_chart(request: HttpRequest, page: int) -> HttpResponse:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    qual_dict = {}
    salary_dict = {}
    stop_dict = {}

    for i in range(1, page+1):
        qual_data, salary_data, stop_data = requ_for_web(page=i, headers=headers)
        qual_dict.update(qual_data)
        salary_dict.update(salary_data)
        stop_dict.update(stop_data)

    # 标签 (字典的键)
    qual_labels = qual_dict.keys()
    salary_labels = salary_dict.keys()
    # 数值 (字典的值)
    qual_sizes = qual_dict.values()
    salary_sizes = salary_dict.values()
    BASE_DIR = os.path.abspath('.')
    '''学历图'''
    plt.figure(figsize=(10, 6))  # 设置画布大小
    plt.pie(qual_sizes, labels=qual_labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('企业对学历的要求')
    qual_chart_path = os.path.join(BASE_DIR, 'static/qual_pie_chart.png')
    plt.savefig(qual_chart_path)
    plt.close()

    '''薪资图'''
    plt.figure(1)
    plt.figure(figsize=(10, 6))  # 设置画布大小
    plt.pie(salary_sizes, labels=salary_labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title("最低薪资占比")
    salary_chart_path = os.path.join(BASE_DIR, 'static/salary_pie_chart.png')
    plt.savefig(salary_chart_path)
    plt.close()

    '''词云图'''
    # 创建WordCloud对象，并设置参数
    wc = WordCloud(font_path='C:/Windows/Fonts/等线/Deng.ttf', width=800, height=400)
    # 从字典生成词云
    wc.generate_from_frequencies(stop_dict)
    # 保存词云图
    wordcloud_path = os.path.join(BASE_DIR, 'static/wordcloud.png')
    wc.to_file(wordcloud_path)
    # wc.to_file('crawler_app/static/wordcloud.png')
    page_options = range(1, 51)
    template = loader.get_template('update_pie_chart.html')
    context = {
        'qual_chart': '/static/qual_pie_chart.png',
        'salary_chart': '/static/salary_pie_chart.png',
        'wordcloud': '/static/wordcloud.png',
        'page_options': page_options,
    }
    return HttpResponse(template.render(context, request))

def detail_page(request: HttpRequest) -> HttpResponse:
    pages = request.GET.get('pages', 2)  # 默认为2，如果没有提供参数
    pages = int(pages)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    qual_data, salary_data, stop_data = requ_for_web(page=pages, headers=headers)
    qual_dict = qual_data  # 将返回的数据赋值给对应的字典
    salary_dict = salary_data
    stop_dict = stop_data
    # 标签 (字典的键)
    qual_labels = qual_dict.keys()
    salary_labels = salary_dict.keys()
    # 数值 (字典的值)
    qual_sizes = qual_dict.values()
    salary_sizes = salary_dict.values()
    BASE_DIR = os.path.abspath('.')
    '''学历图'''
    plt.figure(figsize=(10, 6))  # 设置画布大小
    plt.pie(qual_sizes, labels=qual_labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('企业对学历的要求')
    qual_chart_path = os.path.join(BASE_DIR, 'static/qual_pie_chart_select.png')
    plt.savefig(qual_chart_path)
    plt.close()
    # plt.savefig('crawler_app/static/qual_pie_chart.png')  # 保存学历图

    '''薪资图'''
    plt.figure(1)
    plt.figure(figsize=(10, 6))  # 设置画布大小
    plt.pie(salary_sizes, labels=salary_labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title("最低薪资占比")
    salary_chart_path = os.path.join(BASE_DIR, 'static/salary_pie_chart_select.png')
    plt.savefig(salary_chart_path)
    plt.close()
    # plt.savefig('crawler_app/static/salary_pie_chart.png')  # 保存薪资图

    '''词云图'''
    # 创建WordCloud对象，并设置参数
    wc = WordCloud(font_path='C:/Windows/Fonts/等线/Deng.ttf', width=800, height=400)
    # 从字典生成词云
    wc.generate_from_frequencies(stop_dict)
    # 保存词云图
    wordcloud_path = os.path.join(BASE_DIR, 'static/wordcloud_select.png')
    wc.to_file(wordcloud_path)
    template = loader.get_template('detail_page.html')
    context = {
        'qual_chart': '/static/qual_pie_chart_select.png',
        'salary_chart': '/static/salary_pie_chart_select.png',
        'wordcloud': '/static/wordcloud_select.png',
    }
    return HttpResponse(template.render(context, request))