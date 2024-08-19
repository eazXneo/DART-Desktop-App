import os
from pathlib import Path
import glob
from PIL import Image

import dart.inference as dart
from .settings import CROP_THRESHOLD

def prompt_for_bool(prompt):
    while True:
        try:
            return {"yes": True, "no": False}[input(prompt).lower()]
        except KeyError:
            print("Invalid input. Please type 'yes' or 'no'!")


class DartConnector:

    # TODO: _run_checks() and then run_dart() for the inference pipeline (run_once() vs run_batched())?

    # TODO: return results as list to app.py so that it can delegate results.csv creation to other
    def __init__(self, img_folder, img_ext, crop_black_borders, export_loc):
        self.img_folder = img_folder
        self.img_ext = img_ext
        self.crop_black_borders = crop_black_borders
        self.export_loc = export_loc

        ### TODO: overwrite / create new files rather than complaining
        # check if dart_inference_results.csv exists
        assert not os.path.exists(os.path.join(export_loc, 'dart_inference_results.csv')), \
            'ERROR: dart_inference_results.csv already exists. Please delete \ rename it before running this script.'

    def find_images(self):
        # crop_black_borders = prompt_for_bool('Do you want to crop black borders from your images? (yes/no): ')
        print(f'Okay, we {"will" if self.crop_black_borders else "will not"} crop black borders.')

        print(f'Looking for images in {self.img_folder} with extension {self.img_ext}')
        self.images = list(glob.glob(self.img_folder + f'/*.{self.img_ext}'))

        # assert len(self.images) > 0, 'No images found'
        # print(f'Found {len(self.images)} images, e.g. {Path(self.images[0]).name}, ..., {Path(self.images[-1]).name}')

        return self.images

    def load_pipeline(self):
        print('Loading pipeline...')
        self.dart_pipeline = dart.get_inference_pipeline(model_name='resnet18', device='cpu',
                                               resize_images=True, preprocessing_backend='albumentations_if_available',
                                               crop_black_borders=self.crop_black_borders,
                                               crop_threshold=CROP_THRESHOLD,
                                               loading_verbose=True, loading_pbar=True)

        return self.dart_pipeline


    def run_inference_pipeline(self, update_progress_func, update_screen_func):
        print('\nStarting inference...')
        results = []
        for img_path in self.images:
            print(f'Inferring {img_path}', end='\r')
            img = Image.open(img_path)
            print(f'Inferring {img_path} - Image loaded, running model', end='\r')
            FD = self.dart_pipeline(img)[0]
            print(f'{img_path}: {FD}')
            results.append((img_path, Path(img_path).name, FD))

            # update progressbar
            update_progress_func(80/len(self.images))
            update_screen_func()

        print('Inference complete!')

        return results
