import csv
import os
from pyecharts import WordCloud

'''
作者：pk哥
公众号：Python知识圈
日期：2018/09/19
代码解析详见公众号「Python知识圈」。

'''


def all_list(arr):
    result = {}
    for i in set(arr):
        result[i] = arr.count(i)
    return result


os.chdir('E:\\zufang')
with open('all.csv', 'rt', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    column = [row[1] for row in reader]
    result = all_list(column)
    result.pop('户型')    # 去掉字典中的无关信息

key = list(result.keys())
value = list(result.values())

wordcloud = WordCloud(width=1500, height=700)
wordcloud.add('', key, value, word_size_range=[20, 100])
wordcloud.render('E:\\pye\\style.html')   # 在指定目录下生成文件
