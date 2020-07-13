import os

import IPython.display as display

from .image_viewer import ImageViewer, DIST_DIR


class Gallery(ImageViewer):
    """ Gallery displays a gallery of the provided images.
    """

    def __init__(self, images, labels=None, port=8889):
        """
            Args:
                images: a list of images
                labels: a list of labels for each image
                port: port number for connection
        """
        super(Gallery, self).__init__(images, labels, port)
        self.import_assets()

    def import_assets(self):
        assets_str = ""
        with open(os.path.join(DIST_DIR, "index.html"), "r") as f:
            assets_str = "".join([assets_str, f.read().format(self.id, "gallery")])
        with open(os.path.join(DIST_DIR, "gallery.js"), "r") as f:
            assets_str = "".join([assets_str, "<script>{}</script>".format(f.read())])
        display.display(display.HTML(assets_str))
