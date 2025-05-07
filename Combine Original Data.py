import pandas as pd
import os
from tkinter import filedialog, Tk

root = Tk()
root.withdraw()
root_dir = filedialog.askdirectory(title="Select folder.")
if not root_dir:
    print("Cancel selection.")
    exit()

target_files = ["Amplitude (mV)", "ISI (ms)", "Prominence (mV)", "Width (ms)"]

for base_name in target_files:
    matched_files = []
    group_id = 1
    all_data = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            name, ext = os.path.splitext(file)
            ext = ext.lower()
            if name.lower() == base_name.lower() and ext in ['.csv', '.xlsx', '.xls']:
                file_path = os.path.join(dirpath, file)

                try:
                    if ext == '.csv':
                        df = pd.read_csv(file_path)
                    else:
                        df = pd.read_excel(file_path)

                    if df.empty:
                        continue

                    df.insert(0, 'Group', group_id)
                    all_data.append(df)
                    print(f"Get: {file_path}")
                    group_id += 1

                except Exception as e:
                    print(f"Failed get {file_path}, due to {e}.")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        output_filename = f"{base_name}_combine.csv"
        output_path = os.path.join(root_dir, output_filename)
        combined_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"{group_id - 1} groups, out put: {output_path}.")
    else:
        print("Can't find file.")