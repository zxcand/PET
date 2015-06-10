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
import tracker2 as tracker


class App(object):
    def __init__(self, video_src):
        self.cam = video.create_capture(video_src)
        ret, self.frame = self.cam.read()

    def run(self):
        tr = tracker.tracker()
        while True:
            ret, self.frame = self.cam.read()
            tr_win = tr.track(self.frame)

            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break

        cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    try: video_src = sys.argv[1]
    except: video_src = 0
    print __doc__
    App(video_src).run()
