import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_paths = filedialog.askopenfilenames(
    title="Select Excel",
    filetypes=[("Excel files", "*.xlsx *.xls")]
)

if not file_paths:
    print("Canceled")
    exit()

target_columns = [4, 5, 6, 9]

column_data_dict = {}

for file_path in file_paths:
    df = pd.read_excel(file_path)
    file_base = os.path.splitext(os.path.basename(file_path))[0]  # 文件名无扩展名

    for col_index in target_columns:
        if col_index < len(df.columns):
            col_name = df.columns[col_index]

            col_series = df.iloc[:, col_index]
            col_series.name = file_base  
           
            if col_name not in column_data_dict:
                column_data_dict[col_name] = []
            column_data_dict[col_name].append(col_series)

output_dir = os.path.dirname(file_paths[0])

for col_name, series_list in column_data_dict.items():

    combined_df = pd.concat(series_list, axis=1)

    output_path = os.path.join(output_dir, f"{col_name}.xlsx")
    combined_df.to_excel(output_path, index=False)

print("Get rows")