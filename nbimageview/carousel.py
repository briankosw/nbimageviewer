import IPython.display as display

from . import image_viewer


class Carousel(image_viewer.ImageViewer):
    def __init__(self, images, labels=None):
        super().__init__(images, labels)

    def display(self):
        print("Displaying carousel")
