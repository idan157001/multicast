import socket
import time
import struct
import mss
import mss.tools
from PIL import Image
class multicast_sender:
    def __init__(self):
        """Setting Multicast (IP,PORT),ttl,Socket Configuration"""
        self.multi_group = ("224.1.1.1",1234)
        self.ttl = struct.pack('b', 1)
        self.conf_socket() # creating the socket 

    def capture_screen(self):
        """ capturing screenshot and set the format to png file """
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
        start,stop = 0,64000
        msg = self.capture_screen()
        msg_len = len(msg)
        while True:
            
            if 64000 < msg_len:
                msg_len-= 64000
                sending = self.sock.sendto(msg[start:stop],self.multi_group)
                start,stop= stop,stop+64000
            else:
                sending = self.sock.sendto(msg[stop:],self.multi_group)
                print('image has been sent')
                start,stop = 0,64000
                msg = self.capture_screen()
                msg_len = len(msg)

            time.sleep(0.06)
            



def runner():
    try:
        multi_class = multicast_sender()
        multi_class.send_image()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    runner()