# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 10:53:46 2018

@author: wufan
"""

import csv
from pyecharts import Pie
from pyecharts import Bar

from pyecharts import Style
from pyecharts import Geo
import json
from collections import Counter


filelocation=r'C:\Git\maoyan\maoyan.csv'
time = []
nickName = []
gender = []
cityName = []
userLevel = []
score = []
content = ''

def read_csv():
    content = ''
    # 读取文件内容
    with open(filelocation, 'r', encoding='utf_8_sig', newline='') as file_test:
        # 读文件
        reader = csv.reader(file_test)
        i = 0
        for row in reader:
            if i != 0:
                time.append(row[0])
                nickName.append(row[1])
                gender.append(row[2])
                cityName.append(row[3])
                userLevel.append(row[4])
                score.append(row[5])
                content = content + row[6]
                # print(row)
            i = i + 1
        print('一共有：' + str(i - 1) + '条数据')
        return content

# 评论者性别分布可视化
def sex_distribution(gender):
    # print(gender)

    list_num = []
    list_num.append(gender.count('0')) # 未知
    list_num.append(gender.count('1')) # 男
    list_num.append(gender.count('2')) # 女
    attr = ["其他","男","女"]
    pie = Pie("性别饼图")
    pie.add("", attr, list_num, is_label_show=True)
    pie.render("C:\Git\maoyan\sex_pie.html")   

# 评论者所在城市分布可视化
def city_distribution(cityName):
	city_list = list(set(cityName))
	city_dict = {city_list[i]:0 for i in range(len(city_list))}
	for i in range(len(city_list)):
		city_dict[city_list[i]] = cityName.count(city_list[i])
	# 根据数量(字典的键值)排序
	sort_dict = sorted(city_dict.items(), key=lambda d: d[1], reverse=True)
	city_name = []
	city_num = []
	for i in range(len(sort_dict)):
		city_name.append(sort_dict[i][0])
		city_num.append(sort_dict[i][1])
	

	bar = Bar("评论者城市分布")
	bar.add("", city_name, city_num, is_label_show=True, is_datazoom_show=True)
	bar.render("C:\Git\maoyan\city_bar.html")


def render_city(cities):
    # 对城市数据和坐标文件中的地名进行处理
    handle(cities)
    data = Counter(cities).most_common()  # 使用Counter类统计出现的次数，并转换为元组列表
    print(data)

    # 定义样式
    style = Style(
        title_color='#fff',
        title_pos='center',
        width=1200,
        height=600,
        background_color='#404a59'
    )

    # 根据城市数据生成地理坐标图
    geo = Geo('《影》粉丝位置分布',  **style.init_style)
    attr, value = geo.cast(data)
    geo.add('', attr, value, visual_range=[0, 600],
            visual_text_color='#fff', symbol_size=15,
            is_visualmap=True, is_piecewise=True, visual_split_number=10)
    geo.render("C:\Git\maoyan\geo.html")

def handle(cities):
    # 获取坐标文件中所有地名
    data = None
    with open('C:/ProgramData/Anaconda3/envs/py37/Lib/site-packages/pyecharts/datasets/city_coordinates.json',mode='r', encoding='utf-8') as f:
        data = json.loads(f.read())  # 将str转换为json

    # 循环判断处理
    data_new = data.copy()  # 拷贝所有地名数据
    for city in set(cities):  # 使用set去重
        # 处理地名为空的数据
        if city == '':
            while city in cities:
                cities.remove(city)
                
                
                
                
                
        count = 0
        for k in data.keys():
            count += 1
            if k == city:
                break
            if k.startswith(city):  # 处理简写的地名，如 达州市 简写为 达州
                # print(k, city)
                data_new[city] = data[k]
                break
            if k.startswith(city[0:-1]) and len(city) >= 3:  # 处理行政变更的地名，如县改区 或 县改市等
                data_new[city] = data[k]
                break
            
            
        # 处理不存在的地名
        if count == len(data):
            while city in cities:
                cities.remove(city)

    # print(len(data), len(data_new))

    # 写入覆盖坐标文件
    with open(r'C:/ProgramData/Anaconda3/envs/py37/Lib/site-packages/pyecharts/datasets/city_coordinates.json',mode='w', encoding='utf-8') as f:
        f.write(json.dumps(data_new, ensure_ascii=False))  # 将json转换为str

i=0
for city in set(cityName):
    i+=1
print(i)

if __name__ == '__main__':
   read_csv()
#   sex_distribution(gender)
#   city_distribution(cityName)
   render_city(cityName)