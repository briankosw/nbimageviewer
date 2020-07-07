import os
import json
import asyncio

import IPython.display as display

from .image_viewer import ImageViewer, DIST_DIR


class Carousel(ImageViewer):
    """ Carousel displays a carousel of the provided images.
    """

    def __init__(self, images, labels=None, port=8889, num_slides=1, num_scrolls=1):
        """
        Args:
            images: a list of images
            labels: a list of labels for each image
            port: port number for connection
            num_slides: number of slides visiable at once in the carousel
            num_scrolls: number by which value will change on scroll
        """
        super(Carousel, self).__init__(
            images, labels, port, slidesPerPage=num_slides, slidesPerScroll=num_scrolls
        )
        self.import_assets()
        self._num_slides = num_slides
        self._num_scrolls = num_scrolls

    def import_assets(self):
        assets_str = ""
        with open(os.path.join(DIST_DIR, "index.html"), "r") as f:
            assets_str = "".join([assets_str, f.read().format(self.id)])
        with open(os.path.join(DIST_DIR, "carousel.js"), "r") as f:
            assets_str = "".join([assets_str, "<script>{}</script>".format(f.read())])
        display.display(display.HTML(assets_str))

    @property
    def num_slides(self):
        return self._num_slides

    @num_slides.setter
    def num_slides(self, num_slides):
        self._num_slides = num_slides
        asyncio.create_task(
            self.client.write_message({"attrs": {"slidesPerPage": num_slides}})
        )

    @property
    def num_scrolls(self):
        return self._num_scrolls

    @num_slides.setter
    def num_scrolls(self, num_scrolls):
        self._num_scrolls = num_scrolls
        asyncio.create_task(
            self.client.write_message({"attrs": {"slidesPerScroll": num_scrolls}})
        )
