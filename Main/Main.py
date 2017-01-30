#!/usr/bin/python

import array, time, serial, os.path, threading, os, sys, socket, tornado.web, tornado.ioloop, tornado.websocket, tornado.httpserver
from random import randint
from subprocess import call
from math import *
#from graphics import *
from PIL import Image
from timeit import default_timer as timer
#import LED
from LED import *#findmode, setMotiv, single,
from Snake import *

Serial=True
debug=True
Preview=False

boxsize = 40
cols = 16
rows = 16
hue = 1
framerate = 24
port=8888

start = 0
mode=1

direction=None



settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}


def timeitstart():
	global start
	if(debug):	start = timer()
def timeitend():
	if(debug):
		end = timer()
		print(end - start)
		print("for this frame")
	
class WSHandler(tornado.websocket.WebSocketHandler):
	global direction, Media, CurrentDisplay
	
	def check_origin(self, origin):
		return True

	def open(self):
		global CurrentDisplay
		print('new connection')
		
	def on_message(self, message):
		global CurrentDisplay
		#print('message received:  %s' % message)
		if(message=="lolz"):
			CurrentDisplay.stop()
			print("stopped")
		elif(message[:3]=="dir"):
			#print("dir detected")
			direction=message[3:]
			#print(direction)
			setDir(direction)
		elif(message[:5]=="media"):
			Media=message[5:]
			print(Media)
			if(isinFiles(Media)):
				mode=findmode(Media)
				fps=findfps(Media)
				CurrentDisplay.stop()
				CurrentDisplay = setPeriodicCallback(Media, findmode(Media), fps)
				CurrentDisplay.start()
		elif(message[:4]=="game"):
			game=message[4:]
			if(game=="snake"):
				SnakeRST()
				delay=1000/24
				CurrentDisplay.stop()
				CurrentDisplay = tornado.ioloop.PeriodicCallback(snake, delay)
				CurrentDisplay.start()
			
	def on_close(self):
		print('connection closed')	

 
class MainHandler(tornado.websocket.WebSocketHandler):
	def check_origin(self, origin):
		return True
	def get(self):
		self.render("index.html")

def StartWebsocket(port):
	http_server = tornado.httpserver.HTTPServer(Application)
	http_server.listen(port)
	myIP = socket.gethostbyname(socket.gethostname())
	if debug: print('*** Websocket Server Started at {0}:{1}***'.format(myIP,port))
	tornado.ioloop.IOLoop.instance().start()
	if debug: print("Websocket stopped.")

def StopWebsocket():
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_callback(ioloop.stop)
    if debug: print("Stopping Websocket...")
		
Application = tornado.web.Application([
	(r"/", MainHandler),
	(r'/ws', WSHandler),
], **settings)

def setPeriodicCallback(Media, mode, fps = None):
	if(fps==None):fps=24
	if(Media!=None): 
		setMotiv(Media,mode)
		fps = findfps(Media)
	delay = int(1000/fps)
	if(mode==1):
		CurrentDisplay = tornado.ioloop.PeriodicCallback(single, delay)
		return CurrentDisplay
	elif(mode==2): 
		CurrentDisplay = tornado.ioloop.PeriodicCallback(vertical, delay)
		return CurrentDisplay
	elif(mode==4):
		CurrentDisplay = tornado.ioloop.PeriodicCallback(multiple, delay)
		return CurrentDisplay
	elif(mode==3):
		CurrentDisplay = tornado.ioloop.PeriodicCallback(horizontal, delay)
		return CurrentDisplay
	elif(mode==5):
		CurrentDisplay = tornado.ioloop.PeriodicCallback(singlecolor, delay)
		return CurrentDisplay
	else: print("Unknown mode.")

CurrentDisplay = setPeriodicCallback("mario", 1, 1)
CurrentDisplay.start()


			
StartWebsocket(port)
