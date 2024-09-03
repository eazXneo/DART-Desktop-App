import sys
from pathlib import Path

import tkinter as tk
from PIL import Image, ImageTk

from .dart_connection import DartConnector
from .file_handling import *
from .file_handling import verify_extension
from .menu import Menu


def resource_path(relative_path):
    """
    Get the path to where the executable is located.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")

    return os.path.join(base_path, relative_path)


class App(tk.Tk):
    """
    Main tkinter window.
    """

    def __init__(self):
        # setup
        super().__init__()
        self.geometry("600x400")
        self.title("DART interface Version 1.1")
        self.minsize(800, 500)
        self.configure(bg="darkgrey")
        self.resizable(False, False)

        self.dir_path = None  # TODO: is there a better solution?

        # layout
        self.rowconfigure(0, weight=1, uniform="b")
        self.rowconfigure(1, weight=8, uniform="b")
        self.columnconfigure(0, weight=2, uniform="a")
        self.columnconfigure(1, weight=5, uniform="a")

        # TODO: create_widgets / elements () for all below perhaps more intuitive
        self.create_banner()

        # widgets
        self.image_import_frame = DirImport(self, self.import_folder_func)
        self.menu = Menu(self, self.run_dart)

    def create_banner(self):  # TODO: edit these hard-coded values for image size.
        """
        Creates the banner image at the top of the window.
        """

        # dart banner / title
        self.banner_canvas = tk.Canvas(self, background="white", height=50)
        self.banner_canvas.grid(row=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        # place banner to the left-ish side?
        self.image = Image.open(resource_path("gui_interface/banner.png"))
        self.image_ratio = self.image.size[0] / self.image.size[1]

        self.image_height = int(400 / 8)
        self.image_width = int(self.image_height * self.image_ratio)
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)

        self.banner_canvas.create_image(4, 0, image=self.image_tk, anchor="nw")

    def init_parameters(self):
        pass  # TODO

    def import_folder_func(self, path):
        """
        Function to check whether a valid path was selected from the file dialog.
        If yes, initiates creation of the run-screen.
        """

        self.dir_path = path if os.path.isdir(path) else ""

        # TODO: Could be a separate method.
        if os.path.isdir(self.dir_path):
            # TODO: could show / include images found.

            self.image_import_frame.update_folder_selected(self.dir_path)
            self.menu.grid_forget()

            self.menu = Menu(self, self.run_dart)

            # default export location is Desktop
            desktop_dir = Path.home() / 'Desktop'
            if os.path.isdir(desktop_dir):
                self.menu.display_menu(desktop_dir)
            # if this path doesn't exist, then just the use import path
            else:
                self.menu.display_menu(self.dir_path)


    def open_dialog(self):
        """
        Open dialog to select a directory.
        """

        path = filedialog.askdirectory()
        self.import_folder_func(path)

    def run_dart(self, file_ext, crop_borders, export_loc, user_ext, filename):
        """
        Function that executes when the "RUN" button is pressed.
        """

        dart_panel = self.menu.get_dart_panel()
        # assert dart_panel is not None, "fix code structure around menu panels."

        dart_panel.clear_display()  # for multiple runs of DART, restart progress.

        # verify extension typed in: (TODO: separate method)
        is_valid = verify_extension(file_ext, user_ext)
        if not is_valid:
            dart_panel.update_label(2, "The entered file extension is not supported.")
            return

        # get rid of the "." in the file extension name
        file_ext = is_valid[1:]

        dart_connector = DartConnector(img_folder=self.dir_path, img_ext=file_ext, crop_black_borders=crop_borders,
                                       export_loc=export_loc)

        images = dart_connector.find_images()
        # handle the case where no images found and tell user
        if len(images) < 1:
            dart_panel.update_label(2, "No images found.")
            return

        dart_panel.update_label(0,
                                f"Found {len(images)} images, e.g. {Path(images[0]).name}, ..., {Path(images[-1]).name}")

        # TODO: this has to be cleaned up within the Menu class.
        dart_panel.start_progress()
        dart_panel.reset_progress()
        dart_panel.update_progress(5.0)
        self.update()

        # load pipeline
        pipeline = dart_connector.load_pipeline()
        dart_panel.update_label(1, "Starting inference....")
        dart_panel.update_progress(10.0)
        self.update()

        # start inference (and pass the progressbar)
        results = dart_connector.run_inference_pipeline(dart_panel.update_progress, self.update_screen)
        dart_panel.update_label(2, "Writing results to file...")

        # write to file
        self.export_results_obj = ResultsExport(results, export_loc, filename)
        self.export_results_obj.export_results()
        dart_panel.update_progress(5.0)
        self.update()

        # done
        dart_panel.update_label(3, "Done!")


    def update_screen(self):
        """
        Allows tkinter to update the screen during long computation.
        """
        self.update()
