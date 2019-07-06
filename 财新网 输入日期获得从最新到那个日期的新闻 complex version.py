# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:34:39 2019

@author: z
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup

target_date = input("请输入要查询的舆情日期：(注意输入格式为yyyy-mm-dd)\n") ##输入你想获得的舆情日期
#input_data = input("请输入要查询的关键字，如果有多个的话，请在关键词之间按空格：\n") ##输入你想要的关键字，这里假定为平安。
wenjianjia = r'C:\Users\z\Desktop\朱老师探索性项目'
address = wenjianjia+'\\小boss词库.xlsx'
ciku = pd.read_excel(address)
yijiciku = ciku.iloc[:,0].dropna()
erjiciku = ciku.iloc[:,1].dropna()
zuizhongciku = []
for i,j in enumerate(yijiciku):
    l1 = []
    for m,n in enumerate(erjiciku):
        g1 = j+'+'+n
        l1.append(g1)
    zuizhongciku.append(pd.Series(l1))
zuizhongciku = pd.concat(zuizhongciku)



info_final = []
for n,theme in enumerate(zuizhongciku):
    uri = "http://search.caixin.com/search/search.jsp?special=false&keyword="+theme+"&channel=&type=1&sort=1&time=&startDate=&endDate=&page=1"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
               }
    
    r1 = requests.get(url=uri, headers=headers)
    response1 = r1.text
    soup1 = BeautifulSoup(response1, 'html.parser')
    try:
        total = int(soup1.find_all("div",{"class":"keyWordBox01"})[0].find_all("b")[1].get_text())
    except IndexError:
        continue
    
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
        try:
            date_first = aim[0].span.get_text().replace('[','').replace(']','').replace(' ','')
        except IndexError:
            continue
        
        if target_date > date_first:
            break
        else:
            riqi = [date.span.get_text() for date in aim]
            riqi_final = pd.Series(riqi, name='发布日期').apply(qingxi1) 
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
 

info_final_final = pd.concat(info_final).drop_duplicates()
info_order = info_final_final.sort_values(by=['发布日期','关键词'],ascending=False)

haha = info_order.groupby(['外链网址'])
final = []
redact = []
for a,b in haha:
    if haha['外链网址'].count()[a]==1:
        final.append(b)
    else:
        redact.append(b)
v1 = lambda x:x+'//'

v2 = lambda x:x+'、' 

for i,j in enumerate(redact):
    redact[i]['摘要'] = j['摘要'].apply(v1)
    redact[i]['关键词'] = j['关键词'].apply(v2)

def sum1(series):
    series1 = series.drop_duplicates().reset_index(drop=True)
    for i,j in enumerate(series1):
        if i==0:
            a1 = j
        else:
            a2 = j
            a1 = a1+a2
    a3 = a1[:-1]
    return(a3)


def sum2(series):
    series1 = series.drop_duplicates().reset_index(drop=True)
    for i,j in enumerate(series1):
        if i==0:
            a1 = j
        else:
            a2 = j
            a1 = a1+a2
    a3 = a1[:-2]
    return(a3)

redactor = []
for m,n in enumerate(redact):
    u = n.reset_index(drop=True)
    u['关键词'][0] = sum1(u['关键词']) 
    u['摘要'][0] =sum2(u['摘要'])
    redactor.append(u.loc[0].to_frame().T)

final1 = pd.concat(final)
if len(redactor) != 0:
    redact1 = pd.concat(redactor)
    allinall = pd.concat([final1, redact1])
else:
    allinall = final1
final = allinall.sort_values(by=['发布日期','关键词'],ascending=False)
final['摘要'] = final['摘要'].apply(qingxi3)
final.to_excel(wenjianjia+'\\从今天到'+target_date+'的平安舆情分析.xlsx', index=False)








