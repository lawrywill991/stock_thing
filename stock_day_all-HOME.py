


import requests as req
import pandas as pd
import json as js

import os
import datetime
import sys
# print(sys.executable)


def find_key_series(data): #解出key_set(或稱key_series)
    key_series=[]
    for dict_list in data:
        for keys in dict_list:
            if keys not in key_series:
                key_series.append(keys)
    #print(key_set)
    return key_series

def find_value_set(data,key,key_set): #解出value_set
    value_set=[]
    if key in key_set:
        for dict_list in data:
            value=dict_list[key]
            if value not in value_set:
                value_set.append(value)
        return value_set
    else:
        return False

def find_value_series(data,key,key_set): #解出value_series
    key_value_series=[]
    if key in key_set:
        for dict_list in data:
            for keys in dict_list:
                if keys == key: 
                    value=dict_list[keys]
                    key_value_series.append(value)
        return key_value_series
    else:
        return False

def transform_to_df(data,key_set): #把解成的key_set與value_series組成dict
    transformed_data={}
    for keys in key_set:
        series =find_value_series(data,keys,key_set) 
        transformed_dict = {keys:series}
        transformed_data.update(transformed_dict)
    # print(transformed_data)
    return transformed_data

trade_record=req.get("https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL",verify="D:/python/twse_openapi.pem")
print(len(trade_record.text))
print(trade_record) #顯示API連線狀態
#print(type(trade_record.text))

#---解析data區: 重點是把list[dict] 轉成dict{key:list} 可以直接給pd轉df用------
data_list=js.loads(trade_record.text)#要給python解析前先用loads轉成正確資料型態:list
keys=find_key_series(data_list)
print(keys)
    #---利用解析過程順便確認資料日期是否正確-----------
data_date=find_value_set(data_list,'Date',keys)
print(f"本次data的日期有{len(data_date)}種，{data_date}")
if len(data_date) >1:
    print("資料有問題，先關閉程式不存檔")
    sys.exit(0)
print(type(data_date))
    #----這段轉成datetime的date類別其實沒做也可以運行拉，反正只是拿來當存檔檔名的。
date_str =data_date[0]
y = int(date_str[:3]) + 1911
m = int(date_str[3:5])
d = int(date_str[5:7])
data_date=datetime.date(y,m,d)
# print(f"本次資料內容為{data_date}的資料")
    #----正式組合成dict{key:list}-------------
tranformed_data = transform_to_df(data_list,keys)
df=pd.DataFrame(tranformed_data)
# print(df)
df['TradeVolume']=pd.to_numeric(df['TradeVolume'],errors="coerce")
df["TradeValue"]=pd.to_numeric(df['TradeVolume'],errors="coerce")
df["OpeningPrice"]=pd.to_numeric(df['OpeningPrice'],errors="coerce")
df["HighestPrice"]=pd.to_numeric(df['HighestPrice'],errors="coerce")
df["LowestPrice"]=pd.to_numeric(df['LowestPrice'],errors="coerce")
df["ClosingPrice"]=pd.to_numeric(df['ClosingPrice'],errors="coerce")
df["Transaction"]=pd.to_numeric(df['Transaction'],errors="coerce")
df["Change"]=pd.to_numeric(df['Change'],errors="coerce")
df["Date"]=pd.to_numeric(df["Date"],errors="coerce")
df["Date"]=df["Date"]+19110000
df["Date"]=pd.to_datetime(df["Date"].astype(str),format="%Y%m%d",
                          errors="coerce").dt.date

#------存檔區----要來解析data時直接用三引號全段註解掉就行---------

result_json = os.path.join(r'E:/證交所API',f'交易價量{data_date}.json')
result_csv = os.path.join(r'E:/證交所API',f'交易價量{data_date}.csv')
df=df

if os.path.exists(result_json) or os.path.exists(result_csv) :
    print('今天檔案已存在，程式結束')
    exit(0)

# 存成json格式檔

with open (f"E:/證交所API/交易價量{data_date}.json","a",encoding="UTF-8") as f:
    js.dump(trade_record.json(),f,ensure_ascii=False)
"""
#存成Excel檔 除了用pandas以外，還要pip openpyxl跟fsspec
df.to_excel(f"E:/證交所API/交易價量{data_date}.xlsx",index=False,engine="openpyxl")
"""
#存成csv檔

today_record=pd.DataFrame(trade_record.json())
today_record.to_csv(f"E:/證交所API/交易價量{data_date}.csv",index=False,encoding="utf-8-sig")
