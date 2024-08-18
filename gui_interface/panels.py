import tkinter as tk
from tkinter import ttk


class ExtensionPanel(ttk.Frame):
    def __init__(self, parent):
        pass


class FileNamePanel(ttk.Frame):
    # TODO: file_string ==> file_ext
    def __init__(self, parent, name_string, file_string):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky="we")

        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1, 2, 3), weight=1)

        self.label_extension = ttk.Label(self, text="Select the image file extension:")
        self.label_extension.grid(row=0, column=0, columnspan=2, sticky="w")
        # self.combo_ext_string = tk.StringVar(value=POSSIBLE_IMG_EXTENSIONS[0])
        # self.combobox_extensions = ttk.Combobox(self, values=POSSIBLE_IMG_EXTENSIONS, textvariable=self.combo_ext_string)
        # self.combobox_extensions.grid(row=0, column=1, sticky="w")
