#這是AI編寫(ROO CODE)的程式碼，我都要放在vibe虛擬環境比較安全

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime, timedelta

# 假設原始的資料夾路徑
folder_path = 'E:/證交所API' # 請根據實際情況修改

def run_analysis(start_date_str, end_date_str, target_code):
    #擷取個股在時間區間的價格資料轉成另一個表格
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("輸入錯誤", "日期格式不正確，請使用 YYYY-MM-DD 格式。")
        return None

    matched_rows = []
    current_date = start_date
    while current_date <= end_date:
        filename = f"交易價量{current_date.strftime('%Y-%m-%d')}.csv"
        file_path = os.path.join(folder_path, filename)

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                if 'Code' in df.columns:
                    matched_row = df[df['Code'] == target_code]
                    if not matched_row.empty:
                        matched_row = matched_row.copy()
                        matched_row['來源日期'] = current_date.strftime('%Y-%m-%d')
                        
                        # 計算漲跌
                        if 'OpeningPrice' in matched_row.columns and 'ClosingPrice' in matched_row.columns:
                            open_price = pd.to_numeric(matched_row['OpeningPrice'], errors='coerce')
                            close_price = pd.to_numeric(matched_row['ClosingPrice'], errors='coerce')
                            matched_row['漲跌'] = ((close_price - open_price) / open_price * 100).round(2)
                        else:
                            matched_row['漲跌'] = None # 或其他預設值

                        # 計算極限
                        if 'LowestPrice' in matched_row.columns and 'HighestPrice' in matched_row.columns:
                            lowest_price = pd.to_numeric(matched_row['LowestPrice'], errors='coerce')
                            highest_price = pd.to_numeric(matched_row['HighestPrice'], errors='coerce')
                            matched_row['極限'] = ((lowest_price - highest_price) / lowest_price * 100).round(2)
                        else:
                            matched_row['極限'] = None # 或其他預設值

                        matched_rows.append(matched_row)
                    else:
                        messagebox.showwarning("查詢結果", f"在 {filename} 找不到代號 {target_code}")
                else:
                    messagebox.showwarning("檔案錯誤", f"{filename} 中沒有 'Code' 欄位")
            except Exception as e:
                messagebox.showerror("讀取錯誤", f"讀取檔案 {filename} 時發生錯誤：{e}")
        else:
            # 判斷是否為週末 (週六或週日)
            if current_date.weekday() >= 5: # 0=星期一, 5=星期六, 6=星期日
                # 是假日，跳過，不顯示任何訊息
                pass
            else:
                # 非假日但檔案不存在，顯示訊息
                print(f"檔案不存在：{filename}")
                #這個直接執行程式碼的話print會顯示在cmd視窗。
        current_date += timedelta(days=1)

    if matched_rows:
        result_df = pd.concat(matched_rows, ignore_index=True)
        return result_df
    else:
        return None

def show_results_window(result_df):
    
    #在新視窗中以表格形式顯示查詢結果。
    result_window = tk.Toplevel()
    result_window.title("查詢結果")
    result_window.geometry("800x600") # 設定視窗大小

    if result_df is not None and not result_df.empty:
        # 創建 Treeview
        tree = ttk.Treeview(result_window, show="headings")
        tree.pack(side="left", fill="both", expand=True)

        # 添加滾動條
        vsb = ttk.Scrollbar(result_window, orient="vertical", command=tree.yview)
        vsb.pack(side="right", fill="y")
        tree.configure(yscrollcommand=vsb.set)

        # 設定列
        tree["columns"] = list(result_df.columns)
        for col in result_df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center") # 預設列寬和對齊方式

        # 插入數據
        for index, row in result_df.iterrows():
            tree.insert("", "end", values=list(row))

        # 設定表格樣式 (黑線)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3",
                        bordercolor="black",
                        borderwidth=1)
        style.map('Treeview', background=[('selected', 'blue')])

    else:
        tk.Label(result_window, text="沒有找到符合條件的資料。").pack(padx=10, pady=10)

def on_search_button_click():
    """
    處理搜尋按鈕點擊事件。
    """
    start_date_str = start_date_entry.get()
    end_date_str = end_date_entry.get()
    target_code = target_code_entry.get()

    if not start_date_str or not end_date_str or not target_code:
        messagebox.showwarning("所有欄位都不能為空。")
        return

    result_df = run_analysis(start_date_str, end_date_str, target_code)
    show_results_window(result_df)

# 主視窗設定
root = tk.Tk()
root.title("股票分析器")

# 輸入欄位：起始日期
tk.Label(root, text="起始日期 (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
start_date_entry = tk.Entry(root)
start_date_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
start_date_entry.insert(0, "2025-08-01") # 預設值

# 輸入欄位：結束日期
tk.Label(root, text="結束日期 (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
end_date_entry = tk.Entry(root)
end_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
end_date_entry.insert(0, "2025-08-10") # 預設值

# 輸入欄位：目標代號
tk.Label(root, text="股票代號:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
target_code_entry = tk.Entry(root)
target_code_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
target_code_entry.insert(0, "2330") # 預設值

# 搜尋按鈕
search_button = tk.Button(root, text="執行查詢", command=on_search_button_click)
search_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# 讓欄位可以隨著視窗大小調整
root.grid_columnconfigure(1, weight=1)

root.mainloop()