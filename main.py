import os
import pathlib
import time
from datetime import datetime
import shutil
from tkinter import Tk, Label, Button, StringVar
from tkinter import filedialog

from formats import image_formats, video_formats

total_files = 0
copied_files = 0


def determine_file_type(file_path):
    file_name = os.path.basename(file_path)
    file_extension = file_name.lower().split(".")[-1]
    if file_extension in image_formats:
        return "Képek"
    elif file_extension in video_formats:
        return "Videók"
    else:
        return "Egyéb"


def create_sub_folders(directory):
    video_folder = os.path.join(directory, "Videók")
    images_folder = os.path.join(directory, "Képek")
    other_folder = os.path.join(directory, "Egyéb")

    for folder in [video_folder, images_folder, other_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Létrehozva: {folder}")


def get_file_name(file_path):
    file_name = os.path.basename(file_path)
    return file_name


def copy_file(source_path, destination_path):
    global copied_files
    try:
        shutil.copy2(source_path, destination_path)
        copied_files += 1
        update_progress_label()
        print(f"A fájl sikeresen másolva: {destination_path}")
    except FileNotFoundError as e:
        print("A forrásfájl nem található.")
        print(f"Hiba : {e}")
    except Exception as e:
        print(f"Hiba történt: {e}")


def create_folder_for_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        folder_path = os.path.join(str(date_obj.year), str(date_obj.month))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"A mappa létrehozva: {folder_path}")
            create_sub_folders(folder_path)
        return folder_path
    except ValueError as e:
        print(f"Hiba történt: {e}")


def file_search(root):
    return list(pathlib.Path(root).rglob("*"))


def get_create_time(path):
    global total_files
    total_files = len(data)
    ti_m = os.path.getmtime(path)
    m_ti = time.ctime(ti_m)
    t_obj = time.strptime(m_ti)
    T_stamp = time.strftime("%Y-%m-%d", t_obj)
    folder_path = create_folder_for_date(T_stamp)
    file_format = determine_file_type(path)
    copy_file(path, folder_path + "/" + file_format + "/" + get_file_name(path))


def progres_json(json_data):
    for item in json_data:
        get_create_time(item)


def update_progress_label():
    percent = (copied_files / total_files) * 100
    progress_var.set(f"{copied_files}/{total_files} fájl másolva ({percent:.2f}%)")
    root.update_idletasks()


def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        global data
        data = file_search(folder_selected)
        progres_json(data)


root = Tk()
root.title("Fájl másoló GUI")

progress_var = StringVar()
progress_label = Label(root, textvariable=progress_var)
progress_label.pack()

select_folder_button = Button(root, text="Mappa kiválasztása", command=select_folder)
select_folder_button.pack()

root.mainloop()
