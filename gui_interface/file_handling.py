import os

from tkinter import ttk, filedialog


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
        print("path split: ", path_split)
        path_split = [dir for dir in path_split if dir!=""]
        new_text = str(os.linesep) + "    root"
        for dir in path_split:
            new_text += " " + str(os.linesep) + "|_ " + dir
        self.no_files_selected.configure(text=("Folder selected: " + new_text))
