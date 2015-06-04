#!/usr/bin/env python
import httplib    #httplib modules for the HTTP interactions
from Tkinter import * #Tkinter modules for Windowing
from PIL import Image, ImageTk #Python Image Libraries, required for displaying jpegs
from time import sleep
import StringIO 		#For converting Stream from the server to IO for Image (PIL)
from StreamViewer import StreamViewer 		
import cv2
import numpy as np         
'''Gets the file from the specified
host, port and location/query'''
def get(host,port,query):
     h = httplib.HTTP(host, port)
     h.putrequest('GET', query)
     h.putheader('Host', host)
     h.putheader('User-agent', 'python-httplib')
     h.putheader('Content-type', 'image/jpeg')
     h.endheaders()
     
     (returncode, returnmsg, headers) = h.getreply()
     print "return code:",returncode
     print "return message:",returnmsg
     print "headers:",headers
     if returncode != 200:
         print returncode, returnmsg
         sys.exit()
     
     f = h.getfile()
     return f.read()

'''This is where we show the file on our StreamViewer'''
def streamfile(tbk, root):
     f = get('192.168.1.54',8080,'/?action=snapshot')
     img=Image.open(StringIO.StringIO(f)) #convert to jpeg object from the stream
     imagetk = ImageTk.PhotoImage(img) #Get a PhotoImage to pass to our Frame
     tbk.addImage(imagetk) #Image added
     root.update()
     I = np.array(img)
     I = cv2.cvtColor(I,cv2.COLOR_BGR2RGB)     
     cv2.imshow("tmp",I)
     cv2.waitKey(1)

root = Tk()
tbk = StreamViewer(root)
#As much space as we need, no more, no less
#we change the root geometry to the size of the streaming jpg #As much space as we need, no more, no less

root.geometry("%dx%d+0+0" % (640, 480))
root.resizable(False,False)
'''It's our overrated slideshow viewer .. hehe'''
while(1):
     streamfile(tbk,root)

