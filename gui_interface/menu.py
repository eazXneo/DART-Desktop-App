import os
import tkinter as tk
from tkinter import ttk, filedialog

from .settings import *


class Menu(ttk.Frame):
    def __init__(self, parent, run_dart_func):
        super().__init__(master=parent)
        self.grid(row=1, column=1,  padx=5, pady=5, sticky="nsew")

        self.run_dart_func = run_dart_func

        self.settings_panel = None
        self.dart_panel = None

        self.display_welcome()

    # TODO: add getters for the settings options for DART...

    def display_welcome(self):
        # TODO: larger and to the left?
        welcome_message = \
                ("Welcome to DART." + str(os.linesep)
                + "Please select a folder with images to analyse.")
        self.welcome_label = ttk.Label(self, text=welcome_message)
        self.welcome_label.pack(padx=5, pady=20)

    def display_menu(self, import_dir):
        new_text = ("Please adjust the settings, and when ready, select \"run DART\"." + str(os.linesep) +
                    "The results will be saved as \"dart_inference_results.csv\".")
        self.welcome_label.configure(text=new_text)
        # self.label_about_exports = ttk.Label(self, text="The results will be saved as \"dart_inference_results.csv\"")
        # self.label_about_exports.grid(row=4, columnspan=2, sticky="w")

        self.settings_panel = SettingsPanel(self, import_dir)

        self.dart_panel = DartPanel(
            self,
            self.run_dart_func,
            self.settings_panel.get_file_extension_var(),
            self.settings_panel.get_crop_bool_var(),
            self.settings_panel.get_export_location_var()
        )

    def get_dart_panel(self):  # TODO seems dodgy what if None?
        return self.dart_panel

class SettingsPanel(ttk.Frame):
    def __init__(self, parent, default_export_dir):
        super().__init__(master=parent)
        self.pack(fill="x", pady=4, padx=10, ipady=8)

        self.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        # widgets
        # File extension
        # self.label_extension = ttk.Label(self, text="What file extensions do the images have?")
        self.label_extension = ttk.Label(self, text="Select the image file extension:")
        self.label_extension.grid(row=0, column=0, sticky="w")
        self.combo_ext_string = tk.StringVar(value=POSSIBLE_IMG_EXTENSIONS[0])
        self.combobox_extensions = ttk.Combobox(self, values=POSSIBLE_IMG_EXTENSIONS, textvariable=self.combo_ext_string)
        self.combobox_extensions.grid(row=0, column=1, sticky="w")

        # Crop black borders
        self.label_borders = ttk.Label(self, text="Crop black borders:")
        self.label_borders.grid(row=1, column=0, sticky="w")
        self.check_borders_bool = tk.BooleanVar(value=False)  # TODO: make sure there's a default off...?
        self.checkbutton_borders = ttk.Checkbutton(self, variable=self.check_borders_bool, onvalue=True,
                                                   offvalue=False)
        self.checkbutton_borders.grid(row=1, column=1, sticky="w")

        # Export location
        self.label_export = ttk.Label(self, text="Select results export location: ")
        self.label_export.grid(row=2, column=0, sticky="w")
        self.export_btn = ttk.Button(master=self, text="select results folder", command=self.set_export_loc)  # TODO: set command
        self.export_btn.grid(row=2, column=1, sticky="w")

        # TODO: Which folder is selected?
        self.export_frame = ttk.Frame(self)
        self.export_frame.grid(row=3, columnspan=2, sticky="w", ipadx=10)
        self.export_text = tk.StringVar(value=f"Default export location selected: ")
        self.export_location = tk.StringVar(value=default_export_dir)
        self.label_export_text = ttk.Label(self.export_frame, textvariable=self.export_text)
        self.label_export_text.pack(side="left")
        self.label_folder_selected = ttk.Label(self.export_frame, textvariable=self.export_location)
        self.label_folder_selected.pack(side="left")

    def get_file_extension_var(self):
        return self.combo_ext_string

    def get_crop_bool_var(self):
        return self.check_borders_bool

    def get_export_location_var(self):
        # TODO: not a real value.
        return self.export_location

    def set_export_loc(self):
        # TODO: how to deal with too long path here...
        self.export_text.set("New folder selected: ")

        path_retrieved = filedialog.askdirectory()
        # dealing with potential null path again.
        path_to_set = path_retrieved if os.path.isdir(path_retrieved) else self.export_location.get()
        self.export_location.set(path_to_set)


class DartPanel(ttk.Frame):
    def __init__(self, parent, run_dart_func, file_ext_var, crop_var, export_loc_var):
        super().__init__(master=parent, relief=tk.RIDGE)
        self.pack(fill="x", padx=10, pady=4, ipady=50)

        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)  # simpler way of saying the above
        self.columnconfigure((0), weight=1)  # simpler way of saying the above

        # run DART
        # self.dart_run_button = DartRun()
        self.dart_run_button = ttk.Button(
                self,
                text="run DART",
                command=lambda: run_dart_func(file_ext_var.get(), crop_var.get(), export_loc_var.get()),
        )
        self.dart_run_button.grid(row=0, pady=2)

        self.label1 = ttk.Label(self, text="")
        self.label1.grid(row=1, sticky="w", padx=20)
        self.label2 = ttk.Label(self, text="")
        self.label2.grid(row=2, sticky="w", padx=20)
        self.label3 = ttk.Label(self, text="No process currently running.")
        self.label3.grid(row=3, padx=20)
        self.label4 = ttk.Label(self, text="")
        self.label4.grid(row=4, sticky="w", padx=20)
        self.label5 = ttk.Label(self, text="")
        self.label5.grid(row=5, sticky="w", padx=20)

        self.progress_label_list = [self.label1, self.label2, self.label3, self.label4, self.label5]

        self.progress_var = tk.DoubleVar(value=0.0)

    # TODO: update used on what's happening
    def update_label(self, label_num, text):
        self.progress_label_list[label_num].configure(text=text)
        # TODO: better info display...

    def start_progress(self):
        self.progress_bar = ttk.Progressbar(
            self,
            variable=self.progress_var,
            maximum=100.0,
            mode="determinate"
        )
        self.progress_bar.grid(row=6, sticky="we", padx=20)

        # self.progress_bar.start()

    def update_progress(self, percentage):
        current_progress = self.progress_var.get()
        self.progress_var.set(current_progress+percentage)

    def stop_progress(self):
        self.progress_bar.stop()

    def reset_progress(self):
        self.progress_var.set(0.0)

    def clear_display(self):
        for label in self.progress_label_list:
            label.configure(text="")
            label.grid(sticky="w")
