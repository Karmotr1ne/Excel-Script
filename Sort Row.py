import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_paths = filedialog.askopenfilenames(
    title="Select Excel",
    filetypes=[("Excel or CSV files", "*.xlsx *.xls *.csv")]
)

if not file_paths:
    print("Canceled")
    exit()

target_columns = [5, 6, 7, 10]

column_data_dict = {}

for file_path in file_paths:
    try:
        df = pd.read_csv(file_path, encoding='utf-8')  # 可改为 'gbk' 如果乱码
    except Exception as e:
        print(f"读取失败：{file_path}，原因：{e}")
        continue

    file_base = os.path.splitext(os.path.basename(file_path))[0]

    for col_index in target_columns:
        if col_index < len(df.columns):
            col_name = df.columns[col_index]

            simplified_col_name = col_name.split('.', 1)[1] if '.' in col_name else col_name

            col_series = df.iloc[:, col_index]
            col_series.name = file_base

            if col_name not in column_data_dict:
                column_data_dict[col_name] = []
            column_data_dict[col_name].append(col_series)

output_dir = os.path.dirname(file_paths[0])

for col_name, series_list in column_data_dict.items():
    combined_df = pd.concat(series_list, axis=1)

    output_path = os.path.join(output_dir, f"{col_name}.csv")
    combined_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print("Get rows")