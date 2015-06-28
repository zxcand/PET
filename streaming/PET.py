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
        #self.piStreamer = LocalStreamer()
        self.cam = Camera()
        self.controller = Controller()
        self.start_tracking = False
        self.track_window = (0,0,0,0)

        self.y_tolerance = 0.1
        self.default_ypos_percent = 0.4
        self.win_size_y = 240
        self.win_center_y = self.win_size_y * self.default_ypos_percent

        self.x_tolerance = 0.1
        self.default_xpos_percent = 0.5
        self.win_size_x = 320
        self.win_center_x = self.win_size_x * self.default_xpos_percent

        self.face_area = 64000
        self.area_tolerance = 10000

        self.DegPerPix = 0.2
        self.step = 0.75

    def run(self):

        tr = tracker.tracker()
        while True:

            self.frame = self.cam.getMat()
            #self.frame = self.piStreamer.getFrame()

            tr_win = tr.track(self.frame)

            print tr_win
            if calc_area(tr_win) > 0:
                self.start_tracking = True
            else:
                self.start_tracking = False
                self.controller.goStay()

            if self.start_tracking:
                #--- x
                cur_center_x = get_center_x(tr_win)
                deviation_x = cur_center_x - self.win_center_x
                if deviation_x > self.win_size_x * self.x_tolerance:
                    print "move right!!"
                    #self.controller.goLeft( self.step * deviation_x * self.DegPerPix )
                elif deviation_x < - self.win_size_x * self.x_tolerance:
                    print "move left!!"
                    #self.controller.goRight( self.step * (-deviation_x) * self.DegPerPix )
                else:
                    print "stay in horizontal!!"
                #--- then distance
                #--- if all function work well
                #--- we should calc "distance = area / cos(theta)"
                    if calc_area(tr_win) - self.area_tolerance > self.face_area:
                        print "back off!!"
                        #self.controller.goForward()
                    elif calc_area(tr_win) + self.area_tolerance < self.face_area:
                        print "come forward!!"
                        #self.controller.goBack()
                    else:
                        print "stay in distance!!"
                        self.controller.goStay()
                #--- y
                cur_center_y = get_center_y(tr_win)
                deviation_y = cur_center_y - self.win_center_y
                if deviation_y > self.win_size_y * self.y_tolerance:
                    print "move up your head!!"
                    # lower the cam
                    self.controller.lookLower( self.step * (deviation_y) * self.DegPerPix )
                elif deviation_y < - self.win_size_y * self.y_tolerance:
                    print "lower your head!!"
                    self.controller.lookUpper( self.step * (-deviation_y) * self.DegPerPix )
                    # raise the cam
                else:
                    print "stay in vertical!!"
                    # stay

            '''            
            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            elif ch == ord("s"):
                self.face_area = calc_area(tr_win)
                self.start_tracking = True
            '''
        cv2.destroyAllWindows()

if __name__ == '__main__':    
    PET().run()
        
