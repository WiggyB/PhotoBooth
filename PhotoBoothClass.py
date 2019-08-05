import os
import ImageMergeMulti
from PIL import Image, ImageTk
import multiprocessing

# If running on Raspberry pi import proper classes, if not run Dummy classes
if os.uname()[4][:3] == 'arm':
    import CameraClass
    import TwitterClass
    import DropboxClass
else:
    import CameraClassTest as CameraClass
    import TwitterClassTest as TwitterClass
    import DropboxClassTest as DropboxClass


class PhotoBooth:

    # Dropbox Tokens
    dropbox_token = "LXdgcDzVpX4AAAAAAAADw175Brf7pYw6KLYUkXkyMhJnQzXiQ4uXW5ngtskcF-Wj"

    # Twitter Tokens
    token = "1097906118603558912-8qi7HRS0dBIOPg5igxxlcL2Z6P27IY"
    token_secret = "6qFafsqUFPwUKtljd5WYGvt1xTtfUMYJH5UYuLzCj7inF"
    consumer_key = "wQy0diWcyl1G4GP4eF1arBPtS"
    consumer_secret = "B3JsT7UuB57ncKhZD174iR6k3kQ8lhKa6xj51h9i9l0mfO7S8F"
    # image_size = (1920, 1080)
    preview_ratio = 5
    image_size = (2592, 1944)
    preview_size = (500, 375)

    def __init__(self):

        self.twitter = TwitterClass.TwitterObject(token=self.token,
                                                  token_secret=self.token_secret,
                                                  consumer_key=self.consumer_key,
                                                  consumer_secret=self.consumer_secret)
        self.camera = CameraClass.CameraObject(self.image_size)
        self.dropbox = DropboxClass.DropboxObject(self.dropbox_token)
        self.dropbox_folder = "Wedding"    # The folder the file will be stored in

        self.background_choice = 0
        self.backgrounds_select = []
        self.backgrounds_full = []
        self.backgrounds_preview = []
        self.ImageNumber = 0
        self.merge_path = ''
        self.image = None

        images = ["images/nature.jpg", "images/punk.jpg", "images/spacebackground.jpg"]

        for image in images:
            data = Image.open(image)
            select_image = data.resize((int(data.size[0]/self.preview_ratio), int(data.size[1]/self.preview_ratio)),
                                       Image.ANTIALIAS)
            select_image = ImageTk.PhotoImage(select_image)
            full_image = data.resize(self.image_size, Image.ANTIALIAS)
            preview_image = data.resize(self.preview_size, Image.ANTIALIAS)
            self.backgrounds_select.append(select_image)
            self.backgrounds_full.append(full_image)
            self.backgrounds_preview.append(preview_image)

        # Config file will hold any data that needs to be saved, currently only picture number is stored
        # Will use later to store info about images that haven't been uploaded yet, in case of an internet outage
        exists = os.path.isfile('config.cfg')
        if exists:
            # File exists
            f = open('config.cfg', 'r')
            self.picture_number = int(f.readline())
            f.close()
        else:
            # File does not exist
            f = open('config.cfg', 'x')
            self.picture_number = 0
            f.write(str(self.picture_number))
            f.close()

    def take_picture(self, user_interface):
        self.picture_number += 1
        self.image = self.camera.take_picture()
        preview_image = self.image.resize(self.preview_size, Image.ANTIALIAS)
        merged_preview = ImageMergeMulti.merge(preview_image, self.backgrounds_preview[self.background_choice])
        print(str(merged_preview.size))
        user_interface.app.set_merged_preview(merged_preview)
        user_interface.app.show_picture()

    # Takes the picture, sends it for processing and then sends relevant info to twitter and dropbox objects
    def accept_picture(self):
        # Send to image manipulation class
        f = open('config.cfg', 'w')
        f.write(str(self.picture_number))
        f.close()
        merged_image = ImageMergeMulti.merge(self.image, self.backgrounds_full[self.background_choice])
        dropbox_process1 = multiprocessing.Process(self.dropbox.upload_picture(merged_image,
                                                                               self.dropbox_folder,
                                                                               self.picture_number))
        dropbox_process2 = multiprocessing.Process(self.dropbox.upload_picture(self.image, self.dropbox_folder,
                                                                               str(self.picture_number) + "RAW"))
        twitter_process = multiprocessing.Process(self.twitter.tweet_picture(merged_image, "Picture Number " +
                                                                             str(self.picture_number) +
                                                                             ". #KatieChris2019"))
        processes = [dropbox_process1, dropbox_process2, twitter_process]

        for process in processes:
            process.start()
            print("process started")
