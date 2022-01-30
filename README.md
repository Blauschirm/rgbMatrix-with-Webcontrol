A project to control a 16x16 Matrix of WS2812b LEDs.

All LEDs are wired in series in a zig-zag pattern and are controlled via an Arduino that is connected via a 1Mbps Serial Connection.

The script uses Tornado to host a website for controlling the Matrix.
The web interface is connected to the main Script via a bilateral websocket Connection, to send commands to the server and receive a preview that is displayed as a canvas.

The current contents are:
 - displaying 16x16 pixel bitmaps
 - displaying animations as a sequence if 16x16 pixel bitmaps
 - a digital clock
 - the game snake
 - a binary counter that is displaying my age in milliseconds so I can watch myself age


Things that still need work are:
  - [ ] Redoing the web interface
    - [ ] replacing the current "style"
    - [ ] ssl encryption
    - [ ] adding Options like
      - [ ] adjusting brightness
      - [ ] a color picker for highlight colors
    - [ ] picking the bmps via a galery of previews
  