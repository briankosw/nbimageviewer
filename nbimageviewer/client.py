import json
import asyncio
from asyncio.queues import Queue
import io
import base64

import tornado.websocket as ws


class Client:
    """ Client class handles all the connection and data transfer that happens
        through the websocket for all types of image viewers.
    """

    def __init__(self, addr, images, labels, **view_args):
        """
        Args:
            addr: address of the websocket
            images: a list of images
            labels: a list of labels for each image
        """
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
                await self.queue.get_nowait()
            except asyncio.QueueEmpty:
                await asyncio.sleep(0)

    async def websocket_connect(self, view_args):
        """ Connects to the websocket at given address. Sends attributes and
            data following a signal to the client.

            Arguments:
                view_args: a dictionary of arguments to be passed to the
                           Javascript side
        """
        self.ws = await ws.websocket_connect(self._addr)
        message = {"py_client": None}
        await self.write_message(message)
        # Wait to send data until signal received from server
        while True:
            message = await self.ws.read_message()
            if message:
                await self.write_message({"attrs": view_args})
                await self.send_data()
                break
            await asyncio.sleep(0)

    async def write_message(self, message):
        """ Writes message to the websocket.

            Arguments:
                message: a dictionary that contains the message to be sent to
                         the Javascript side
        """
        while self.ws is None:
            await asyncio.sleep(0.001)
        message_json = json.dumps(message)
        await self.queue.put(asyncio.ensure_future(self.ws.write_message(message_json)))

    async def send_data(self):
        """ Send image data to front end.
        """
        images_bytes = list(map(Client.image2bytes, self._images))
        data_dict = {"data": {}}
        for i, image in enumerate(images_bytes):
            data_dict["data"][i] = image
        await self.write_message(data_dict)

    @staticmethod
    def image2bytes(image, quality=80):
        """ Converts PIL Image to bytearray.

            Arguments:
                image: image buffer in PIL Image format
                quality: the quality of the output image
        """
        bytesIO = io.BytesIO()
        image.save(bytesIO, format="JPEG", optimize=True, quality=quality)

        return base64.b64encode(bytesIO.getvalue()).decode()
