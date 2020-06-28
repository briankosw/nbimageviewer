import os
import asyncio

import IPython.display as display

from . import image_viewer

CAROUSEL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/assets/carousel"


class Carousel(image_viewer.ImageViewer):
    """
        Carousel displays a carousel of the provided images.
    """

    def __init__(self, images, labels=None, port=8889):
        super(Carousel, self).__init__(images, labels, port)
        self.import_assets()
        display.display(display.HTML(CAROUSEL_DIR + "/carousel.html"))
        asyncio.create_task(self.display())

    async def display(self):
        await self.client.websocket_connect()
        await self.client.ws.write_message("py_client")
        # await self.client.send_data()

    def import_assets(self):
        assets_str = ""
        asset_files = os.listdir(CAROUSEL_DIR)
        for asset_file in asset_files:
            if ".js" in asset_file:
                with open(os.path.join(CAROUSEL_DIR, asset_file), "r") as f:
                    assets_str = "".join(
                        [assets_str, "<script>{}</script>".format(f.read())]
                    )
            elif ".css" in asset_file:
                with open(os.path.join(CAROUSEL_DIR, asset_file), "r") as f:
                    assets_str = "".join(
                        [assets_str, "<style>{}</style>".format(f.read())]
                    )
        display.display(display.HTML(assets_str))
