import time
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

        self.x_tolerance = 0.25
        self.default_xpos_percent = 0.5
        self.win_size_x = 320
        self.win_center_x = self.win_size_x * self.default_xpos_percent

        self.face_area = 10000 # 1600 == 1 m, 4000 == .3 m,
        self.dis_tolerance_closer = 2000
        self.dis_tolerance_farther = 1700

        self.DegPerPix = 0.2 # 0.2 at distance == 2 m
        self.dtPerDeg = 1.0/90
        self.step = 0.05

    def run(self):

        tr = tracker.tracker()
        t = time.time()
        while True:

            self.frame = self.cam.getMat()
            #self.frame = self.piStreamer.getFrame()

            tr_win = tr.track(self.frame)

            #print tr_win
            if calc_area(tr_win) > 0:
                self.start_tracking = True
                self.controller.setLed(True)
            else:
                self.start_tracking = False
                self.controller.setLed(False)
                self.controller.goStay()

            if self.start_tracking:
                #time.sleep(1.0/60)
                now = time.time()
                print int(1/(now-t)),'fps'
                t = now
                #time.sleep(1.0/60)
                print calc_area(tr_win)
                #--- x
                cur_center_x = get_center_x(tr_win)
                deviation_x = cur_center_x - self.win_center_x
                if deviation_x > self.win_size_x * self.x_tolerance:
                    #self.controller.goRight( self.step * (deviation_x) * self.DegPerPix )
                    self.controller.goRight()
                    #self.stop_t = now + self.step * (deviation_x) * self.DegPerPix * self.dtPerDeg
                    print "move right!!",self.step * (-deviation_x) * self.DegPerPix
                elif deviation_x < - self.win_size_x * self.x_tolerance:
                    print "move left!!",self.step * (deviation_x) * self.DegPerPix
                    #self.controller.goLeft( self.step * (-deviation_x) * self.DegPerPix )
                    self.controller.goLeft()
                    #self.stop_t = now + self.step * (-deviation_x) * self.DegPerPix * self.dtPerDeg
                else:
                    self.controller.goStay()
                    #print "stay in horizontal!!"
                #--- then distance
                #--- if all function work well
                #--- we should calc "distance = area / cos(theta)"
                    if calc_area(tr_win) - self.dis_tolerance_closer > self.face_area:
                        print "back off!!"
                        self.controller.goBackward()
                        self.stop_t = now #+ self.step * (deviation_x) * self.DegPerPix * self.dtPerDeg
                    elif calc_area(tr_win) + self.dis_tolerance_farther < self.face_area:
                        print "come forward!!"
                        self.controller.goForward()
                        self.stop_t = now #+ self.step * (deviation_x) * self.DegPerPix * self.dtPerDeg
                    else:
                        print "stay in distance!!"
                        self.stop_t = now
                        self.controller.goStay()
#'''

                #if self.stop_t <= now:
                if False:
                    self.controller.goStay()
#'''
                #print time.time() - now, "judging time"
                #--- y
                cur_center_y = get_center_y(tr_win)
                deviation_y = cur_center_y - self.win_center_y
                if deviation_y > self.win_size_y * self.y_tolerance:
                    print "move up your head!!"
                    # lower the cam
                    #self.controller.lookLower( self.step * (deviation_y) * self.DegPerPix )
                elif deviation_y < - self.win_size_y * self.y_tolerance:
                    print "lower your head!!"
                    #self.controller.lookUpper( self.step * (-deviation_y) * self.DegPerPix )
                    # raise the cam
                else:
                    print "stay in vertical!!"
                    # stay
#'''
'''            
            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            elif ch == ord("s"):
                self.face_area = calc_area(tr_win)
                self.start_tracking = True
#'''
#        cv2.destroyAllWindows()

if __name__ == '__main__':    
    PET().run()
        
