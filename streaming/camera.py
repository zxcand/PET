from time import time
import cv2
class Camera(object):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""

    def __init__(self):
        self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

    def get_frame(self):
        return self.frames[int(time()) % 3]

class Camera2(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
                 
    def get_frame(self):
        success, image = self.video.read()
        
        if not success:
            print 'Failed'
        cv2.imwrite('tmp.jpg',image)
        return open('tmp.jpg','rb').read()
