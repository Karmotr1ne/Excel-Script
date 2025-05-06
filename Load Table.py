import originpro as op
import tkinter as tk
from tkinter import filedialog
import os

op.set_show(True)

root = tk.Tk()
root.withdraw()
file_paths = filedialog.askopenfilenames(
    title="Select Excel",
    filetypes=[("Excel Document", "*.xlsx")]
)

if not file_paths:
    print("Cancel selection")
    exit()

book = op.new_book('w', lname='Excel_Merged')

for path in file_paths:
    filename = os.path.basename(path)
    sheet_name = os.path.splitext(filename)[0]

    wks = book.add_sheet()
    wks.activate()
    wks.from_file(path)
    wks.label = sheet_name

print("Get all excel!")