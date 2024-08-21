import pytest
import os
import glob
import shutil
import random
import tempfile
import pandas as pd

from gui_interface.app import App
from gui_interface.looping_over_images_in_folder_for_testing import run_original_dart_script
from tests.mock_user_input import *
from pathlib import Path

# def test_always_passes():
#     assert True
#
# def test_always_fails():
#     assert False

IMAGE_N = 50
GUI_RESULTS_FILENAME = "results_gui"
OG_SCRIPT_RESULTS_FILENAME = "results_og"


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


@pytest.fixture
def run_gui_dart(application):
    # if possible, hook into the app.run_dart function.
    # run dart from there

    app = application
    app.run_dart(
        ".jpg",
        False,
        str(os.path.join(os.getcwd(), "tests/test_results")),
        "",
        GUI_RESULTS_FILENAME
    )

    path_to_results = str(os.path.join(os.getcwd(), "tests/test_results/", GUI_RESULTS_FILENAME))

    return path_to_results


@pytest.fixture
def run_original_dart(setup_data):
    # run the original example script

    set_keyboard_input([setup_data, "jpg", "no", str(os.path.join(os.getcwd(), "tests/test_results"))])

    results = run_original_dart_script()  # TODO: if user input, then make a separate file for unittest stuff and throw into there, call here?

    print('Writing results to file...')
    with open(str(os.path.join(os.getcwd(), "tests/test_results/", (OG_SCRIPT_RESULTS_FILENAME + ".csv"))), 'w') as f:
        f.write('image_path,image_name,FD\n')
        for img_path, img_name, FD in results:
            f.write(f'{img_path}, {img_name}, {FD}\n')

    print('Created dart_inference_results.csv')

    print('Done!')


def test_compare_50_random_images(run_gui_dart, run_original_dart):
    print("?")

    # open both csv files to compare them

    # make this a separate function potentially
    # Read CSV files
    df1_gui = pd.read_csv(str(os.path.join(os.getcwd(), "tests/test_results/", (GUI_RESULTS_FILENAME + ".csv"))))
    df2_og = pd.read_csv(str(os.path.join(os.getcwd(), "tests/test_results/", (OG_SCRIPT_RESULTS_FILENAME + ".csv"))))

    # Compare dataframes
    diff = df1_gui.compare(df2_og)

    # Print the differences
    print("Differences between file1 and file2:")
    print(diff)

    assert len(diff) == 0

# TODO: test parameters somehow via clicks?
