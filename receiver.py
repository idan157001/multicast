import socket
import struct
import os
import threading
import time
import cv2
from PIL import Image,ImageFile
import cv2 as cv
import io
import numpy as np
import sys
from pynput import keyboard

ImageFile.LOAD_TRUNCATED_IMAGES = True # permit sending large file on multicast
MULTICAST_GROUP = '224.1.1.1'
SERVER_ADDRESS = ('', 1234)





class Multicast_to_vid:
    def __init__(self):
        self.SCREEN_DATA = b"" # bytes of png
        self.screen_size = [1000,800]
        self.listen_to_multicast() # creating socket and bind to multicast

    def save_img(self):
        """receive bytes of png and connect it to full image """
        while True:
            data,addr = self.sock.recvfrom(64000)
            if data:
                self.SCREEN_DATA+= data
            else:
                self.load_frame()   # if picture is full show it on screen with opencv    

    def listen_to_multicast(self):
        """Create the socket"""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to the server address
        self.sock.bind(SERVER_ADDRESS)

        group = socket.inet_aton(MULTICAST_GROUP)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        return self.sock

    def load_frame(self):
        """load new image and show it on screen """ 
        
        image = Image.open(io.BytesIO(self.SCREEN_DATA))
        image = np.array(image)
        image = cv.resize(image,self.screen_size)
        cv.imshow('frame',image)
        self.SCREEN_DATA = b"" # reseting bytes of png after show it
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            sys.exit(1)

    def change_screen_size(self,key):
        """ resizing screen by pressing '-'/'+' key """
        
        SIZE = 50
        key = str(key)
        if key == "'+'":
           self.screen_size[0]+=SIZE; self.screen_size[1]+=SIZE
        elif key == "'-'":
            self.screen_size[0]-=SIZE; self.screen_size[1]-=SIZE





cls = Multicast_to_vid()

listener = keyboard.Listener(on_press=cls.change_screen_size)
save_image = threading.Thread(target=cls.save_img)

if __name__ == '__main__':
    listener.start()
    save_image.start()

