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
    image_size = (2592, 1944)
    preview_size = (300, 300)

    def __init__(self, user_interface):

        self.UI = user_interface
        self.twitter = TwitterClass.TwitterObject(token=self.token,
                                                  token_secret=self.token_secret,
                                                  consumer_key=self.consumer_key,
                                                  consumer_secret=self.consumer_secret)
        self.camera = CameraClass.CameraObject(self.image_size)
        self.dropbox = DropboxClass.DropboxObject(self.dropbox_token)
        self.dropbox_folder = "Wedding"    # The folder the file will be stored in

        self.background_choice = 0
        self.backgrounds_preview = []
        self.backgrounds_full = []

        self.ImageNumber = 0

        self.merge_path = ''

        nature_image = Image.open("images/nature.jpg")
        nature_preview = nature_image.resize(self.preview_size, Image.ANTIALIAS)
        nature_preview = ImageTk.PhotoImage(nature_preview)
        nature_full = nature_image.resize(self.image_size, Image.ANTIALIAS)

        punk_image = Image.open("images/punk.jpg")
        punk_preview = punk_image.resize(self.preview_size, Image.ANTIALIAS)
        punk_preview = ImageTk.PhotoImage(punk_preview)
        punk_full = punk_image.resize(self.image_size, Image.ANTIALIAS)

        space_image = Image.open("images/spacebackground.jpg")
        space_preview = space_image.resize(self.preview_size, Image.ANTIALIAS)
        space_preview = ImageTk.PhotoImage(space_preview)
        space_full = space_image.resize(self.image_size, Image.ANTIALIAS)

        self.backgrounds_preview.append(nature_preview)
        self.backgrounds_preview.append(punk_preview)
        self.backgrounds_preview.append(space_preview)

        self.backgrounds_full.append(nature_full)
        self.backgrounds_full.append(punk_full)
        self.backgrounds_full.append(space_full)

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

    # Takes the picture, sends it for processing and then sends relevant info to twitter and dropbox objects
    def take_picture(self):
        self.picture_number += 1
        print("Calling picture object: " + str(time.time() - self.UI.start))
        image_path = self.camera.take_picture(self.picture_number)
        print("Picture object done: " + str(time.time() - self.UI.start))

        f = open('config.cfg', 'w')
        f.write(str(self.picture_number))
        f.close()

        # Send to image manipulation class
        print("starting merge function: " + str(time.time() - self.UI.start))
        self.merge_path = ImageMergeMulti.merge(image_path, self.backgrounds_full[self.background_choice])
        print("merge function finished: " + str(time.time() - self.UI.start))
        dropbox_process = multiprocessing.Process(self.dropbox.upload_picture(self.merge_path, self.dropbox_folder,
                                                                              self.picture_number))
        twitter_process = multiprocessing.Process(self.twitter.tweet_picture(self.merge_path, "Picture Number " +
                                                                             str(self.picture_number) +
                                                                             ". #KatieChris2019"))
        dropbox_process.start()
        twitter_process.start()

        # self.dropbox.upload_picture(self.merge_path, self.dropbox_folder, self.picture_number)
        # self.twitter.tweet_picture(self.merge_path, "Picture Number " + str(self.picture_number) +
        #  ". #KatieChris2019")
        # self.UI.frame.process_complete()

    def get_merge_path(self):
        return self.merge_path
