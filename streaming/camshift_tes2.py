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

def calc_area((x0, y0, w, h)):
    return w*h

class App(object):
    def __init__(self):
        #self.cam = video.create_capture(video_src)
        self.piStreamer = LocalStreamer()
        self.start_tracking = False
        self.track_window = (0,0,0,0)

    def run(self):

        tr = tracker.tracker()
        while True:
            #ret, self.frame = self.cam.read()
            self.frame = self.piStreamer.getFrame()
            cv2.imshow('test',self.frame)
            cv2.waitKey(1)
            tr_win = tr.track(self.frame)

            if self.start_tracking:
                if calc_area(self.track_window) < calc_area(tr_win) - 100:
                    print "back off!!"
                if calc_area(self.track_window) > calc_area(tr_win) + 100:
                    print "come forward!!"

            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            elif ch == ord("s"):
                self.track_window = tr_win
                self.start_tracking = True

        cv2.destroyAllWindows()

if __name__ == '__main__':    
    App().run()
