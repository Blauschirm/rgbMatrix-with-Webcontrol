#!/usr/bin/python


import os
import os.path
import socket
import pickle
import json
import sys

from math import *
from os import urandom
from random import randint
from subprocess import call
from timeit import default_timer as timer

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket

from LED import * 
from Snake import Snake
from BinCounter import BinCounter
from Clock import Clock
from MediaPlayer import MediaPlayer

#from GameofLife import GameofLife

debug = True

port = 8888
 

class Config:
    def __init__(self):
        self.colors = {"highlight": (255, 120, 0)}
        self.clock = {"offset": False, "seconds": False, "seconds_smooted": False}

config_path = os.path.join(os.path.dirname(__file__), 'saves', 'config.pickle')
picture_root_folder = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "static/Images/Pixels")
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"), 
}


if os.path.exists(config_path):
    with open(config_path, mode="rb") as config_file:
        config = pickle.load(config_file)
else:
    config = Config()  
    config.colors["highlight"] = (255, 120, 0)

direction = None

snake = Snake()
clock = Clock(config)
binary_counter = BinCounter()
media_player = MediaPlayer(picture_root_folder)

def getDirection():
    global direction
    return direction

class WSHandler(tornado.websocket.WebSocketHandler):
    global direction, CurrentDisplay, media_player

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
        global CurrentDisplay, config
        #print('message received:  %s' % message)
        if message == "ready_for_config":
            print("sending config to client")
            self.write_message(json.dumps({"highlight_color": config.colors["highlight"]}))
        elif message[:15] == "highlight_color":
            global highlight_color
            highlight_color_str = message[17:].split(",")
            highlight_color = tuple(int(v) for v in highlight_color_str)
            config.colors["highlight"] = highlight_color
        elif message[:3] == "dir": 
            global direction, snake
            direction = message[3:]
            if snake: snake.setDir(direction)
        elif message[:5] == "media":
            name = message[5:]
            media_player.set_media_by_name(name)
            print(name)
            CurrentDisplay.stop()
            CurrentDisplay = tornado.ioloop.PeriodicCallback(media_player.update, media_player.media_frametime_ms)
            CurrentDisplay.start()
        elif message[:4] == "game":
            game = message[4:]
            if game == "snake":
                delay = 1000/15
                snake = Snake()
                snake.reset()
                CurrentDisplay.stop()
                CurrentDisplay = tornado.ioloop.PeriodicCallback(snake.update, delay)
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
                global binary_counter
                CurrentDisplay.stop()
                CurrentDisplay = tornado.ioloop.PeriodicCallback(binary_counter.update, 15)
                CurrentDisplay.start()
            if message[3:] == "clock":
                print("Starting Clock")
                global clock
                CurrentDisplay.stop()
                CurrentDisplay = tornado.ioloop.PeriodicCallback(clock.update, 500)
                CurrentDisplay.start()
        
        # Save config to file
        with open(config_path, mode="wb") as config_file:
            pickle.dump(config, config_file)
            
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
    if debug: print('*** Webserver Server Started at {0}:{1}***'.format(myIP, port))
    tornado.ioloop.IOLoop.instance().start()
    if debug: print("Websocket stopped.")

def StopWebsocket():
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_callback(ioloop.stop)
    if debug: print("Stopping Webserver...")
        
Application = tornado.web.Application([
    (r"/", MainHandler), 
    (r'/ws', WSHandler), 
], **settings)

if __name__ == "__main__":
    print("Starting")
    CurrentDisplay = tornado.ioloop.PeriodicCallback(clock.update, 15)
    CurrentDisplay.start()   
    
    StartWebsocket(port)   
