from picamera import PiCamera
import io
from PIL import Image


# A wrapper around the PiCamera module
class CameraObject:

    def __init__(self, image_size):
        # Stream object that the raw image will; be temp stored in
        self.stream = io.BytesIO()
        self.camera = PiCamera()
        self.camera.rotation = 200
        self.camera.resolution = image_size
        self.camera.framerate = 15

    def open_window(self):
        self.camera.start_preview(fullscreen=False, window=(0, -80, 640, 640))

    def close_window(self):
        self.camera.stop_preview()

    def take_picture(self):
        self.close_window()
        self.camera.capture(self.stream, format='png')
        self.stream.seek(0)
        return Image.open(self.stream)
