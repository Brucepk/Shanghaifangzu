import requests
from bs4 import BeautifulSoup
import csv
import time
import random

'''
作者：pk哥
公众号：Python知识圈
日期：2018/09/09
代码解析详见公众号「Python知识圈」。

'''
def get_html(url):
    # 用的代理 ip，如果被封的，在http://www.xicidaili.com/换一个
    proxy_addr = {'http': '61.135.217.7:80'}
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    try:
        html = requests.get(url, headers=headers, proxies=proxy_addr).text
        return html
    except BaseException:
        print('request error')
        pass


def RoomInfo(html):
    soup = BeautifulSoup(html, 'lxml')
    titles = soup.select('#house-lst div.info-panel h2 a')
    styles = soup.select('#house-lst div.info-panel div.col-1 div.where span.zone span')
    squares = soup.select('#house-lst div.info-panel div.col-1 div.where span.meters')
    prices = soup.select('#house-lst div.info-panel div.col-3 div.price span')
    data = []
    for ti, st, sq, pr, in zip(titles, styles, squares, prices):
        info = {}
        title = ti.get_text().strip()    # 出租房屋标题
        info['标题'] = title
        style = st.get_text().strip()    # 出租房屋户型
        info['户型'] = style
        square = sq.get_text().strip()[0:-2]   # 出租房屋面积
        info['面积（平方）'] = square
        price = pr.get_text().strip()    # 出租房屋房租
        info['房租（元/月）'] = price
        price_square = round(float(price)/float(square), 3)    # 出租房屋每平米房租
        info['每平方房租（元）'] = price_square
        data.append(info)
    return data


def write2csv(url, data):
    name = url.split('/')[-3]
    print('正在把数据写入{}文件'.format(name))    # 以链接中的地区拼音给文件命名
    with open('E:\\zufang\\{}.csv'.format(name), 'a', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['标题', '户型', '面积（平方）', '房租（元/月）', '每平方房租（元）']  # 控制列的顺序
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        print("写入成功")


def get_page_num(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    nums = soup.select('#content div.content__article p span.content__title--hl')
    for n in nums:
        total = int(n.get_text())
        if total < 30:
            num = 1
            return num
        else:
            num = total / 30
            if num > 100:
                num = 100
                return num
            else:
                return num


for area in ['pudong', 'minhang', 'baoshan', 'putuo', 'yangpu', 'changning', 'songjiang', 'jiading', 'huangpu',
             'jingan', 'zhabei', 'hongkou', 'qingpu', 'fengxian', 'jinshan', 'chongming', 'shanghaizhoubian',
             'ditiezufang', 'all']:
    base_url = 'https://sh.lianjia.com/zufang/{}/pg1/'.format(area)
    num = get_page_num(base_url)
    for page in range(1, int(num) + 1):
        url = 'https://sh.lianjia.com/zufang/{}/pg{}/'.format(area, page)
        html = get_html(url)
        data = RoomInfo(html)
        write2csv(url, data)
        time.sleep(int(format(random.randint(0, 5))))