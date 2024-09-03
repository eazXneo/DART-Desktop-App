import os
from datetime import datetime

from tkinter import ttk, filedialog

from .settings import DEFAULT_FILE_NAME, ALL_PILLOW_EXTENSIONS


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

    def open_dialog(self):
        path = filedialog.askdirectory()
        self.import_dir_func(path)

    def update_folder_selected(self, folder_path):
        """
        Updates the display on the left panel with which folder is selected.
        """

        path_split = folder_path.split("/")
        print("path split: ", path_split)
        path_split = [dir for dir in path_split if dir != ""]
        new_text = str(os.linesep) + "    root"
        for dir in path_split:
            new_text += " " + str(os.linesep) + "|_ " + dir
        self.no_files_selected.configure(text=("Folder selected: " + new_text))


# TODO decide whether utility class, or more Tkinter related as a frame.
class ResultsExport:
    def __init__(self, results, default_export_loc, filename):
        self.results = results
        self.export_loc = default_export_loc
        self.filename = filename

    def format_time_stamp(self):
        """
        Create a filename with a timestamp
        """

        current_datetime = datetime.now()
        print(current_datetime)
        formatted_datetime = (f"_{current_datetime.year}-{current_datetime.month}-{current_datetime.day}_"
                              f"{current_datetime.hour}-{current_datetime.minute}-{current_datetime.second}")

        return formatted_datetime

    def export_results(self):
        """
        Create the results file.
        """

        if self.filename == DEFAULT_FILE_NAME or self.filename == "":
            file_name = "dart_inference_results" + ".csv"
        else:
            file_name = self.filename + ".csv"
        print('Writing results to file...')
        with open(os.path.join(self.export_loc, file_name), 'w') as f:
            f.write('image_path,image_name,FD\n')
            for img_path, img_name, FD in self.results:
                f.write(f'{img_path}, {img_name}, {FD}\n')

        print('Created dart_inference_results.csv')

        print('Done!')


def verify_extension(file_ext, user_ext):
    """
    Checks whether extension supplied is valid in Pillow.
    """

    if file_ext in ALL_PILLOW_EXTENSIONS:
        return file_ext
    elif user_ext in ALL_PILLOW_EXTENSIONS:
        return user_ext
    elif ("." + user_ext) in ALL_PILLOW_EXTENSIONS:
        return "." + user_ext

    return False
