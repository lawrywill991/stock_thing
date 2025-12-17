
import requests as req
import pandas as pd
import json as js
import sqlite3
import os

def dowload_stock_day_all():
     trade_record=req.get("https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL",verify="D:/python/twse_openapi.pem")
     print(trade_record)
     today_df = pd.DataFrame(trade_record.json())
     print(today_df['Date'].unique())
     return today_df

#-----為了把Json檔轉成db檔節省空間，先寫這段去手動整合執行(一步一步來比較妥當，之後再用for迴圈練習自動整合好了)-------------------------
#重設整個db檔的table(清空資料)
#測試GitHub加一行註解來試試看好了
def reset_table(empty_table):
     
     empty_db= ["Date","Code","Name","TradeVolume",
               "TradeValue","OpeningPrice",
               "HighestPrice","LowestPrice",
               "ClosingPrice","Change","Transaction"]
     empty_df = pd.DataFrame(columns=empty_db)
     with sqlite3.connect('stock.db') as conn:
          empty_df.to_sql(empty_table,conn,if_exists='replace',index=False)
          print(f'{empty_table}表格已重製，目前資料為空')
     with sqlite3.connect('stock.db') as conn:
          df = pd.read_sql_query(f'SELECT * FROM {empty_table}',con=conn)
          print(df)
#單純呼叫db的table，檢查檔案狀態用
def check_table(table_name):
     try:
         with sqlite3.connect('stock.db') as conn:
               df = pd.read_sql_query(f'SELECT * FROM {table_name} ',conn)
               # print(df['Date'].unique())
               print(f'{table_name}已有{df['Date'].unique()}資料合計{df['Date'].count()}筆')
     except pd.errors.DatabaseError:
           print(f'在stock_db中找不到{table_name} 表格')

#檢查json檔與是否存在，並試圖整合進DB檔的table中
def json_putinto_db(table_name,new_data):
     databaseError = False
     filenotFound = False
     #------讀取stock.db檔的table----
     try:
           with sqlite3.connect('stock.db') as conn:
                old_df = pd.read_sql_query(f'SELECT * FROM {table_name}',conn)
           print(old_df.tail(2))
     except pd.errors.DatabaseError:
           print(f'在stock_db中找不到{table_name} 表格')
           databaseError = True
     
     #------讀取json檔-----
     json_locate = os.path.join(r'E:\證交所API',new_data)+'.json'
     # print(json_locate)
     # print(os.path.exists(json_locate))
     try:
         with open(json_locate,"r",encoding='utf-8') as f1:
              data = js.load(f1)
         new_df = pd.DataFrame(data)
         print(new_df.tail(3))
     except FileNotFoundError:
          print(f'找不到{new_data}檔案')
          filenotFound = True
     #------整合df並選擇是否覆蓋存入-------
     if databaseError or filenotFound :
          print('df缺少,整合中止')
     else:
          if new_df['Date'].isin(old_df['Date']).any():
               print('新df與舊df重複,中止combine')
          else:
               print('新df不存在於舊df中，開始整合')
               combined_df = pd.concat([old_df,new_df],ignore_index=True)
               print('整合完畢，頭尾顯示如下')
               print(combined_df.head(1))
               print(combined_df.tail(1))
               save_db=input(f'是否覆蓋與存入{table_name}(Y/N)').upper()
               if save_db == 'Y':
                    combined_df.to_sql(table_name,conn,if_exists='replace',index=False)
                    print(f'{new_data}加入stock.db檔的{table_name}table中')
               else:
                    print(f'stock.db檔未存入{new_data}')

#將新下載的df整合進DB檔的table中
def today_addinto_db(table_name,today_df):
     tablenotfound = False
     try:
           with sqlite3.connect('stock.db') as conn:
                old_df = pd.read_sql_query(f'SELECT * FROM {table_name}',conn)
           print(old_df.tail(2))
           pd.read_sql

     except pd.errors.DatabaseError:
           print(f'在stock.db中找不到{table_name} 表格')
           tablenotfound = True
     if tablenotfound:
          print(f'stock.db沒有{table_name}表格,中止程式')
     else:
          if today_df['Date'].isin(old_df['Date']).any():
               print('今日資料與舊df重複,中止整合')
          else:
               print('今日資料不存在於舊df中，開始整合')
               combined_df = pd.concat([old_df,today_df],ignore_index=True)
               print('整合完畢，頭尾顯示如下')
               print(combined_df.head(1))
               print(combined_df.tail(1))
               save_db=input(f'是否覆蓋與存入{table_name}(Y/N)').upper()
               if save_db == 'Y':
                    combined_df.to_sql(table_name,conn,if_exists='replace',index=False)
                    print(f'{today_df}加入stock.db檔的{table_name}table中')
               else:
                    print(f'stock.db檔未存入{today_df}')

if __name__ == '__main__':
     # reset_table('stock_day_all')

     # present_data = input('請輸入整合stock.db檔中的table名稱:')
     # new_data = input('請輸入要加入的json檔名(E:\證交所API)')
     # json_putinto_db(present_data,new_data)

     check_table_name = input('請輸入檢查stock.db檔的表格名稱:')
     check_table(check_table_name)

     # present_data = input('請輸入整合stock.db檔中的table名稱:')
     # today_df=dowload_stock_day_all()
     # today_addinto_db(present_data,today_df)
     leave_program=input('請按下enter結束程式:')
#------以下是這程式第一版寫法(剛學到requests、pandas的時候寫的)-------------------------
# 存成json格式檔

#with open (f"E:/證交所API/交易價量{now}.json","a",encoding="UTF-8") as f:
#    js.dump(trade_record.json(),f,ensure_ascii=False)

#存成Excel檔 除了用pandas以外，還要pip openpyxl跟fsspec
# today_record=pd.DataFrame(trade_record.json())
# today_record.to_excel(f"D://python/{now}.xlsx",index=False,engine="openpyxl")

#存成csv檔
#today_record=pd.DataFrame(trade_record.json())
#today_record.to_csv(f"E:/證交所API/交易價量{now}.csv",index=False,encoding="utf-8-sig")
