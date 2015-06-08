#!/usr/bin/env python

import httplib  	#httplib modules for the HTTP interactions
import StringIO 		#For converting Stream from the server to IO for Image (PIL)
from PIL import Image, ImageTk #Python Image Libraries, required for displaying jpegs

import cv2
import numpy as np
import threading

DEBUG  = False
OUTPUT = False

HOST  = '192.168.1.54'
PORT  = 8080
QUERY = '/?action=snapshot'


class Streamer(threading.Thread):
	def __init__(self, _host=HOST, _port=PORT, _query=QUERY):
		super(Streamer, self).__init__()  
		self.host = _host
		self.port = _port
		self.query = _query
		self.I = None

		#start the reciving stream
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True # Daemonize thread
		thread.start()  

	def run(self):
		while True:
			self.I = self.getStreamFromHost()
			if OUTPUT:
				img =Image.open(StringIO.StringIO(self.I)) #convert to jpeg object from the stream
				img = np.array(img)
				img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
				cv2.imshow("streaming client",img)
				cv2.waitKey(1)


	def getStreamFromHost(self):
		h = httplib.HTTP(self.host, self.port)
		h.putrequest('GET', self.query)
		h.putheader('Host', self.host)
		h.putheader('User-agent', 'python-httplib')
		h.putheader('Content-type', 'image/jpeg')
		h.endheaders()
		
		(returncode, returnmsg, headers) = h.getreply()
		if returncode != 200:
			print returncode, returnmsg
			sys.exit()

		if DEBUG:
			print "return code:",returncode
			print "return message:",returnmsg
			print "headers:",headers

		f = h.getfile()
		return f.read()

	def getFrame(self):
		raw = self.getStreamFromHost()
		img =Image.open(StringIO.StringIO(raw)) #convert to jpeg object from the stream
		img = np.array(img)
		img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

		if OUTPUT:
			cv2.imshow("streaming client",img)
			cv2.waitKey(1)
		return img

if __name__=="__main__":
	s = Streamer()
	while True:
		s.getFrame()

