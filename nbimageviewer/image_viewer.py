import os
from abc import ABC, abstractmethod
import asyncio

import numpy as np
import PIL
import IPython.display as display

from .server import Application
from .client import Client

ASSETS_DIR = os.path.dirname(os.path.realpath(__file__)) + "/assets/"


class ImageViewer(ABC):
    """
        ImageViewer is an Abstract Base Class for different types of image
        viewing options. Since there are different pipelines and optimizations
        for different types of image viewing layouts, ImageViewer serves as a
        starting point that initializes and launches all the necessarily
        components that are shared amongst all the different layouts.
    """

    def __init__(self, images, labels=None, port=8889):
        # start application
        self.app = Application()
        self.app.listen(port)
        # add port to window
        display.display(display.Javascript("window.port = " + str(port)))
        initialize_scripts()
        # create client
        self.client = Client("ws://localhost:" + str(port), images, labels)
        # asyncio.create_task(self.display())

    @abstractmethod
    async def display(self):
        """ Abstract method that displays the provided images.
        """

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
                "Image input size ({}) does not match label input size({})".format(
                    len(images), len(labels)
                )
            )
        self._labels = labels  # FIX: random code to remove pylint warning


def initialize_scripts():
    """ Initializes the scripts inside the assets directory.
    """
    script_str = ""
    asset_dirs = os.listdir(ASSETS_DIR)
    for asset_dir in asset_dirs:
        asset_files = os.listdir(os.path.join(ASSETS_DIR, asset_dir))
        for asset_file in asset_files:
            if ".js" in asset_file:
                with open(os.path.join(ASSETS_DIR, asset_dir, asset_file), "r") as f:
                    script_str = "".join(
                        [script_str, "<script>{}</script>".format(f.read())]
                    )
            elif ".css" in asset_file:
                with open(os.path.join(ASSETS_DIR, asset_dir, asset_file), "r") as f:
                    script_str = "".join([script_str, "<style>{}</style>".format(f.read())])

    display.display(display.HTML(script_str))
