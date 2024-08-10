import sys
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from .image_widgets import *
from .dart_connection import run_inference_pipeline
from .menu import Menu

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
        self.resizable(False, False)  # DEBUG: for now, unresponsive

        self.dir_path = None  # TODO: get a better solution...?

        # layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=2, uniform="a")
        self.columnconfigure(1, weight=5, uniform="a")

        # dart banner / title
        self.banner = ttk.Frame(self)
        self.banner.grid(row=0, columnspan=2, padx=5, pady=5, sticky='nsew')
        self.banner_text = ttk.Label(self.banner, text="DART -  Deep Approximation of Retinal Traits", font="Courier 24 bold")
        self.banner_text.pack(pady=10)

        # widgets  # TODO: create_widgets() for all below perhaps more intuitive
        # Import (Frame + Button)
        self.image_import_frame = DirImport(self, self.import_folder_func)

        # TODO: Menu greyed out / message.
        self.menu = Menu(self, self.run_dart)


    def open_dialog(self):
        path = filedialog.askdirectory()
        self.import_folder_func(path)

    def init_parameters(self):
        pass

    def import_folder_func(self, path):
        print("path to FOLDER:", path)  # DEBUG
        self.dir_path = path

        # TODO: potentially a separate method. Or this all goes to the Menu class
        if os.path.isdir(self.dir_path):
            ### from tut, import_image
            # TODO: change to including images found...?
            # self.close_button = CloseOutput(self, self.close_edit)
            ###

            self.image_import_frame.update_folder_selected(self.dir_path)

            # TODO: probably just un-block the menu...
            self.menu.grid_forget()
            self.menu = Menu(self, self.run_dart)
            self.menu.display_menu()

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

        # TODO: Messages + confirmation.


# TODO: all toggles should be one class.
