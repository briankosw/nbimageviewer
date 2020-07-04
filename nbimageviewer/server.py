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

    @classmethod
    def send_data(cls, data):
        """ Send data to JavaScript client.
        """
        logging.info("Sending data to js client")
        try:
            cls.js_client.write_message(data)
        except Exception as e:
            logging.error("Error sending data", exc_info=True)

    @classmethod
    def signal_py(cls):
        """ Signals to Python client that JavaScript client has
            succesfully connected.
        """
        logging.info("Signaling py_client")
        try:
            cls.py_client.write_message("js_client connected.")
        except Exception as e:
            logging.error("Error signaling py_client", exc_info=True)

    def initialize(self, port, path):
        self._port = port
        self._path = path

    def on_message(self, message):
        json_msg = tornado.escape.json_decode(message)
        msg_key = next(iter(json_msg))
        if msg_key == "py_client":
            SocketHandler.py_client = self
            logging.info("Python client connected.")
        elif msg_key == "js_client":
            SocketHandler.js_client = self
            logging.info("JavaScript client connected.")
            SocketHandler.signal_py()
        elif msg_key == "attrs":
            logging.info("Attributes received. Sending to js_client.")
            SocketHandler.send_data(json_msg)
        elif msg_key == "data":
            logging.info("Data received. Sending to js_client.")
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
