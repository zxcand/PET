import cv2.cv as cv
import time as time

import faceDetector as fD

def is_rect_nonzero(r):
    (_,_,w,h) = r
    return (w > 0) and (h > 0)

class tracker:
    def __init__(self):
        self.track_window = (0,0,0,0)
        track_box = None
        self.hist = cv.CreateHist([180], cv.CV_HIST_ARRAY, [(0,180)], 1 )
        self.faceDetector = fD.faceDetector()
        self.init = False
        self.GUI = True
        self.faceScaleDown = 0.8

        if self.GUI:
            cv.NamedWindow( "CamShiftDemo", 1 )
            cv.NamedWindow( "Histogram", 1 )

    def hue_histogram_as_image(self, hist):
        """ Returns a nice representation of a hue histogram """

        histimg_hsv = cv.CreateImage( (320,200), 8, 3)

        mybins = cv.CloneMatND(hist.bins)
        cv.Log(mybins, mybins)
        (_, hi, _, _) = cv.MinMaxLoc(mybins)
        cv.ConvertScale(mybins, mybins, 255. / hi)

        w,h = cv.GetSize(histimg_hsv)
        hdims = cv.GetDims(mybins)[0]
        for x in range(w):
            xh = (180 * x) / (w - 1)  # hue sweeps from 0-180 across the image
            val = int(mybins[int(hdims * x / w)] * h / 255)
            cv.Rectangle( histimg_hsv, (x, 0), (x, h-val), (xh,255,64), -1)
            cv.Rectangle( histimg_hsv, (x, h-val), (x, h), (xh,255,255), -1)

        histimg = cv.CreateImage( (320,200), 8, 3)
        cv.CvtColor(histimg_hsv, histimg, cv.CV_HSV2BGR)
        return histimg

    def track(self, frame):
        print "start tracking\n"

        if not self.init:            
            while not is_rect_nonzero(self.track_window):
                #c = cv.WaitKey(7) % 0x100
                time.sleep(.07)
                print "find face first\n"
                (x1, y1, w, h) = self.faceDetector.findFace(frame)
                self.track_window = (int(x1+(1-self.faceScaleDown)/2*w), \
                                     int(y1+(1-self.faceScaleDown)/2*h), \
                                     int(self.faceScaleDown*w), \
                                     int(self.faceScaleDown*h))

        # Convert to HSV and keep the hue
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        self.hue = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.Split(hsv, self.hue, None, None, None)
        
        # Compute back projection
        backproject = cv.CreateImage(cv.GetSize(frame), 8, 1)

        if not self.init:
            sub = cv.GetSubRect(frame, self.track_window)
            save = cv.CloneMat(sub)
            cv.ConvertScale(frame, frame, 0.5)
            cv.Copy(save, sub)
            x,y,w,h = self.track_window
            cv.Rectangle(frame, (x,y), (x+w,y+h), (255,255,255))

            sel = cv.GetSubRect(self.hue, self.track_window )
            cv.CalcArrHist( [sel], self.hist, 0)
            (_, max_val, _, _) = cv.GetMinMaxHistValue( self.hist)
            if max_val != 0:
                cv.ConvertScale(self.hist.bins, self.hist.bins, 255. / max_val)

            self.init = True

        # Run the cam-shift
        cv.CalcArrBackProject( [self.hue], backproject, self.hist )
        if is_rect_nonzero(self.track_window):
            crit = ( cv.CV_TERMCRIT_EPS | cv.CV_TERMCRIT_ITER, 10, 1)
            (iters, (area, value, rect), track_box) = cv.CamShift(backproject, self.track_window, crit)
            self.track_window = rect

        if self.track_window and is_rect_nonzero(self.track_window):
            cv.EllipseBox( frame, track_box, cv.CV_RGB(255,0,0), 3, cv.CV_AA, 0 )

        if self.GUI:
            cv.ShowImage( "CamShiftDemo", frame )
            cv.ShowImage( "Histogram", self.hue_histogram_as_image(self.hist))        

        return self.track_window
        
