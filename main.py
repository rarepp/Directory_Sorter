import pathlib as pl
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox

CATEGORIES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Presentations": [".pptx"],
    "Archives": [".zip", ".rar", ".7z"],
    "Audio": [".mp3", ".wav"],
    "Videos": [".mp4"],
    "Applications": [".exe"],
}


class DirectorySorterApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Directory Sorter")
        self.geometry("600x250")
        self.resizable(False, False)

        # Reactive Tkinter Variables
        self.folder_var = tk.StringVar(value=str(pl.Path.home() / "Downloads"))
        self.status_var = tk.StringVar()

        self._validate_initial_path()
        self._build_ui()

    def _validate_initial_path(self):
        initial_path = pl.Path(self.folder_var.get())
        if initial_path.exists():
            self.status_var.set("Ready to sort")
        else:
            self.status_var.set("Default directory not found")

    def _build_ui(self):
        # Configure Grid Layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Main Container
        container = tk.Frame(self, padx=20, pady=20)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)

        # Selection Group Box
        selection_frame = tk.LabelFrame(
            container, text=" Selected Directory ", padx=10, pady=10
        )
        selection_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        selection_frame.columnconfigure(0, weight=1)

        path_entry = tk.Entry(
            selection_frame, textvariable=self.folder_var, state="readonly"
        )
        path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        browse_btn = tk.Button(
            selection_frame, text="Browse...", command=self.browse_folder
        )
        browse_btn.grid(row=0, column=1)

        # Action & Status Area
        action_frame = tk.Frame(container)
        action_frame.grid(row=1, column=0, sticky="ew")
        action_frame.columnconfigure(0, weight=1)

        sort_btn = tk.Button(
            action_frame,
            text="Sort Directory",
            command=self.sort_folder,
            bg="#007acc",
            fg="white",
            font=("TkDefaultFont", 10, "bold"),
            pady=5,
        )
        sort_btn.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        status_label = tk.Label(
            action_frame,
            textvariable=self.status_var,
            fg="#555555",
            anchor="w",
        )
        status_label.grid(row=1, column=0, sticky="w")

    def browse_folder(self):
        path = fd.askdirectory()
        if path:
            self.folder_var.set(path)
            self.status_var.set("Directory selected")

    def sort_folder(self):
        folder_path = pl.Path(self.folder_var.get())

        if not folder_path.exists():
            self.status_var.set("Invalid directory path")
            return

        moved_count = 0
        try:
            for file in folder_path.iterdir():
                if file.is_file():
                    file_ext = file.suffix.lower()
                    target_category = "Others"

                    for category, extensions in CATEGORIES.items():
                        if file_ext in extensions:
                            target_category = category
                            break

                    target_dir = folder_path / target_category
                    target_dir.mkdir(exist_ok=True)
                    file.rename(target_dir / file.name)
                    moved_count += 1

            self.status_var.set(
                f"Complete! Sorted {moved_count} file(s)."
            )
            messagebox.showinfo("Success", f"Sorted {moved_count} files.")

        except Exception as e:
            self.status_var.set("Error during sorting process")
            messagebox.showerror("Error", f"Failed to sort files: {e}")


if __name__ == "__main__":
    app = DirectorySorterApp()
    app.mainloop()