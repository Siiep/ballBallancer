from picamera import PiCamera
from time import sleep

#PiCamera is the built-in camera input from the raspberry pi module.
camera = PiCamera()
camera.resolution = (320, 240) #sets resolution to 320 px to 240 px
camera.framerate = 32 #sets MAZ framerate


#starts the camera
camera.start_preview()

#waits 10 seconds
sleep(10)

#stops the camera
camera.stop_preview()
