# import tkinter as tk
# from tkinter import ttk, filedialog
# from settings import *
#
#
# # class ImageImport(ttk.Frame):
# #     """
# #     (Frame + Button) to import image and/or folder.
# #     Opens the file explorer dialog for election
# #     """
# #
# #     def __init__(self, parent, import_img_func):
# #         # the frame
# #         super().__init__(master=parent)
# #         # TODO: cover entire RIGHT SIDE
# #         self.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
# #
# #         self.import_img_func = import_img_func
# #
# #         # the button
# #         import_imgs_button = ttk.Button(master=self, text="select image(s)", command=self.open_dialog)
# #         import_imgs_button.pack(expand=True)
# #
# #     def open_dialog(self):
# #         path = filedialog.askopenfile().name
# #         self.import_img_func(path)
#
# class DirImport(ttk.Frame):
#     """
#     (Frame + Button) to import image and/or folder.
#     Opens the file explorer dialog for election
#     """
#
#     def __init__(self, parent, import_dir_func):
#         # the frame
#         super().__init__(master=parent)
#         # TODO: cover entire RIGHT SIDE
#         self.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
#
#         self.import_dir_func = import_dir_func
#
#         # the button
#         import_imgs_button = ttk.Button(master=self, text="select folder", command=self.open_dialog)
#         import_imgs_button.pack(expand=True)
#
#     # TODO: BUG: when cancel on img.dir dialog selected,
#     #  then button disappears but program thinks something is selected
#     def open_dialog(self):
#         path = filedialog.askdirectory()
#         self.import_dir_func(path)
#
# class DirImport(ttk.Frame):
#     """
#     (Frame + Button) to import image and/or folder.
#     Opens the file explorer dialog for election
#     """
#
#     def __init__(self, parent, import_dir_func):
#         # the frame
#         super().__init__(master=parent)
#         # TODO: cover entire RIGHT SIDE
#         self.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
#
#         self.import_dir_func = import_dir_func
#
#         # the button
#         import_imgs_button = ttk.Button(master=self, text="select folder", command=self.open_dialog)
#         import_imgs_button.pack(expand=True)
#
#     # TODO: BUG: when cancel on img.dir dialog selected,
#     #  then button disappears but program thinks something is selected
#     def open_dialog(self):
#         path = filedialog.askdirectory()
#         self.import_dir_func(path)
#
#
# class ImageOutput(tk.Canvas):
#     def __init__(self, parent):
#         super().__init__(master=parent, background=BACKGROUND_COLOR, bd=0, relief="ridge")
#         self.grid(row=0, column=0, sticky="nsew")