# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 14:48:33 2019

@author: z
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:34:39 2019

@author: z
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup

target_date = input("请输入要查询的舆情日期：(注意输入格式为yyyy-mm-dd)\n") ##输入你想获得的舆情日期
data_input = 'love'
theme_all = ''
while data_input != '':
    data_input= input("请输入要查询的关键字，如果有多个的话，每输一次按一下空格，如果输完所有关键词之后，再多按一下空格：\n")
    theme_all = theme_all+data_input+'+'
#input_data = input("请输入要查询的关键字，如果有多个的话，请在关键词之间按空格：\n") ##输入你想要的关键字，这里假定为平安。
wenjianjia = r'C:\Users\z\Desktop\朱老师探索性项目'
theme = theme_all[:-2]

info_final = []

uri = "http://search.caixin.com/search/search.jsp?special=false&keyword="+theme+"&channel=&type=1&sort=1&time=&startDate=&endDate=&page=1"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
           }

r1 = requests.get(url=uri, headers=headers)
response1 = r1.text
soup1 = BeautifulSoup(response1, 'html.parser')
try:
    total = int(soup1.find_all("div",{"class":"keyWordBox01"})[0].find_all("b")[1].get_text())
except IndexError:
    total = 0
times = int(total/20)+1

qingxi1 = lambda x:x.replace('[','').replace(']','').replace(' ','')
qingxi2 = lambda x:'……'+x+'……'
qingxi3 = lambda x:x.replace(' ','')


for i in range(1,times+1):
    url = "http://search.caixin.com/search/search.jsp?special=false&keyword="+theme+"&channel=&type=1&sort=1&time=&startDate=&endDate=&page=%s"%i
    r2 = requests.get(url=url, headers=headers)
    response2 = r2.text
    soup2 = BeautifulSoup(response2, 'html.parser')
    aim = soup2.find_all("div",{"class":"searchxt"})
#    date_first = aim[0].span.get_text().replace('[','').replace(']','').replace(' ','')
    try:
        date_first = aim[0].span.get_text().replace('[','').replace(']','').replace(' ','')
    except IndexError:
        continue   
    
    if target_date > date_first:
        break
    else:
        riqi = [date.span.get_text() for date in aim]
        riqi_final = pd.Series(riqi, name='发布日期').apply(qingxi3).apply(qingxi1) 
        title = [timu.a.get_text() for timu in aim]
        title_final = pd.Series(title, name='标题')
        short = [zhaiyao.p.get_text() for zhaiyao in aim]
        short_final = pd.Series(short, name='摘要').apply(qingxi2)
        wailian = [u.a.attrs["href"] for u in aim]  
        wailian_final = pd.Series(wailian, name='外链网址')
        info_first = pd.concat([riqi_final, title_final, short_final, wailian_final], axis=1)
        info1 = info_first[info_first['发布日期'] >= target_date]
        info1['关键词'] =theme
        print(info1)
        info_final.append(info1)
 
if len(info_final)==0:
    info_final_final = pd.DataFrame(columns=['发布日期','标题','摘要','外链网址','关键词'])   
else:    
    info_final_final = pd.concat(info_final)

info_order = info_final_final.sort_values(by=['发布日期'],ascending=False)
info_order.to_excel(wenjianjia+'\\从今天到'+target_date+'的，关键词为'+theme+'的平安舆情分析.xlsx', index=False)








