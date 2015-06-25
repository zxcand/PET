import cv2
import numpy as np

#from camera import Cam
import tracker2 as tracker
from streamer import LocalStreamer

def calc_area((x0, y0, w, h)):
    return w*h
def get_center_x((x0, y0, w, h)):
    return x0+w/2
def get_center_y((x0, y0, w, h)):
    return y0+h/2

class PET():
    def __init__(self):
        self.piStreamer = LocalStreamer()
        #self.cam = Cam()

        self.start_tracking = False
        self.track_window = (0,0,0,0)

        self.y_tolerance = 0.1
        self.default_ypos_percent = 0.4
        self.win_size_y = 480

        self.x_tolerance = 0.1
        self.default_xpos_percent = 0.5
        self.win_size_x = 640

    def run(self):

        tr = tracker.tracker()
        while True:

            #self.frame = self.cam.getFrame()
            self.frame = self.piStreamer.getFrame()

            tr_win = tr.track(self.frame)

            if self.start_tracking:
                #--- x
                if get_center_x(tr_win) > self.win_size_x * (self.default_xpos_percent + self.x_tolerance):
                    print "move right!!"
                elif get_center_x(tr_win) < self.win_size_x * (self.default_xpos_percent - self.x_tolerance):
                    print "move left!!"
                else:
                    print "stay in horizontal!!"
                #--- then distance
                    if calc_area(tr_win) - 10000 > calc_area(self.track_window):
                        print "back off!!"
                    elif calc_area(tr_win) + 10000 < calc_area(self.track_window):
                        print "come forward!!"
                    else:
                        print "stay in distance!!"
                #--- y
                if get_center_y(tr_win) > self.win_size_y * (self.default_ypos_percent + self.y_tolerance):
                    print "move up your head!!"
                    # lower the cam
                elif get_center_y(tr_win) < self.win_size_y * (self.default_ypos_percent - self.y_tolerance):
                    print "lower your head!!"
                    # raise the cam
                else:
                    print "stay in vertical!!"
                    # stay

            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            elif ch == ord("s"):
                self.track_window = tr_win
                self.start_tracking = True

        cv2.destroyAllWindows()

if __name__ == '__main__':    
    PET().run()
        
