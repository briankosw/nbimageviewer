import os
import asyncio

import IPython.display as display

from . import image_viewer

ASSETS_DIR = os.path.dirname(os.path.realpath(__file__)) + "/assets/"


class Carousel(image_viewer.ImageViewer):
    """
        Carousel displays a carousel of the provided images.
    """
    def __init__(self, images, labels=None, port=8889):
        super(Carousel, self).__init__(images, labels, port)
        display.display(display.HTML(ASSETS_DIR + "carousel/carousel.html"))
        asyncio.create_task(self.display())

    async def display(self):
        await self.client.websocket_connect()
        await self.client.ws.write_message("py_client")
        # await self.client.send_data()
