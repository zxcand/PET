#!/usr/bin/env python

'''
Camshift tracker
================

This is a demo that shows mean-shift based tracking
You select a color objects such as your face and it tracks it.
This reads from video camera (0 by default, or the camera number the user enters)

http://www.robinhewitt.com/research/track/camshift.html

Usage:
------
    camshift.py [<video source>]

    To initialize tracking, select the object with mouse

Keys:
-----
    ESC   - exit
    b     - toggle back-projected probability visualization
'''

import cv2
import video
from streamer import LocalStreamer
import tracker2 as tracker
#import controller as controller
import numpy as np

def calc_area((x0, y0, w, h)):
    return w*h
def get_center_x((x0, y0, w, h)):
    return x0+w/2
def get_center_y((x0, y0, w, h)):
    return y0+h/2

class App(object):
    def __init__(self):
        #self.cam = video.create_capture(video_src)
        self.piStreamer = LocalStreamer()
        self.start_tracking = False
        self.track_window = (0,0,0,0)
        
        self.win_default_y_percent = 0.35
        self.win_size_y = 480
        self.win_default_y = np.floor(self.win_size_y * self.win_default_y_percent)
        
        self.win_default_x_percent = 0.5
        self.win_size_x = 640
        self.win_default_x = np.floor(self.win_size_x * self.win_default_x_percent)

    def run(self):
        #con = controller.controller()
        tr = tracker.tracker()
        while True:
            #ret, self.frame = self.cam.read()
            self.frame = self.piStreamer.getFrame()
            #cv2.imshow('test',self.frame)
            #cv2.waitKey(1)
            tr_win = tr.track(self.frame)

            if self.start_tracking:
                #--- x
                if get_center_x(tr_win) > self.win_default_x + 15:
                    print "move right!!"
                elif get_center_x(tr_win) < self.win_default_x - 15:
                    print "move left!!"
                else:
                    print "stay in horizontal!!"
                #--- than distance
                    if calc_area(self.track_window) < calc_area(tr_win) - 1200:
                        print "back off!!"
                    elif calc_area(self.track_window) > calc_area(tr_win) + 1200:
                        print "come forward!!"
                    else:
                        print "stay in distance!!"
                #--- y
                if get_center_y(tr_win) > self.win_default_y + 15:
                    print "move up your head!!"
                elif get_center_y(tr_win) < self.win_default_y - 15:
                    print "lower your head!!"
                else:
                    print "stay in vertical!!"
                
                

            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            elif ch == ord("s"):
                self.track_window = tr_win
                self.start_tracking = True

        cv2.destroyAllWindows()

if __name__ == '__main__':    
    App().run()
