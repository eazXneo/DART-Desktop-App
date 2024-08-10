import os

import tkinter as tk
from tkinter import ttk, filedialog
from .settings import *


# class ImageImport(ttk.Frame):
#     """
#     (Frame + Button) to import image and/or folder.
#     Opens the file explorer dialog for election
#     """
#
#     def __init__(self, parent, import_img_func):
#         # the frame
#         super().__init__(master=parent)
#         # TODO: cover entire RIGHT SIDE
#         self.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
#
#         self.import_img_func = import_img_func
#
#         # the button
#         image_import_frame = ttk.Button(master=self, text="select image(s)", command=self.open_dialog)
#         image_import_frame.pack(expand=True)
#
#     def open_dialog(self):
#         path = filedialog.askopenfile().name
#         self.import_img_func(path)

# TODO: use inheritance if also indiv file import as well.
class DirImport(ttk.Frame):
    """
    (Frame + Button) to import folder.
    Opens the file explorer dialog for election
    """

    def __init__(self, parent, import_dir_func):
        super().__init__(master=parent)  # the frame
        # TODO: cover entire RIGHT SIDE (or left?)
        self.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        self.import_dir_func = import_dir_func

        # the button
        import_imgs_button = ttk.Button(master=self, text="select image folder", command=self.open_dialog)
        import_imgs_button.pack(padx=5, pady=20)

        # message to select folder.
        self.no_files_selected = ttk.Label(self, text="No folder selected.")
        self.no_files_selected.pack(padx=5, pady=5)

    # TODO: BUG: when cancel on img.dir dialog selected,
    #  then button disappears but program thinks something is selected
    def open_dialog(self):
        path = filedialog.askdirectory()
        self.import_dir_func(path)

    def update_folder_selected(self, folder_path):
        path_split = folder_path.split(str(os.sep))
        print(path_split)
        path_split.pop(0) if (path_split[0] == "") else 3 + 3
        new_text = ""
        for dir in path_split:
            new_text += " " + str(os.linesep) + "|_ " + dir
        self.no_files_selected.configure(text=("Folder selected: " + new_text))


class ImageOutput(tk.Canvas):
    def __init__(self, parent, resize_image_func):
        super().__init__(master=parent, background=BACKGROUND_COLOR, bd=0, relief="ridge")
        self.grid(row=0, column=0, sticky="nsew")
        self.bind("<Configure>", resize_image_func)


class CloseOutput(ttk.Button):
    def __init__(self, parent, close_func):
        super().__init__(
            master=parent,
            command=close_func,
            text="x",
            # text_color=WHITE,
            # fg_color = "transparent",
            # width=40,
            # height=40,
            # corner_radius=0.05,
            # hover_color=CLOSE_RED
        )  # the arguments can be passed if switch to ctk made.
        self.place(relx=0.99, rely=0.01, anchor="ne")
