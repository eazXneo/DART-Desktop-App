import tkinter as tk
from tkinter import ttk

from .settings import *


class FileExtensionPanel(ttk.Frame):
    """
    Setting for the file extension
    """

    def __init__(self, parent, curr_ext_var, entry_ext_string):
        super().__init__(master=parent)
        self.grid(row=0, column=0, columnspan=2, sticky="we")

        self.combo_ext_string = curr_ext_var
        self.entry_ext_string = entry_ext_string

        self.rowconfigure(0, weight=1)
        self.columnconfigure((0), weight=1, uniform="c")
        self.columnconfigure((1), weight=1, uniform="c")
        self.columnconfigure((2), weight=1, uniform="c")
        self.columnconfigure((3), weight=1, uniform="c")

        self.label_extension = ttk.Label(self, text="Select the image file extension:")
        self.label_extension.grid(row=0, column=0, columnspan=2, sticky="w")

        self.combobox_extensions = ttk.Combobox(self, values=POSSIBLE_IMG_EXTENSIONS+["OTHER (specify)"], textvariable=self.combo_ext_string)
        self.combobox_extensions.grid(row=0, column=2, sticky="we")

        self.entry_ext = ttk.Entry(self, textvariable=self.entry_ext_string)

        # check whether "other" is selected
        self.combo_ext_string.trace("w", self.combo_string_update)

    def combo_string_update(self, *args):
        """
        tracks the current value of the conmbo string
        (needed to display or hide the entry field to specify own file extension.)
        """

        if self.combo_ext_string.get() == "OTHER (specify)":
            self.entry_ext.grid(row=0, column=3, sticky="w")
        else:
            self.entry_ext.grid_forget()
