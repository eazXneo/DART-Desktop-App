from PyInstaller.utils.hooks import collect_data_files, get_module_file_attribute

datas = collect_data_files("dart")
datas += collect_data_files("gui_interface")
