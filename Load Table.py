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
    title="Select Excel",
    filetypes=[("Excel Document", "*.xlsx")]
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
    wks.from_file(path)
    wks.label = sheet_name

print("Get all excel!")