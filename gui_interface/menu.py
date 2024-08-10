import os
import tkinter as tk
from tkinter import ttk
from .settings import *

class Menu(ttk.Frame):
    def __init__(self, parent, run_dart_func):
        super().__init__(master=parent)
        self.grid(row=1, column=1,  padx=5, pady=5, sticky="nsew")

        self.run_dart_func = run_dart_func

        self.display_welcome()

    # TODO: add getters for the settings options for DART...

    def display_welcome(self):
        # TODO: larger and to the left?
        welcome_message = \
                ("Welcome to DART." + str(os.linesep)
                + "Please select a folder with images to analyse.")
        self.welcome_label = ttk.Label(self, text=welcome_message)
        self.welcome_label.pack(padx=5, pady=20)

    def display_menu(self):
        self.welcome_label.forget()


        self.settings_panel = SettingsPanel(self)

        self.dart_panel = DartPanel(self, self.run_dart_func)

class SettingsPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.pack(fill="x", pady=4, padx=10, ipady=8)

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        # widgets
        # File extension
        # self.label_extension = ttk.Label(self, text="What file extensions do the images have?")
        self.label_extension = ttk.Label(self, text="Select the image file extension:")
        self.label_extension.grid(row=0, column=0, sticky="w")
        combo_ext_string = tk.StringVar(value=POSSIBLE_IMG_EXTENSIONS[0])
        self.combobox_extensions = ttk.Combobox(self, values=POSSIBLE_IMG_EXTENSIONS, textvariable=combo_ext_string)
        self.combobox_extensions.grid(row=0, column=1, sticky="w")

        # Crop black borders
        self.label_borders = ttk.Label(self, text="Crop black borders:")
        self.label_borders.grid(row=1, column=0, sticky="w")
        check_borders_bool = tk.BooleanVar(value=False)  # TODO: make sure there's a default off...?
        self.checkbtn_borders = ttk.Checkbutton(self, variable=check_borders_bool, onvalue=True,
                                                offvalue=False)
        self.checkbtn_borders.grid(row=1, column=1, sticky="w")

        # Export location
        self.label_export = ttk.Label(self, text="Select results export location: ")
        self.label_export.grid(row=2, column=0, sticky="w")
        self.export_btn = ttk.Button(master=self, text="select results folder")  # TODO: set command
        self.export_btn.grid(row=2, column=1, sticky="w")
        # TODO: Which folder is selected?


class DartPanel(ttk.Frame):
    def __init__(self, parent, run_dart_func):
        super().__init__(master=parent)
        self.pack(fill="x", pady=4, ipady=8)

        self.rowconfigure((0, 1), weight=1)  # simpler way of saying the above
        self.columnconfigure((0, 1), weight=1)  # simpler way of saying the above

        # run DART
        # self.dart_run_button = DartRun()
        self.dart_run_button = ttk.Button(self, text="Run DART", command=run_dart_func)
        self.dart_run_button.pack()


### from tut
class PositionFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)  # Also  fg_color="blue"
        self.pack(expand=True, fill="both")
###


class ColourFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)  # Also  fg_color="green"
        self.pack(expand=True, fill="both")
###
