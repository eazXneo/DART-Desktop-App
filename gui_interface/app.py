import sys
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
        self.geometry("500x300")
        self.title("DART prototype 1")
        self.minsize(800, 500)
        self.configure(bg="darkgrey")  # DEBUG: need borders for now

        self.dir_path = None  # TODO: get a better solution...?

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=2)

        # widgets  # TODO: create_widgets() for all below perhaps more intuitive
        # Import (Frame + Button)
        self.image_import_frame = DirImport(self, self.import_folder_func)

        # TODO: Menu greyed out / message.

    def open_dialog(self):
        path = filedialog.askdirectory()
        self.import_folder_func(path)

    def init_parameters(self):
        pass

    def import_folder_func(self, path):
        print("path to FOLDER:", path)  # DEBUG
        self.dir_path = path

        if os.path.isdir(self.dir_path):
            ### from tut, import_image
            # TODO: change to including images found...?
            self.close_button = CloseOutput(self)
            ###

            self.image_import_frame.update_folder_selected(self.dir_path)
            # TODO: improve layout
            self.menu = ttk.Frame(self)
            self.menu.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
            self.menu.rowconfigure(0, weight=1)
            self.menu.columnconfigure(0, weight=1)

            # TODO: add combo box for file name extensions?

            # TODO: this probably goes into menu.py later...
            # self.dart_run_button = DartRun()
            self.dart_run_button = ttk.Button(self.menu, text="Run DART", command=self.run_dart)
            self.dart_run_button.pack()

    ### from tut
    def resize_image(self, event):
        canvas_ratio = event.width / event.height
    ###

    # TODO: img/fdr should just be re-selectable
    ### from tut
    def close_edit(self):
        pass
    ###

    # TODO: potentially put this is the function in dart_connection.py
    def run_dart(self):
        if not os.path.isdir(self.dir_path):
            pass
        print("-- run dart function --")
        run_inference_pipeline(img_folder=self.dir_path, img_ext="jpg", crop_black_borders="no")


# TODO: all toggles should be one class.
