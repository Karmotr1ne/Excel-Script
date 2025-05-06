import originpro as op
import tkinter as tk
from tkinter import filedialog
import os

op.set_show(True)

cache_file = 'last_path.txt'
last_dir = ''

if os.path.exists(cache_file):
    with open(cache_file, 'r', encoding='utf-8') as f:
        last_dir = f.read().strip()

root = tk.Tk()
root.withdraw()

file_paths = filedialog.askopenfilenames(
    title="select file",
    initialdir=last_dir,
    filetypes=[("get file", "*.xlsx *.xls *.csv")]
)

if not file_paths:
    print("Cancel selection")
    exit()

with open(cache_file, 'w', encoding='utf-8') as f:
    f.write(os.path.dirname(file_paths[0]))

book = op.new_book('w', lname='')

for path in file_paths:
    filename = os.path.basename(path)
    sheet_name = os.path.splitext(filename)[0]

    wks = book.add_sheet()
    wks.activate()
    try:
        wks.from_file(path)
        wks.label = sheet_name
    except Exception as e:
        print(f"Failed in loading {filename}, as {e}.")
        continue

print("Load all.")