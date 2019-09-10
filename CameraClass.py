from picamera import PiCamera
import io
from PIL import Image


# A wrapper around the PiCamera module
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

    def take_picture(self):
        self.close_window()
        # Creates the image as a Bytes object so it can stay in RAM instead of being saved to disk
        stream = io.BytesIO()
        self.camera.capture(stream, format='png')
        stream.seek(0)
        return Image.open(stream)

