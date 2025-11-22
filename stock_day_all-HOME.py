

import requests as req
import pandas as pd
# import schedule
import time
import json as js

# trade_record=req.get("https://openapi.twse.com.tw/v1/exchangeReport/MI_5MINS",verify=False)
now=time.strftime("%Y-%m-%d",time.localtime())
print(now)
trade_record=req.get("https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL",verify="D:/python/twse_openapi.pem")
print(trade_record)

# 存成json格式檔
with open (f"E:/證交所API/交易價量{now}.json","a",encoding="UTF-8") as f:
    js.dump(trade_record.json(),f,ensure_ascii=False)
#存成Excel檔 除了用pandas以外，還要pip openpyxl跟fsspec
# today_record=pd.DataFrame(trade_record.json())
# today_record.to_excel(f"D://python/{now}.xlsx",index=False,engine="openpyxl")

#存成csv檔
today_record=pd.DataFrame(trade_record.json())
today_record.to_csv(f"E:/證交所API/交易價量{now}.csv",index=False,encoding="utf-8-sig")