from PIL import Image
import os, json, sys
import numpy as np

from time import sleep


from LED import numpy_flush



picture_root_folder = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "static/Images/Pixels")


class MediaPlayer():
    def __init__(self, picture_root_folder):
        self.picture_root_folder = picture_root_folder
        self.media_name = "flappy"
        self.media_path = "flappy"
        self.media_mode = "auto"
        self.media_fps  = 5
        self.current_image = None
        self.numpy_image = np.zeros((16, 16, 3), np.uint8)
        self.media_frames = 0
        self.current_index = 0

        self.update_handlers = {'s': self.single, 'h': self.horizontal, 'v': self.vertical, 'm': self.multiple}

    def set_media(self, name, info):
        # "flappy", {"path": "/flappy", "mode": "auto", "fps" : 5}
        self.media_name = name
        self.media_path = os.path.join(self.picture_root_folder, info["path"])
        print("self.media_path = " + self.media_path)
        self.media_mode = info["mode"]
        self.media_fps  = info["fps"]

        if self.media_mode not in ('v', 'h', 's', 'm'):
            self.media_mode = self.findmode()
        self.update_handler = self.update_handlers[self.media_mode]

        self.numpy_image = np.array(Image.open(self.media_path))

    def set_media_by_name(self, name):
        self.media_name = name
        with open("static/Images/medias.json", mode="rb") as json_file:
            media_catalog = json.load(json_file)
        if name in media_catalog:
            self.set_media(name, media_catalog[name])
        else:
            print(f"name '{name}' not in catalog!")
            
    def findmode(self):
        if(self.media_path[-4:] == ".bmp"):
            picture = Image.open(self.media_path)
            width, height = picture.size
            if(height % 16 == 0 and width % 16 == 0):
                if(height > 16 and width == 16):
                    self.media_frames = height//16
                    media_mode = 'v'
                elif(width > 16 and height == 16):
                    self.media_frames = width//16
                    media_mode = 'h'
                elif(height == 16 and width == 16):
                    self.media_frames = 1
                    media_mode = 's'
        else:
            picname = "0.bmp"
            complete_filepath = os.path.join(self.media_path, picname)
            picture = Image.open(complete_filepath)
            width, height = picture.size
            if(width == 16 and height == 16):
                media_mode = 'm'

            i = 0
            while(os.path.exists(os.path.join(self.media_path, f"{i}.bmp"))):
                if not Image.open(os.path.join(self.media_path, f"{i}.bmp")).size == (16, 16):
                    break
                i+=1

            self.media_frames = i
        return media_mode
    
    def update(self):
        self.update_handler()

    def single(self):
        matrix = np.array(self.current_image)
        numpy_flush(matrix)

    def vertical(self):
        matrix = self.numpy_image[16*self.current_index:16*(self.current_index+1), 0:16, :]
        numpy_flush(matrix)

        self.current_index += 1
        if(self.current_index >= self.media_frames):
            self.current_index = 0

    def horizontal(self):
        matrix = self.numpy_image[0:16, 16*self.current_index:16*(self.current_index+1), :]
        numpy_flush(matrix)

        self.current_index += 1
        if(self.current_index >= self.media_frames):
            self.current_index = 0

    def multiple(self):

        picname = str(self.current_index) + ".bmp"
        complete_filepath = os.path.join(self.media_path, picname)
        print(complete_filepath)

        picture = Image.open(complete_filepath)
        matrix = np.array(picture)
        numpy_flush(matrix)
        self.current_index += 1
        picname = str(self.current_index) + ".bmp"
        complete_filepath = os.path.join(self.media_path, picname)
        if not os.path.exists(complete_filepath):
            self.current_index = 0



class Media:
    def __init__(self, path, mode, requestedfps):
        self.path = path
        self.mode = mode
        self.fps = requestedfps


if __name__ == "__main__":
    mediaplayer = MediaPlayer(picture_root_folder = picture_root_folder)
    mediaplayer.set_media_by_name("nyancat")
    for i in range(20):
        mediaplayer.update()
        sleep(1/mediaplayer.media_fps)