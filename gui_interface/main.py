import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from .image_widgets import *
from .dart_connection import run_inference_pipeline
from .menu import *

import os


# TODO: relpath saving? 1
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class App(tk.Tk):
    def __init__(self):
        # setup
        super().__init__()
        self.geometry("1000x600")
        self.title("DART prototype 1")
        self.minsize(800, 500)
        self.configure(bg="darkgrey")  # DEBUG: need borders for now

        self.dir_path = None  # TODO: get a better solution...?

        # layout
        # self.rowconfigure((0,1,2), weight=1)
        self.rowconfigure(0, weight=1)
        # self.rowconfigure(1, weight=1)
        # self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=2)

        # widgets
        # ImportButton (Frame + Button)
        # self.import_imgs_button = DirImport(self, self.import_folder_func)

        # TODO: improve layout
        self.menu = ttk.Frame(self)
        self.menu.grid(column=1, row=0, padx=5, pady=5, sticky="ew")
        self.menu.rowconfigure((0,1,2), weight=1)
        self.menu.columnconfigure(0, weight=1)

        # the button
        import_imgs_button = ttk.Button(master=self.menu, text="select folder", command=self.open_dialog)
        import_imgs_button.grid(column=1, row=0)

        # TODO: this probably goes into menu.py later...
        # self.dart_run_button = DartRun()
        self.dart_run_button = ttk.Button(self.menu, text="Run DART", command=self.run_dart)
        self.dart_run_button.grid(column=1, row=2)

        # message to select folder. TODO: update
        self.no_files_selected = ttk.Label(self, text="No folder selected.")
        self.no_files_selected.grid(row=0, column=0, padx=5, pady=5)

        # run
        # self.mainloop()

    def open_dialog(self):
        path = filedialog.askdirectory()
        self.import_folder_func(path)

    def init_parameters(self):
        pass

    # TODO: create_widgets() perhaps more intuitive
    # def import_image_func(self, path):
    #     print("path to IMAGE:", path)  # DEBUG
    #     self.import_imgs_button.grid_forget()
    #     self.no_files_selected.grid_forget()
    #
    #     self.image_output = ImageOutput(self)

    def import_folder_func(self, path):
        print("path to FOLDER:", path)  # DEBUG

        # self.image_output = ImageOutput(self)
        self.dir_path = path

        if os.path.isdir(self.dir_path):
            # self.import_imgs_button.grid_forget()
            self.no_files_selected.grid_forget()

    # TODO: img/fdr should just be re-selectable
    def close_edit(self):
        pass

    # TODO: potentially put this is the function in dart_connection.py
    def run_dart(self):
        if not os.path.isdir(self.dir_path):
            pass
        print("-- run dart function --")
        run_inference_pipeline(img_folder=self.dir_path, img_ext="tif", crop_black_borders="no")


# if __name__ == "__main__":
#     app = App()
#     app.mainloop()

# TODO: all toggles should be one class.

# TODO: 1 - playg4 for variables from GUI into program (DART)
