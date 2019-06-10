## -*- coding: utf-8 -*-
#"""
#Created on Thu Jun  6 09:56:41 2019
#
#@author: z
#"""
import requests
import pandas as pd
import time
target_date = '2015-06-01' ##输入你想获得最早的新闻日期
input_data = "平安证券" ##输入你想要的关键字，这里假定为平安。
theme = input_data.replace(" ","+")

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'}
uri1 = "https://api.wallstreetcn.com/apiv1/search/article?query="+theme+"&order_type=time&cursor=1"
r = requests.get(uri1, headers=headers)
r.encoding = r.apparent_encoding
response = r.text
json_data = r.json()

for key, value in json_data.items():
    if key == 'data':
        raw_data = value['items']
        Count = value['count']
times = int(Count/100)+1 ##如果cursor的值加一，根据访问uri1获得的新数据为100个，故根据变量Count的结果获取要遍历的次数，注意此处cursor的值不是0-indexed的

info = []
for g in range(1, times+1):
    urit = "https://api.wallstreetcn.com/apiv1/search/article?query="+theme+"&order_type=time&cursor=%i"%g 
    r1 = requests.get(urit, headers=headers)
    r1.encoding = r1.apparent_encoding
    response1 = r1.text
    json_data1 = r1.json()
    for key, value in json_data1.items():
        if key == 'data':
            raw_data1 = value['items']
    buchongzuozhe = [x['author']['display_name'] for x in raw_data1]
    biaoti = [x['title'] for x in raw_data1]
    laiyuan = [x['source_name'] for x in raw_data1]
    zhaiyao = [x['content_short'] for x in raw_data1]
    wailian = [x['uri'] for x in raw_data1]
    weichulishijian = [x['display_time'] for x in raw_data1]
    
    for i,j in enumerate(laiyuan):
        if j == "":
            laiyuan[i] = buchongzuozhe[i]
    
    data1 = pd.concat([pd.Series(weichulishijian),pd.Series(biaoti), pd.Series(laiyuan), pd.Series(zhaiyao), pd.Series(wailian)], axis=1)
    
    qingli2 = lambda x:x.replace("<em>","").replace("</em>","").replace("\\x26quot;","").replace("\\x26gt;","").replace("\\x0a","").lstrip()
    data1[1] = data1[1].apply(qingli2)    
    data1[3] = data1[3].apply(qingli2)
    
    def tiaoxi(x):
        if len(x)<=5:
            x = ""
        return(x)   
    data1[3] = data1[3].apply(tiaoxi)
    
    qingli3 = lambda x:time.strftime("%Y-%m-%d", time.localtime(x))
    data1[0] = data1[0].apply(qingli3)
    
    index1 = data1[data1[4].str.contains('api')].index
    data2 = data1.drop(index1)
    data3 = data2.reset_index(drop=True)
    info.append(data3)
    ###########################################################################################   
    ##确认日期
    date_last = data1.iloc[-1,0]
    if date_last < target_date:
        break

info_all = pd.concat(info).reset_index(drop=True)
info_final = info_all[info_all[0]>=target_date]
info_final.columns = ['发布日期', '标题', '来源', '摘要', '外链']
mulu = 'C://Users//z//Desktop//朱老师探索性项目'
dizhi= mulu+'//关键字为'+input_data+',起始时间为'+target_date+'的华尔街见闻新闻.xlsx'
info_final.to_excel(dizhi, index=False)



  

