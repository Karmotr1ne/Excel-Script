import os
import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict

def extract_number(s):
    match = re.search(r"(\d+)", s)
    return int(match.group(1)) if match else float('inf')

def scan_group_folder(group_dir):
    sample_map = defaultdict(lambda: defaultdict(list))

    for dirpath, _, filenames in os.walk(group_dir):
        for fname in filenames:
            if re.search(r"\.(csv|xls|xlsx)$", fname.lower()):
                cond_num = extract_number(fname)
                full_path = os.path.join(dirpath, fname)

                rel_path = os.path.relpath(full_path, group_dir)
                parts = rel_path.split(os.sep)

                if len(parts) < 3:
                    continue

                date = parts[0]
                slice_name = parts[1]
                sample_label = f"{date}/{slice_name}"

                sample_map[sample_label][cond_num].append(full_path)

    return sample_map

def compute_means_from_raw(file_list):
    durations = []
    ibis = []

    for path in file_list:
        try:
            if path.lower().endswith(".csv"):
                df = pd.read_csv(path, header=0)
            else:
                df = pd.read_excel(path, header=0)

            if df.shape[1] < 6 or df.shape[0] < 2:
                continue

            start_vals = pd.to_numeric(df.iloc[:, 3], errors='coerce')
            end_vals = pd.to_numeric(df.iloc[:, 4], errors='coerce')
            ibi_vals = pd.to_numeric(df.iloc[:, 5], errors='coerce')

            burst_durations = (end_vals - start_vals).dropna()
            mean_duration = burst_durations.mean()
            mean_ibi = ibi_vals.dropna().mean()

            durations.append(mean_duration)
            ibis.append(mean_ibi)

        except:
            continue

    if durations:
        return sum(durations) / len(durations), sum(ibis) / len(ibis)
    else:
        return None, None

# Main logic
root = tk.Tk()
root.withdraw()

group_dir = filedialog.askdirectory(title="Select a group folder (e.g. Reversan)")
if not group_dir:
    exit()

sample_map = scan_group_folder(group_dir)

def sort_sample_key(sample_label):
    date_str, slice_str = sample_label.split('/')
    date_digits = re.sub(r"[^\d]", "", date_str)
    slice_num = extract_number(slice_str)
    return (int(date_digits), slice_num)
all_samples = sorted(sample_map.keys(), key=sort_sample_key)

all_conditions = sorted({c for sample in sample_map.values() for c in sample})

timing_df = pd.DataFrame(index=all_samples, columns=[f"Cond{c}" for c in all_conditions])
ibi_df = pd.DataFrame(index=all_samples, columns=[f"Cond{c}" for c in all_conditions])

for sample in all_samples:
    for cond in all_conditions:
        files = sample_map[sample].get(cond, [])
        if files:
            dur, ibi = compute_means_from_raw(files)
            if dur is not None:
                timing_df.at[sample, f"Cond{cond}"] = dur
            if ibi is not None:
                ibi_df.at[sample, f"Cond{cond}"] = ibi

timing_df.to_csv(os.path.join(group_dir, "Timing_summary.csv"))
ibi_df.to_csv(os.path.join(group_dir, "IBI_summary.csv"))

print("Finished: Saved Timing_summary.csv and IBI_summary.csv")

