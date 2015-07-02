# iPET 
> Our final project of NTU IoT course on 2015 spring.

## Goal
we want to built a robot
- which can follow us around
- we can control it remotely
- we can see what it sees

## Work
#### Hardware:
- raspberry pi model B+ (with pi camera)
- two motors and two wheels
- 3D models designed by ourselves (see:  )

#### Software architecture:
######Algorithm
1. detect faces in current frame, and choose the biggest one to track
2. in following frames
   - track the face
   - see if we lose track of the face, yes -> goto step 1
   - move the face to the center of the frame

######Implementation
we have several classes: PET, camera, controller, tracker, face detector

**PET**
```
while True:
  get frame <== from camera
  track certain area <== by tracker
  try to move the area to the center of the frame <== use controller
```
**camera**
> interface of piCam

**controller**
> interface of motors
provide 5 functions: **rotateLeft**, **rotateRight**, **goForward**, **goBackward**, **stay**

**tracker**
```
if we lose track of face:
  detect face <== by face detector
  mark the face as "tracking area"

use camshift to track "tracking area"
```
**face detector**
```
detect faces
return area of the biggest one
```



  Pet
    streamer
    controller
    trackcer
      face detector
'''
  
Reference
  mjpeg-stream
  http://mjpeg-stream-client.googlecode.com/svn/trunk/ mjpeg-stream-client-read-only
  
