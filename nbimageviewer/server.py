import json
import logging
import asyncio
import tornado.web as web
import tornado.websocket as ws
import tornado.escape
import tornado.ioloop


class Application(web.Application):
    def __init__(self, port=None, path=None):
        if port is None or path is None:
            raise ValueError("port and id value cannot be None.")
        handlers = [(r"/" + path, SocketHandler, {"port": port, "path": path})]
        super(Application, self).__init__(handlers)


class SocketHandler(ws.WebSocketHandler):
    """Handler for socket connections.
    """
    py_client = None
    js_client = None
    view_args = {}

    @classmethod
    def send_data(cls, data):
        logging.info("Sending data to js client")
        try:
            cls.js_client.write_message(data)
        except Exception as e:
            logging.error("Error sending data", exc_info=True)

    def initialize(self, port, path):
        self._port = port
        self._path = path

    def on_message(self, message):
        json_msg = tornado.escape.json_decode(message)
        msg_key = next(iter(json_msg))
        if msg_key == "py_client":
            SocketHandler.py_client = self
            logging.info("Python client connected.")
            SocketHandler.view_args = json_msg[msg_key]
        elif msg_key == "js_client":
            SocketHandler.js_client = self
            logging.info("JavaScript client connected.")
            if SocketHandler.view_args is not None:
                SocketHandler.send_data(json.dumps(SocketHandler.view_args))
                SocketHandler.view_args = None
        else:
            if SocketHandler.js_client is None:
                SocketHandler.view_args[msg_key] = json_msg[msg_key]
            else:
                SocketHandler.send_data(json_msg)

    def on_close(self):
        if self == SocketHandler.py_client:
            SocketHandler.py_client = None
        else:
            SocketHandler.js_client = None

    def check_origin(self, origin):
        return "localhost" in origin


if __name__ == "__main__":
    app = Application()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()
