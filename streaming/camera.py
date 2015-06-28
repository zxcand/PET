#!/usr/bin/env python
from flask import Flask, render_template, Response

import time
import io
import threading
import picamera
import cv2
import numpy as np


app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(Camera().gen(),
                mimetype='multipart/x-mixed-replace; boundary=frame')


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
        
    def __init__(self):
        pass

    def gen(self):
        """Video streaming generator function."""
        while True:
            frame = self.get_frame()
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        self.initialize()
        Camera.last_access = time.time()
        return self.frame
    
    def getMat(self):
        frame = self.get_frame()
        img = cv2.imdecode( np.fromstring(frame, np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
        return img 



    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.hflip = False
            camera.vflip = False

            # let camera warm up
            # camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None



if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)
