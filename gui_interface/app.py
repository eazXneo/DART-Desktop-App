import sys
from pathlib import Path

import tkinter as tk
from tkinter import ttk

from .dart_connection import DartConnector
from .file_handling import *
from .menu import Menu


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
        self.title("DART interface Version 1.1")
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
        self.banner_text = ttk.Label(self.banner, text="DART -  Deep Approximation of Retinal Traits",
                                     font="Courier 24 bold")
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
        self.dir_path = path if os.path.isdir(path) else ""

        print("path to FOLDER:", self.dir_path)  # DEBUG

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
            self.menu.display_menu(self.dir_path)

    # TODO: potentially put this is the function in dart_connection.py
    def run_dart(self, file_ext, crop_borders, export_loc):
        dart_panel = self.menu.get_dart_panel()
        assert dart_panel is not None, "fix code structure around menu panels."

        dart_panel.clear_display()

        # DEBUG
        print("-- run dart function --")  # DEBUG
        # TODO: get rid of the "." in the file extension name
        print("> Import path: ", self.dir_path)  # DEBUG
        file_ext = file_ext[1:]
        print("> File extension: ", file_ext)  # DEBUG
        # crop_borders = "yes" if crop_borders else "no"
        print("> Crop borders: ", crop_borders)  # DEBUG
        print("> Export location: ", export_loc)  # DEBUG
        # TODO: results should be a list.

        dart_connector = DartConnector(img_folder=self.dir_path, img_ext=file_ext, crop_black_borders=crop_borders, export_loc=export_loc)

        # TODO: potentially send the labels to dart_connection, and dart_connector will call all functions? Meh

        # found images.
        images = dart_connector.find_images()
        assert len(images) > 0, 'No images found'  # TODO: handle this case and tell user
        dart_panel.update_label(0, f"Found {len(images)} images, e.g. {Path(images[0]).name}, ..., {Path(images[-1]).name}")

        # load pipeline
        pipeline = dart_connector.load_pipeline()
        dart_panel.update_label(1, "Starting inference....")

        # start inference (TODO and pass the progressbar)
        results = dart_connector.run_inference_pipeline()
        dart_panel.update_label(2, "Writing results to file...")

        # write to file
        self.export_results_obj = ResultsExport(results, export_loc)
        self.export_results_obj.export_results()

        # done
        dart_panel.update_label(3, "Done!")

        # TODO: Messages + confirmation. (use a canvas?)

# TODO: all toggles should be one class. (maybe all option settings should be - left right etc.)
