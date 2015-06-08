import numpy as np

import cv2
import cv2.cv as cv

class faceDetector:
    def __init__(self):
        self.cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_alt.xml")

    def detect(self, img):
        rects = self.cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
        if len(rects) == 0:
            print "no face\n"
            return []
        #rects[:,2:] += rects[:,:2]
        print "see face\n"
        return rects

    def findFace(self, img):
        print "start detect faces"
        gray = cv2.cvtColor(np.array(cv.GetMat(img)), cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        rects = self.detect(gray)

        max_area = 0
        max_rect = (0,0,0,0)

        for rect in rects:
            max_rect = (rect[0], rect[1], rect[2], rect[3])
            '''
            if rect[2]*rect[3] > max_area:
                max_rect = (rect[0], rect[1], rect[2], rect[3])
            #'''
                
        return max_rect
