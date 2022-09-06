import socket
import time
import struct
import mss
import mss.tools
from PIL import Image

class Multicast_sender:
    def __init__(self):
        """Setting Multicast (IP,PORT),ttl,Socket Configuration"""
        self.multi_group = ("224.1.1.1",1234)
        self.ttl = struct.pack('b', 1)
        self.conf_socket() # creating the socket 
        self.max_buffer = 64000

    def capture_screen(self):
        """ capturing screenshot and set the format to png file """
        #monitor_size = {'top': 800, 'left': 800, 'width': 800, 'height': 800}
        with mss.mss() as m:
            monitor = m.monitors[1]
            data = m.grab(monitor)
        png = mss.tools.to_png(data.rgb,data.size)
        
        return png
        
    def conf_socket(self):
        """ Configuration of the multicast socket """
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.ttl)
        self.sock.settimeout(0.1)

    def send_image(self):
        """
        Sending the png image on the multicast socket '64k' bytes maximum
        """
        start,stop = 0,self.max_buffer
        msg = self.capture_screen()
        msg_len = len(msg)
        while True:
            
            if self.max_buffer < msg_len:
                msg_len -= self.max_buffer
                sending = self.sock.sendto(msg[start:stop],self.multi_group)
                start,stop= stop,stop+self.max_buffer
            else:
                sending = self.sock.sendto(msg[stop:],self.multi_group)
                print('image has been sent')
                start,stop = 0,self.max_buffer
                msg = self.capture_screen()
                msg_len = len(msg)

            
            



def runner():
    try:
        multi_class = Multicast_sender()
        multi_class.send_image()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    runner()