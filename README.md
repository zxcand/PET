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
we have several classes: PET, camera, controller, tracker, face detector

**www**
```
x = 0
x = 2 + 2
what is x
```

'''
  Pet
    streamer
    controller
    trackcer
      face detector
'''
  
Reference
  mjpeg-stream
  http://mjpeg-stream-client.googlecode.com/svn/trunk/ mjpeg-stream-client-read-only
  
