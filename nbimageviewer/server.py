import logging
import nest_asyncio
import tornado.web as web
import tornado.websocket as ws
import tornado.escape


class Application(web.Application):
    def __init__(self):
        handlers = [(r"/", SocketHandler)]
        super(Application, self).__init__(handlers)


class SocketHandler(ws.WebSocketHandler):
    py_client = None
    js_client = None

    @classmethod
    def send_data(cls, data):
        logging.info("Sending data to js client")
        try:
            cls.js_client.write_message(data)
        except Exception as e:
            logging.error("Error sending data", exc_info=True)

    def on_message(self, message):
        message = tornado.escape.json_decode(message)["body"]
        if message == "py_client":
            py_client = self
            logging.info("Python client connected.")
        elif message == "js_client":
            js_client = self
            logging.info("JavaScript client connected.")
        elif message == "data":
            SocketHandler.send_data(message["data"])

    def on_close(self):
        if self == SocketHandler.py_client:
            SocketHandler.py_client = None
        else:
            SocketHandler.js_client = None

    def check_origin(self, origin):
        return "localhost" in origin
