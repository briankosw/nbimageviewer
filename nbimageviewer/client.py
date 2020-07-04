import json
import asyncio
from asyncio.queues import Queue
import io
import base64

import tornado.websocket as ws


class Client:
    def __init__(self, addr, images, labels, **view_args):
        self._addr = addr
        self._images = images
        self._labels = labels
        self.ws = None
        # initialize queue and worker process
        self.queue = Queue()
        asyncio.create_task(self.worker())
        asyncio.create_task(self.websocket_connect(view_args))

    async def worker(self):
        """ Handles asynchronous tasks that are enqueued to the work queue.
        """
        while True:
            try:
                task = await self.queue.get_nowait()
            except asyncio.QueueEmpty:
                await asyncio.sleep(0.0001)

    async def websocket_connect(self, view_args):
        """ Connects to the websocket at given address.
        """
        self.ws = await ws.websocket_connect(self._addr)
        message = {"py_client": view_args}
        await self.write_message(message)

    async def write_message(self, message):
        """ Writes message to the websocket.
        """
        while self.ws is None:
            await asyncio.sleep(0.001)
        message_json = json.dumps(message)
        await self.queue.put(
            asyncio.ensure_future(self.ws.write_message(message_json))
        )

    async def send_data(self):
        """ Send image data to front end.
        """
        images_bytes = list(map(Client.image2bytes, self._images))
        data_dict = {"data": {}}
        for i, image in enumerate(images_bytes):
            data_dict["data"][i] = image
        await self.ws.write_message(json.dumps(data_dict))

    @staticmethod
    def image2bytes(image, quality=100):
        """ Converts PIL Image to bytearray.
        """
        bytesIO = io.BytesIO()
        image.save(bytesIO, format="JPEG", optimize=True, quality=quality)

        return base64.b64encode(bytesIO.getvalue()).decode()
