import os
from abc import ABC, abstractmethod

import numpy as np
import PIL
import IPython.display as display


ASSETS_DIR = os.path.dirname(os.path.realpath(__file__)) + "/assets/"

class ImageViewer(ABC):
    """
        ImageViewer is an Abstract Base Class for different types of image
        viewing options.
    """
    def __init__(self, images, labels=None):
        self._images = images
        self._labels = labels
        self._init_script()

    @abstractmethod
    def display(self):
        """ Abstract method that displays the provided images.
        """
        pass

    def _validate_args(self, images, labels):
        """ Validates the arguments provided to the __init__ function.
        """
        if isinstance(images) == np.ndarray:
            pass
        elif isinstance(images) == list:
            if isinstance(images[0]) == "str":
                pass
            elif isinstance(images[0]) == PIL.Image:
                pass
        else:
            raise TypeError(
                "Image input type {} is not supported.".format(type(images))
            )
        if len(images) != len(labels):
            raise ValueError(
                "Image input size ({}) does not match label input size({})"
                    .format(len(images), len(labels))
            )

    def _init_script(self):
        """ Initializes the scripts inside the assets directory.
        """
        script_str = ""
        asset_files = os.listdir(ASSETS_DIR)
        for asset_file in asset_files:
            if ".js" in asset_file:
                with open(ASSETS_DIR + asset_file, 'r') as f:
                    script_str = ''.join([
                        script_str,
                        "<script>{}</script>".format(f.read())
                    ])
            elif ".css" in asset_file:
                with open(ASSETS_DIR + asset_file, 'r') as f:
                    script_str = ''.join([
                        script_str,
                        "<style>{}</style>".format(f.read())
                    ])

        display.display(display.HTML(script_str))
