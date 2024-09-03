import os
import tkinter as tk
from tkinter import ttk, filedialog

from .panels import *


# TODO: all toggles should be one class. (maybe all option settings should be - left right etc.)
class Menu(ttk.Frame):
    """
    The screen that is displayed on the right side once a folder is selected.
    Contains Settings and Display panel.
    """

    def __init__(self, parent, run_dart_func):
        super().__init__(master=parent)
        self.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.run_dart_func = run_dart_func

        self.settings_panel = None
        self.dart_panel = None

        self.display_welcome()

    def display_welcome(self):
        """
        tk welcome text
        """

        welcome_message = \
            ("Welcome to DART!" + str(os.linesep)
             + "Please select a folder with images to analyse." + str(os.linesep)
             + "" + str(os.linesep)
             + "DART uses a deep neural network to predict the output of" + str(os.linesep)
             + "an existing pipeline on high quality images from " + str(os.linesep)
             + "synthetically degraded versions of these images." + str(os.linesep)
             + "More information can be found in the paper: \"Robust and" + str(os.linesep)
             + "efficient computation of retinal fractal dimension through " + str(os.linesep)
             + "deep approximation\" by Justin Engelmann, " + str(os.linesep)
             + "Ana Villaplana-Velasco, Amos Storkey and Miguel O. Bernabeu." + str(os.linesep)
             + "" + str(os.linesep)
             + "This application was created to make DART simple to use with" + str(os.linesep)
             + "no installation of Python or libraries such as PyTorch necessary." + str(os.linesep)
             )
        self.welcome_label = ttk.Label(self, text=welcome_message)
        self.welcome_label.pack(padx=1, pady=15)

    def display_menu(self, import_dir):
        """
        Creates menu (right side)
        """

        new_text = "Please adjust the settings, and when ready, select \"run DART\"."
        self.welcome_label.configure(text=new_text)

        self.settings_panel = SettingsFrame(self, import_dir)

        self.dart_panel = DartFrame(
            self,
            self.run_dart_func,
            self.settings_panel.get_sys_extension_var(),
            self.settings_panel.get_crop_bool_var(),
            self.settings_panel.get_export_location_var(),
            self.settings_panel.get_user_extension_var(),
            self.settings_panel.get_user_filename()
        )

    def get_dart_panel(self):
        """
        Currently necessary so that the application can access the dart panel
        # TODO unsure of how to improve style here.
        """

        return self.dart_panel


class SettingsFrame(ttk.Frame):
    """
    Creates the settings panel (top right)
    """

    def __init__(self, parent, default_export_dir):  # TODO every row could be further abstracted as one setting.
        super().__init__(master=parent)
        self.pack(fill="x", pady=4, padx=10, ipady=8)

        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        self.system_ext_string = tk.StringVar(value=POSSIBLE_IMG_EXTENSIONS[0])
        self.user_ext_string = tk.StringVar()

        self.extension_panel = FileExtensionPanel(self, self.system_ext_string, self.user_ext_string)

        # Crop black borders
        self.label_borders = ttk.Label(self, text="Crop black borders:")
        self.label_borders.grid(row=1, column=0, sticky="w")
        self.check_borders_bool = tk.BooleanVar(value=False)
        self.checkbutton_borders = ttk.Checkbutton(self, variable=self.check_borders_bool, onvalue=True,
                                                   offvalue=False)
        self.checkbutton_borders.grid(row=1, column=1, sticky="w")

        # Export location
        self.label_export = ttk.Label(self, text="Select results export location: ")
        self.label_export.grid(row=2, column=0, sticky="w")
        self.export_btn = ttk.Button(master=self, text="select results folder",
                                     command=self.set_export_loc)
        self.export_btn.grid(row=2, column=1, sticky="w")

        # file name
        self.label_filename = ttk.Label(self, text="Enter results file name:")
        self.label_filename.grid(row=3, column=0, sticky="w")
        self.user_filename = tk.StringVar(value=DEFAULT_FILE_NAME)
        self.entry_filename = ttk.Entry(master=self, textvariable=self.user_filename)
        self.entry_filename.grid(row=3, column=1, sticky="w")

        # Export folder
        self.export_frame = ttk.Frame(self)
        self.export_frame.grid(row=4, columnspan=2, sticky="w", ipadx=10)
        self.export_text = tk.StringVar(value=f"Default export location selected: ")
        self.export_location = tk.StringVar(value=default_export_dir)
        self.label_export_text = ttk.Label(self.export_frame, textvariable=self.export_text)
        self.label_export_text.pack(side="left")
        self.label_folder_selected = ttk.Label(self.export_frame, textvariable=self.export_location)
        self.label_folder_selected.pack(side="left")

    """
    getters (So that the dart panel can access the settings.)
    """

    def get_user_filename(self):
        return self.user_filename

    def get_sys_extension_var(self):
        return self.system_ext_string

    def get_user_extension_var(self):
        return self.user_ext_string

    def get_crop_bool_var(self):
        return self.check_borders_bool

    def get_export_location_var(self):
        return self.export_location

    def set_export_loc(self):
        # TODO: visuals: deal with too long path here.
        self.export_text.set("New folder selected: ")

        path_retrieved = filedialog.askdirectory()
        # dealing with potential null path again.
        path_to_set = path_retrieved if os.path.isdir(path_retrieved) else self.export_location.get()
        self.export_location.set(path_to_set)


class DartFrame(ttk.Frame):
    """
    The display panel (bottom left)
    """

    def __init__(self, parent, run_dart_func, file_ext_var, crop_var, export_loc_var, user_ext_var, filename_var):
        super().__init__(master=parent, relief=tk.RIDGE)
        self.pack(fill="x", padx=10, pady=4, ipady=50)

        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)  # simpler way of saying the above
        self.columnconfigure((0), weight=1)  # simpler way of saying the above

        # run DART
        self.dart_run_button = ttk.Button(
            self,
            text="run DART",
            command=lambda: run_dart_func(file_ext_var.get(), crop_var.get(), export_loc_var.get(), user_ext_var.get(),
                                          filename_var.get()),
        )
        self.dart_run_button.grid(row=0, pady=2)

        # initialise display panel
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

    def update_label(self, label_num, text):
        """
        Update user on GUI
        """

        self.progress_label_list[label_num].configure(text=text)
        # TODO: consider what other messages / wording would be good to communicate with user.

    def start_progress(self):
        """
        Initialises progressbar
        """

        self.progress_bar = ttk.Progressbar(
            self,
            variable=self.progress_var,
            maximum=100.0,
            mode="determinate"
        )
        self.progress_bar.grid(row=6, sticky="we", padx=20)

    def update_progress(self, percentage):
        """
        updates the progressbar to a given percentage
        """

        current_progress = self.progress_var.get()
        self.progress_var.set(current_progress + percentage)

    def reset_progress(self):
        """
        progressbar is set to 0%
        """

        self.progress_var.set(0.0)

    def clear_display(self):
        """
        Clear the display panel (user can now run dart multiple times.)
        """

        for label in self.progress_label_list:
            label.configure(text="")
            label.grid(sticky="w")

        # TODO: decide whether you want to reset or destroy progressbar here.
        #  (ties into app.py TODO)
        self.reset_progress()
