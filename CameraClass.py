from picamera import PiCamera


class CameraObject:

    def __init__(self, image_size):
        self.camera = PiCamera()
        self.camera.rotation = 200
        self.camera.resolution = image_size
        self.camera.framerate = 15

    def open_window(self):
        self.camera.start_preview(fullscreen=False, window=(0, -80, 640, 640))

    def close_window(self):
        self.camera.stop_preview()

    def take_picture(self, number):
        path = '/home/pi/Desktop/image%s.png' % number
        self.camera.capture(path, format='png')
        self.close_window()
        return path
