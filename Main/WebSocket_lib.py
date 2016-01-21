import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import os

def check_origin(self, origin):
    return True
 
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('new connection')
      
    def on_message(self, message):
        print('message received:  %s' % message)
        # Reverse Message and send it back
        #print('sending back message: %s' % message[::-1])
        #self.write_message(message[::-1])
 
    def on_close(self):
        print('connection closed')
 
    def check_origin(self, origin):
        return True
 
class MainHandler(tornado.websocket.WebSocketHandler):
	def get(self):
		self.render("index.html")
		
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

 
Application = tornado.web.Application([
	(r"/", MainHandler),
	(r'/ws', WSHandler),
], **settings)

def StartWebsocket(*args, **kwargs):
	port=8000
	http_server = tornado.httpserver.HTTPServer(Application)
	http_server.listen(port)
	myIP = socket.gethostbyname(socket.gethostname())
	print('*** Websocket Server Started at %s***' % myIP)
	tornado.ioloop.IOLoop.current().start()
	print("Websocket stopped.")

def StopWebsocket():
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_callback(ioloop.stop)
    print("Stopping Websocket.")


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application)
    http_server.listen(8000)
    myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
