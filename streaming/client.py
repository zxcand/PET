#!/usr/bin/env python
import httplib    #httplib modules for the HTTP interactions
from Tkinter import * #Tkinter modules for Windowing
from PIL import Image, ImageTk #Python Image Libraries, required for displaying jpegs
from time import sleep
import StringIO 		#For converting Stream from the server to IO for Image (PIL)
import cv2
import numpy as np         


OUTPUT = True

def get(host,port,query):
    h = httplib.HTTP(host, port)
    h.putrequest('GET', query)
    h.putheader('Host', host)
    h.putheader('User-agent', 'python-httplib')
    h.putheader('Content-type', 'image/jpeg')
    h.endheaders()
     
    (returncode, returnmsg, headers) = h.getreply()
    if returncode != 200:
        print returncode, returnmsg
        sys.exit()

    if OUTPUT:
        print "return code:",returncode
        print "return message:",returnmsg
        print "headers:",headers

    f = h.getfile()
    return f.read()

def streamfile():
    f = get('192.168.1.54',8080,'/?action=snapshot')
    img=Image.open(StringIO.StringIO(f)) #convert to jpeg object from the stream
    I = np.array(img)
    I = cv2.cvtColor(I,cv2.COLOR_BGR2RGB)
    cv2.imshow("streaming client",I)
    cv2.waitKey(1)
    return I

