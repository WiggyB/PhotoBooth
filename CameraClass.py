from picamera import PiCamera
import time


class CameraObject:

    # Constructor for camera object
    def __init__(self):
        self.camera = PiCamera()
        self.camera.rotation = 200
        self.camera.resolution = (2592, 1944)
        self.camera.framerate = 15

    def open_window(self):
        self.camera.start_preview(fullscreen=False, window=(0, -80, 640, 640))

    def close_window(self):
        self.camera.stop_preview()

    def take_picture(self, number):
        self.open_window()
        time.sleep(3)
        self.camera.capture('/home/pi/Desktop/image%s.jpg' % number)
        self.close_window()
        return '/home/pi/Desktop/image%s.jpg' % number
