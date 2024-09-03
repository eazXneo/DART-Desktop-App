import os
from pathlib import Path
import glob
from PIL import Image

import src.dart.inference as dart
from .settings import CROP_THRESHOLD


class DartConnector:
    """
    Interfaces with the .dart module.
    Split into functions so the app GUI can be updated outside of this file.
    """

    # TODO: refactor, such that all methods have to have vars passed rather than setting instance variables
    #  outside of the constructor
    # TODO: different structure idea: _run_checks() and then run_dart() for the inference pipeline
    #  (run_once() vs run_batched())?

    def __init__(self, img_folder, img_ext, crop_black_borders, export_loc):
        self.img_folder = img_folder
        self.img_ext = img_ext
        self.crop_black_borders = crop_black_borders
        self.export_loc = export_loc

    def find_images(self):
        """
        Finds images in the folder
        """

        print(f'Okay, we {"will" if self.crop_black_borders else "will not"} crop black borders.')

        print(f'Looking for images in {self.img_folder} with extension {self.img_ext}')
        self.images = list(glob.glob(self.img_folder + f'/*.{self.img_ext}'))

        return self.images

    def load_pipeline(self):  # Example of where should have to pass the images to it(?)
        """
        Creates inference pipeline
        """

        print('Loading pipeline...')
        self.dart_pipeline = dart.get_inference_pipeline(model_name='resnet18', device='cpu',
                                                         resize_images=True,
                                                         preprocessing_backend='albumentations_if_available',
                                                         crop_black_borders=self.crop_black_borders,
                                                         crop_threshold=CROP_THRESHOLD,
                                                         loading_verbose=True, loading_pbar=True)

        return self.dart_pipeline

    def run_inference_pipeline(self, update_progress_func, update_screen_func):
        """
        Runs the inference pipeline on all images.
        Currently also updates the GUI screen after every image.
        """

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
            update_progress_func(80 / len(self.images))
            update_screen_func()

        print('Inference complete!')

        return results
