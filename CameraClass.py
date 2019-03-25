from picamera import PiCamera


class CameraObject:

    # Constructor for camera object
    def __init__(self):
        self.camera = PiCamera()
        self.camera.rotation = 200
        self.camera.resolution = (2592, 1944)
        self.camera.framerate = 15

    def start_preview(self):
        self.camera.start_preview()

    def stop_preview(self):
        self.camera.stop_preview()

    def take_picture(self, number):
        self.camera.capture('/home/pi/Desktop/image%s.jpg' % number)
        return
