import os
import ImageMergeMulti
from PIL import Image, ImageTk
import multiprocessing
import time

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
    preview_size = (640, 480)

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

        nature_image = Image.open("images/nature.jpg")
        nature_select = nature_image.resize((int(nature_image.size[0]/self.preview_ratio), int(nature_image.size[1]/self.preview_ratio)), Image.ANTIALIAS)
        nature_select = ImageTk.PhotoImage(nature_select)
        nature_full = nature_image.resize(self.image_size, Image.ANTIALIAS)
        nature_preview = nature_image.resize(self.preview_size, Image.ANTIALIAS)

        punk_image = Image.open("images/punk.jpg")
        punk_select = punk_image.resize((int(punk_image.size[0]/self.preview_ratio), int(punk_image.size[1]/self.preview_ratio)), Image.ANTIALIAS)
        punk_select = ImageTk.PhotoImage(punk_select)
        punk_full = punk_image.resize(self.image_size, Image.ANTIALIAS)
        punk_preview = punk_image.resize(self.preview_size, Image.ANTIALIAS)

        space_image = Image.open("images/spacebackground.jpg")
        space_select = space_image.resize((int(space_image.size[0]/self.preview_ratio), int(space_image.size[1]/self.preview_ratio)), Image.ANTIALIAS)
        space_select = ImageTk.PhotoImage(space_select)
        space_full = space_image.resize(self.image_size, Image.ANTIALIAS)
        space_preview = space_image.resize(self.preview_size, Image.ANTIALIAS)

        self.backgrounds_select.append(nature_select)
        self.backgrounds_select.append(punk_select)
        self.backgrounds_select.append(space_select)

        self.backgrounds_full.append(nature_full)
        self.backgrounds_full.append(punk_full)
        self.backgrounds_full.append(space_full)

        self.backgrounds_preview.append(nature_preview)
        self.backgrounds_preview.append(punk_preview)
        self.backgrounds_preview.append(space_preview)

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
        print("take picture background choice:" + str(self.background_choice))
        merged_preview = ImageMergeMulti.merge(preview_image, self.backgrounds_preview[self.background_choice])
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
