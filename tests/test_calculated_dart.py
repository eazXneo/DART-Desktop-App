import pytest
import os
import glob
import shutil
import random
import tempfile

from gui_interface.app import App
from pathlib import Path

# def test_always_passes():
#     assert True
#
# def test_always_fails():
#     assert False

IMAGE_N = 50

# @pytest.fixture
# def teardown():
#     print(os.path.join(os.getcwd(), "tests/data_subset"))
    # [f.unlink() for f in Path("/path/to/folder").glob("*") if f.is_file()]

@pytest.fixture
def setup_data():
    src_dir = str(os.path.join(os.getcwd(), "tests/test_data"))
    # dst_dir = str(os.path.join(os.getcwd(), "tests/data_subset"))
    temp_dir = tempfile.TemporaryDirectory(dir=os.path.join(os.getcwd(), "tests"))
    dst_dir = temp_dir.name
    img_list = random.sample(list(glob.iglob(os.path.join(src_dir, "*.jpg"))), IMAGE_N)
    for jpgfile in img_list:
        shutil.copy(jpgfile, dst_dir)

    yield dst_dir

    # print(os.path.join(os.getcwd(), "tests/data_subset"))
    temp_dir.cleanup()


@pytest.fixture
def application(setup_data):
    app = App()
    # import_dir_path = str(os.path.join(os.getcwd(), "tests/test_data"))
    # import_dir_path = str(os.path.join(os.getcwd(), os.pardir, "eye_scans"))  # DEBUG
    import_dir_path = setup_data
    app.dir_path = import_dir_path
    app.menu.display_menu(import_dir_path)
    return app

def test_50_random_images(application):
    # if possible, hook into the app.run_dart function.
    # run dart from there
    app = application
    app.run_dart(
        ".jpg",
        False,
        str(os.path.join(os.getcwd(), "tests/test_results")),
        "",
        "results_gui"
    )

    # run the original example script

    # open both csv files to compare them
    # make this a separate function potentially

# TODO: test parameters somehow via clicks?