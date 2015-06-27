import cv2
import numpy as np

from controller import Controller
from camera import Camera
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
        #self.cam = Camera()
        self.controller = Controller()
        self.start_tracking = False
        self.track_window = (0,0,0,0)

        self.y_tolerance = 0.1
        self.default_ypos_percent = 0.4
        self.win_size_y = 480

        self.x_tolerance = 0.1
        self.default_xpos_percent = 0.5
        self.win_size_x = 640

        self.face_area = -1;
        self.area_tolerance = 10000

    def run(self):

        tr = tracker.tracker()
        while True:

            #self.frame = self.cam.getMat()
            self.frame = self.piStreamer.getFrame()

            tr_win = tr.track(self.frame)

            if self.start_tracking:
                #--- x
                if get_center_x(tr_win) > self.win_size_x * (self.default_xpos_percent + self.x_tolerance):
                    print "move right!!"
                    self.controller.goLeft()
                elif get_center_x(tr_win) < self.win_size_x * (self.default_xpos_percent - self.x_tolerance):
                    print "move left!!"
                    self.controller.goRight()
                else:
                    print "stay in horizontal!!"
                #--- then distance
                #--- if all function work well
                #--- we should calc "distance = area / cos(theta)"
                    if calc_area(tr_win) - self.area_tolerance > self.face_area:
                        print "back off!!"
                        self.controller.goForward()
                    elif calc_area(tr_win) + self.area_tolerance < self.face_area:
                        print "come forward!!"
                        self.controller.goBack()
                    else:
                        print "stay in distance!!"
                        self.controller.goStay()
                #--- y
                if get_center_y(tr_win) > self.win_size_y * (self.default_ypos_percent + self.y_tolerance):
                    print "move up your head!!"
                    # lower the cam
                    self.controller.lookLower()
                elif get_center_y(tr_win) < self.win_size_y * (self.default_ypos_percent - self.y_tolerance):
                    print "lower your head!!"
                    self.controller.lookUpper()
                    # raise the cam
                else:
                    print "stay in vertical!!"
                    # stay

            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            elif ch == ord("s"):
                self.face_area = calc_area(tr_win)
                self.start_tracking = True

        cv2.destroyAllWindows()

if __name__ == '__main__':    
    PET().run()
        
