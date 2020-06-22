import logging
import json
import nest_asyncio
import tornado.web as web
import tornado.websocket as ws
import tornado.escape
import tornado.ioloop

logging.getLogger().setLevel(logging.DEBUG)


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
        try:
            json_msg = tornado.escape.json_decode(message)
            logging.info(json_msg)
            SocketHandler.send_data(json_msg)
        except json.JSONDecodeError:
            if message == "py_client":
                SocketHandler.py_client = self
                logging.info("Python client connected.")
            elif message == "js_client":
                SocketHandler.js_client = self
                logging.info("JavaScript client connected.")

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
