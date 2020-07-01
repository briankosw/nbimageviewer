import json
import asyncio
import io
import base64

import tornado.websocket as ws


class Client:
    def __init__(self, addr, images, labels):
        self._addr = addr
        self._images = images
        self._labels = labels
        self.ws = asyncio.create_task(self.websocket_connect())

    async def websocket_connect(self):
        self.ws = await ws.websocket_connect(self._addr)

    async def send_data(self):
        images_bytes = list(map(Client.image2bytes, self._images))
        data_dict = {"data": {}}
        for i, image in enumerate(images_bytes):
            data_dict["data"][i] = image
        await self.ws.write_message(json.dumps(data_dict))

    @staticmethod
    def image2bytes(image, quality=100):
        bytesIO = io.BytesIO()
        image.save(bytesIO, format="JPEG", optimize=True, quality=quality)

        return base64.b64encode(bytesIO.getvalue()).decode()
