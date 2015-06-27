
import numpy as np
import faceDetector as fD
import cv2
import time

def is_rect_nonzero(r):
    (_,_,w,h) = r
    return (w > 0) and (h > 0)

def calc_area((x0, y0, w, h)):
    return w*h

class tracker:
    def __init__(self):
        self.track_window = (0,0,0,0)
        self.tracking_state = 0
        self.faceDetector = fD.faceDetector()
        self.init = False
        self.faceScaleDown = 0.8
        self.minFaceArea = 225
        self.maxFaceArea = 300000

        self.GUI = True
	if self.GUI:
            cv2.namedWindow('camshift')

    def show_hist(self):
        bin_count = self.hist.shape[0]
        bin_w = 24
        img = np.zeros((256, bin_count*bin_w, 3), np.uint8)
        for i in xrange(bin_count):
            h = int(self.hist[i])
            cv2.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        cv2.imshow('hist', img)

    def track(self, frame):
        cv2.imshow('tracker', frame)

        if calc_area(self.track_window) < self.minFaceArea or \
           calc_area(self.track_window) > self.maxFaceArea:
            self.init = False

        vis = frame.copy()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))

        if not self.init:
            (x0, y0, w, h) = self.faceDetector.findFace(frame)
            self.track_window = (int(x0+(1-self.faceScaleDown)/2*w), \
                                 int(y0+(1-self.faceScaleDown)/2*h), \
                                 int(self.faceScaleDown*w), \
                                 int(self.faceScaleDown*h))

            if not is_rect_nonzero(self.track_window):
                return self.track_window
                

            #when we got track_window, then pre-process
            (x0, y0, w, h) = self.track_window
            x1 = x0 + w
            y1 = y0 + h
            hsv_roi = hsv[y0:y1, x0:x1]
            mask_roi = mask[y0:y1, x0:x1]
            hist = cv2.calcHist( [hsv_roi], [0], mask_roi, [16], [0, 180] )
            cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX);
            self.hist = hist.reshape(-1)
            if self.GUI:
                self.show_hist()

            vis_roi = vis[y0:y1, x0:x1]
            cv2.bitwise_not(vis_roi, vis_roi)
            vis[mask == 0] = 0

            self.init = True

        #start tracking
        prob = cv2.calcBackProject([hsv], [0], self.hist, [0, 180], 1)
        prob &= mask
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
        track_box, self.track_window = cv2.CamShift(prob, self.track_window, term_crit)

        try: cv2.ellipse(vis, track_box, (0, 0, 255), 2)
        except: print track_box

        if self.GUI:
            cv2.imshow('camshift', vis)

        return self.track_window
