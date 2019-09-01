#!/usr/bin/python


import os
import os.path
import socket
from math import *
from os import urandom
from random import randint
from subprocess import call
from timeit import default_timer as timer

import serial
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from PIL import Image

from LED import *  # findmode, setMotiv, single
from Snake import Snake
from BinCounter import BinCounter
#from GameofLife import GameofLife


debug = True
Preview = False

boxsize = 40
cols = 16
rows = 16
hue = 1
framerate = 24
port = 8888

start = 0
mode = 1
S = None
direction = None
BC = None


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"), 
}


def timeitstart():
    global start
    if debug: start = timer()
def timeitend():
    if debug:
        end = timer()
        print(end - start)
        print("for this frame")

def getDirection():
    global direction
    return direction

class WSHandler(tornado.websocket.WebSocketHandler):
    global direction, Media, CurrentDisplay

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {"permessage-deflate"}

    def check_origin(self, origin):
        return True

    def open(self):
        global CurrentDisplay
        print('new connection')
        setWSH(self)
        self.set_nodelay(True)

    def on_message(self, message):
        global CurrentDisplay
        #print('message received:  %s' % message)
        if message == "lolz":
            CurrentDisplay.stop()
            print("stopped")

        elif message[:3] == "dir": 
            global direction, S
            #print("dir detected")
            direction = message[3:]
            #print(direction)
            if S: S.setDir(direction)
        elif message[:5] == "media":
            Media = message[5:]
            print(Media)
            if isinFiles(Media):
                mode = findmode(Media)
                fps = findfps(Media)
                CurrentDisplay.stop()
                CurrentDisplay = setPeriodicCallback(Media, findmode(Media), fps)
                CurrentDisplay.start()
        elif message[:4] == "game":
            game = message[4:]
            if game == "snake":
                delay = 1000/15
                S = Snake()
                S.reset()
                CurrentDisplay.stop()
                CurrentDisplay = tornado.ioloop.PeriodicCallback(S.update, delay)
                CurrentDisplay.start()
            #if game == "GoL":
                #GoL = GameofLife()
                #GoL.reset()
                #delay = 10000
                #CurrentDisplay.stop()
                #CurrentDisplay = tornado.ioloop.PeriodicCallback(GoL.update, delay)
                #CurrentDisplay.start()
        elif message[:3] == "etc":
            if message[3:] == "bincounter":
                print("Starting binary counter")
                global BC
                if not BC:
                    BC = BinCounter()
                CurrentDisplay.stop()
                CurrentDisplay = tornado.ioloop.PeriodicCallback(BC.update, 100)
                CurrentDisplay.start()
            
    def on_close(self):
        print('connection closed')
        setWSH(None)    

class MainHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def get(self):
        self.render("index.html")

def StartWebsocket(port):
    http_server = tornado.httpserver.HTTPServer(Application)
    http_server.listen(port)
    myIP = socket.gethostbyname(socket.gethostname())
    if debug: print('*** Websocket Server Started at {0}:{1}***'.format(myIP, port))
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

def setPeriodicCallback(Media, mode, requested_fps = 24):
    fps = requested_fps
    if Media != None:
        setMotiv(Media, mode)
        fps = findfps(Media)
    delay = int(1000/fps)
    if mode == 1:
        CurrentDisplay = tornado.ioloop.PeriodicCallback(single, delay)
        return CurrentDisplay
    elif mode == 2: 
        CurrentDisplay = tornado.ioloop.PeriodicCallback(vertical, delay)
        return CurrentDisplay
    elif mode == 4:
        CurrentDisplay = tornado.ioloop.PeriodicCallback(multiple, delay)
        return CurrentDisplay
    elif mode == 3:
        CurrentDisplay = tornado.ioloop.PeriodicCallback(horizontal, delay)
        return CurrentDisplay
    elif mode == 5:
        CurrentDisplay = tornado.ioloop.PeriodicCallback(singlecolor, delay)
        return CurrentDisplay
    else: print("Unknown mode.")

if __name__ == "__main__":
    print("Starting")
    CurrentDisplay = setPeriodicCallback("mario", 1, 1)
    CurrentDisplay.start()       
    StartWebsocket(port)
