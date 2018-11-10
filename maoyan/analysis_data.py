# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 10:53:46 2018

@author: wufan
"""
from os import path
import csv
from pyecharts import Pie
from pyecharts import Bar
from pyecharts import Line
from pyecharts import Geo
from collections import Counter
import jieba
import re
import json
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt





#定义个函数式用于分词
def jiebaclearText(text):
    #定义一个空的列表，将去除的停用词的分词保存
    mywordList=[]
    #通过正则表达式替换掉逗号，句号以及换行回车
    text = re.sub('[,，。. \r\n]', '', text)
    #进行分词,cut_all=False精确模式分词
    seg_list=jieba.cut(text,cut_all=False)
    #将一个generator的内容用/连接
    listStr='/'.join(seg_list)
    #把影替换掉
    listStr = listStr.replace("影", "")
    #打开停用词表
    f_stop=open(stopwords_path,encoding="utf8")
    #读取
    try:
        f_stop_text=f_stop.read()
    finally:
        f_stop.close()#关闭资源
    #将停用词格式化，用\n分开，返回一个列表
    f_stop_seg_list=f_stop_text.split("\n")
    #对默认模式分词的进行遍历，去除停用词
    for myword in listStr.split('/'):
        #去除停用词，如果改分词拆分不在停词表里且他去掉空格后的长度大于1，保存改词
        if not(myword.split()) in f_stop_seg_list and len(myword.strip())>1:
            mywordList.append(myword)
            #将他们以空格相连输出字符串
    return ' '.join(mywordList)

# 生成词云图
def make_wordcloud(dir,text1,bgimage):
    #把电影名字去掉
    text1 = text1.replace("影", "")
    #载入背景图
    bg = plt.imread(bgimage)
    # 生成

    wc = WordCloud(# FFFAE3
        background_color="white",  # 设置背景为白色，默认为黑色
        width=890,  # 设置图片的宽度
        height=600,  # 设置图片的高度
        mask=bg,
        # margin=10,  # 设置图片的边缘
        max_font_size=150,  # 显示的最大的字体大小
        random_state=50,  # 为每个单词返回一个PIL颜色
        font_path=dir+r'/static/simkai.ttf'  # 中文处理，用系统自带的字体
    ).generate_from_text(text1)
    #显示彩色图
    plt.figure()
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    #根据mask图显示
    bg_color = ImageColorGenerator(bg)
    
    plt.figure()
    plt.imshow(wc.recolor(color_func=bg_color))
    plt.axis("off")
    plt.show()
	# 保存云图
    wc.to_file(dir+r"/word_cloud.png")

    
    







# 每日评论总数可视化分析
def time_num_visualization(dir,time): 
    time_list = list(set(time))
    time_dict = {time_list[i]: 0 for i in range(len(time_list))}
    time_num = []
    for i in range(len(time_list)):
        time_dict[time_list[i]] = time.count(time_list[i])
    # 根据数量(字典的键值)排序
    sort_dict = sorted(time_dict.items(), key=lambda d: d[0], reverse=False)
    time_name = []
    time_num = []
    print(sort_dict)
    for i in range(len(sort_dict)):
        time_name.append(sort_dict[i][0])
        time_num.append(sort_dict[i][1])

    line = Line("评论数量日期折线图")
    line.add(
        "日期-评论数",
        time_name,
        time_num,
        is_fill=True,
        area_color="#000",
        area_opacity=0.3,
        is_smooth=True,
    )
    line.render(dir+"\line.html")

    
# 评论者猫眼等级、评分可视化
def level_score_visualization(dir,userLevel,score):

    userLevel_list = list(set(userLevel))#去重
    userLevel_num = []
    #计每一个评价的分数
    for i in range(len(userLevel_list)):
        userLevel_num.append(userLevel.count(userLevel_list[i]))

    score_list = list(set(score))
    score_num = []
    for i in range(len(score_list)):
        score_num.append(score.count(score_list[i]))

    pie01 = Pie("等级环状饼图", title_pos='center', width=900)
    pie01.add(
        "等级",
        userLevel_list,
        userLevel_num,
        radius=[40, 75],
        label_text_color=None,
        is_label_show=True,
        legend_orient="vertical",
        legend_pos="left",
    )
    pie01.render(dir+r"\level_pie.html")
    pie02 = Pie("评分玫瑰饼图", title_pos='center', width=900)
    pie02.add(
        "评分",
        score_list,
        score_num,
        center=[50, 50],
        is_random=True,
        radius=[30, 75],
        rosetype="area",
        is_legend_show=False,
        is_label_show=True,
    )
    pie02.render(dir+r"\score_pie.html")    

#读取csv内容   
def read_csv(filelocation):
    content = ''
    # 读取文件内容
    with open(filelocation, 'r', encoding='utf_8_sig', newline='') as file_test:
        # 读文件
        reader = csv.reader(file_test)
        i = 0
        for row in reader:
            if i != 0:
                ####把数据分解读到相应的list
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
def sex_distribution(dir,gender):
    # print(gender)

    list_num = []
    list_num.append(gender.count('0')) # 未知
    list_num.append(gender.count('1')) # 男
    list_num.append(gender.count('2')) # 女
    attr = ["其他","男","女"]
    pie = Pie("性别饼图")
    pie.add("", attr, list_num, is_label_show=True)
    pie.render(dir+r"\sex_pie.html")   

# 评论者所在城市分布可视化
def city_distribution(dir,cityName):
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
    bar.render(dir+r"\city_bar.html")

def render_city(dir,cities):
    # 对城市数据和坐标文件中的地名进行处理
    handle(cities)
    # 使用Counter类统计出现的次数，并转换为元组列表
    data = Counter(cities).most_common()  
#    print(data)
    
    geo = Geo("电影《影》观众分布", title_color="#fff",
          title_pos="center", width=1200,
          height=600, background_color='#404a59')
    attr, value = geo.cast(data)
    geo.add("", attr, value, visual_range=[0, 600], visual_text_color="#fff",
            symbol_size=15, is_visualmap=True)
    geo.render(dir+r"\geo.html")

#处理echart地图库
def handle(cities):
    # 获取坐标文件中所有地名
    data = None
    with open('C:/ProgramData/Anaconda3/envs/py37/Lib/site-packages/pyecharts/datasets/city_coordinates.json',mode='r', encoding='utf-8') as f:
        data = json.loads(f.read())  # 将str转换为json

    # 循环判断处理
    data_new = data.copy()  # 拷贝所有地名数据
    for city in set(cities):  # 使用set去重
        # 如果地名为空将它移除
        if city == '':
            while city in cities:
                cities.remove(city)                                         
        #在原数据集中遍历城市名，如果不存在，剔除它                
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
        if count == len(data):
            while city in cities:
                cities.remove(city)
    #前后对比           
    # print(len(data), len(data_new))
    # 写入覆盖坐标文件
    with open(r'C:/ProgramData/Anaconda3/envs/py37/Lib/site-packages/pyecharts/datasets/city_coordinates.json',mode='w', encoding='utf-8') as f:
        f.write(json.dumps(data_new, ensure_ascii=False))  # 将json转换为str

if __name__ == '__main__':
    #变量初始化
    #当前文件路径
    dir = path.dirname(__file__)
    filelocation=dir+r'/maoyan.csv'
    #停用词路径，需要事先准备好停用词
    bgimage=dir + r"/static/poster_v1.png"
    stopwords_path = dir+r'/static/stopwords.txt'
    time = []
    nickName = []
    gender = []
    cityName = []
    userLevel = []
    score = []
    content = ''
    #函数开始执行
    content=read_csv(filelocation)
    #性别分布
#    sex_distribution(dir,gender)
#    #城市分布，柱状图
#    city_distribution(dir,cityName)
#    #城市分布，地理图
#    render_city(dir,cityName)
#    #时间分布，柱状图
#    time_num_visualization(dir,time)
#    #评论分数，评论级别分布，饼图
#    level_score_visualization(dir,userLevel,score)
    #生成词云
    text=jiebaclearText(content)
    #画图
    make_wordcloud(dir,text,bgimage)