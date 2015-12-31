__author__ = 'Adisorn'
import tornado.ioloop
import tornado.web
import tornado.websocket
import socket
import urlparse
import os
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/html')
        hostname = urlparse.urlparse("%s://%s"%(self.request.protocol, self.request.host)).hostname
        ip_address = socket.gethostbyname(hostname)
        print(ip_address)

        self.render('index.html', SERVER_NAME=ip_address, SERVER_PORT='8888', HTTPS='off')


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        #self.write_message(u"You said: " + message)
        content = json.loads(message)
        msg_type = content['MSG_TYPE']
        if msg_type == 'import':
            print("do import")
        elif msg_type == 'nlp':
            print("do nlp")
        elif msg_type == 'visualise':
            print("do visualisation")

    def on_close(self):
        print("WebSocket closed")

def make_app():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        "login_url": "/login",
        "xsrf_cookies": True,
    }
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ws", WebSocketHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
