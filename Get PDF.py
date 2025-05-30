import os
import shutil
from tkinter import Tk, filedialog

def select_directory(prompt_title):
    root = Tk()
    root.withdraw()  # hide
    folder_path = filedialog.askdirectory(title=prompt_title)
    root.destroy()
    return folder_path

def copy_pdfs_with_structure(source_root, target_root):
    for dirpath, dirnames, filenames in os.walk(source_root):
        relative_path = os.path.relpath(dirpath, source_root)
        target_dir = os.path.join(target_root, relative_path)

        for file in filenames:
            if file.lower().endswith('.pdf'):
                os.makedirs(target_dir, exist_ok=True)
                source_file = os.path.join(dirpath, file)
                target_file = os.path.join(target_dir, file)
                shutil.move(source_file, target_file)
                print(f"Moved: {source_file} -> {target_file}")

if __name__ == "__main__":
    print("Select source")
    source_root = select_directory("source")

    print("Select target")
    target_root = select_directory("target")

    copy_pdfs_with_structure(source_root, target_root)
    print("Finish move")
