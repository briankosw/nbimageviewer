import os
import logging
from uuid import uuid4
from abc import ABC, abstractmethod

import numpy as np
import PIL
import IPython.display as display

from .server import Application
from .client import Client

logging.getLogger().setLevel(logging.DEBUG)
DIST_DIR = os.path.dirname(os.path.realpath(__file__)) + "/assets/dist/"


class ImageViewer(ABC):
    """
        ImageViewer is an Abstract Base Class for different types of image
        viewing options. Since there are different pipelines and optimizations
        for different types of image viewing layouts, ImageViewer serves as a
        starting point that initializes and launches all the necessarily
        components that are shared amongst all the different layouts.
    """

    app = None

    def __init__(self, images, labels=None, port=8889, **kwargs):
        """
        Args:
            images: a list of images
            labels: a list of labels for each image
            port: port number for connection
        """
        self.id = uuid4().hex
        self.addr = "ws://localhost:" + str(port)
        # start application
        if ImageViewer.app is None:
            ImageViewer.app = Application(port=port)
            ImageViewer.app.listen(port)
        # add addr to window
        display.display(display.Javascript('window.addr = "{}"'.format(self.addr)))
        # add id to window
        display.display(display.Javascript('window.id = "{}"'.format(self.id)))
        # create client
        self.client = Client(self.addr, images, labels, **kwargs)

    @abstractmethod
    def import_assets(self):
        """ Imports relevant assets
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
