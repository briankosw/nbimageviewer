import json
import asyncio
import tornado.websocket as ws


class Client:
    def __init__(self, url):
        self.ws = None
        self.url = url

    async def websocket_connect(self):
        self.ws = await ws.websocket_connect(self.url)

        return self

    async def send_data(self):
        pass
