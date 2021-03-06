## What is iPET?
- a robot pet which can follow us around
- a robot pet we can control it remotely
- a robot pet showing us what it sees

## Video
http://youtu.be/Oe8pGG040HU


## Work
#### Hardware:
- raspberry pi model B+ (with pi camera)
- two motors and two wheels
- 3D models designed by ourselves (see:  )

#### Software architecture:
#####Algorithm
1. detect faces in current frame, and choose the biggest one to track
2. in following frames
   1. track the face
   2. see if we lose track of the face, yes -> goto step 1
   3. move the face to the center of the frame

#####Implementation
we have several classes: PET, camera, controller, tracker, face detector

######PET
```
while True:
  get frame <== from camera
  track certain area <== by tracker
  try to move the area to the center of the frame <== use controller
```
######camera
> interface of piCam

######controller
> 
interface of motors  
provide 5 functions: **rotateLeft**, **rotateRight**, **goForward**, **goBackward**, **stay**

######tracker
```
if we lose track of face:
  detect face <== by face detector
  mark the face as "tracking area"

use camshift to track "tracking area"
```
######face detector
```
detect faces
return area of the biggest one
```

## Authors and Contributors
* [Fan Wang] (https://github.com/zxcand)  
* [Chih-Yang Chen] (https://github.com/Jayis)  
* Keng-Ming Lee  
**instructor** : Wei-Chao Chen

## Reference
1. *Rainer Lienhart and Jochen Maydt. An Extended Set of Haar-like Features for Rapid Object Detection. IEEE ICIP 2002, Vol. 1, pp. 900-903, Sep. 2002*
[[Implemented by OpenCV]] (http://docs.opencv.org/modules/objdetect/doc/cascade_classification.html?highlight=cascadeclassifier)
2. *Bradski, G.R. “Computer Vision Face Tracking for Use in a Perceptual User Interface”, Intel, 1998*
[[Implemented by OpenCV]] (http://docs.opencv.org/modules/video/doc/motion_analysis_and_object_tracking.html)
