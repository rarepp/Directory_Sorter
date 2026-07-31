import pathlib as pl
import tkinter as tk
import tkinter.filedialog as fd

selected_folder = pl.Path.home() / "Downloads"
status = " "
state = 0

CATEGORIES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Presentations": [".pptx"],
    "Archives": [".zip", ".rar", ".7z"],
    "Audio": [".mp3", ".wav"],
    "Videos": [".mp4"],
    "Applications": [".exe"]
}


def browser_folder():
    global selected_folder
    global status
    path = fd.askdirectory()
    if path:
        selected_folder = pl.Path(path)
        status = "Directory Selected"
        directory_status.config(text=status)
        directory_path.config(text=path)


def check_path(path):
    global status
    if pl.Path(path).exists():
        status = "Good to go"
    else:
        status = "Invalid path"


check_path(selected_folder)

root = tk.Tk()
root.title("Directory Sorter")
root.geometry("700x400")

folder_button = tk.Button(root, text="Browse Folder", command=browser_folder)
folder_button.pack()

sort_button = tk.Button(
    root, text="Sort Folder", command=lambda: sort_folder(selected_folder)
)
sort_button.pack()

directory_path = tk.Label(root, text=str(selected_folder))
directory_path.pack()

directory_status = tk.Label(root, text=status)
directory_status.pack()

def sort_folder(folder):
    if pl.Path(folder).exists():
        for file in pl.Path(folder).iterdir():
            if file.is_file():
                file_extension = file.suffix.lower()
                category_found = False

                for category_name, extensions in CATEGORIES.items():
                    if file_extension in extensions:
                        target_dir = folder / category_name
                        target_dir.mkdir(exist_ok=True)
                        file.rename(target_dir / file.name)
                        category_found = True
                        break

                if not category_found:
                    others_dir = folder / "Others"
                    others_dir.mkdir(exist_ok=True)
                    file.rename(others_dir / file.name)

        directory_status.config(text="Sorting Complete!")

root.mainloop()