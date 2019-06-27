import os
# import ImageMerge
import ImageParellel as ImageMerge
from PIL import Image, ImageTk

# If running pi, import proper classes
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
    #image_size = (2592, 1944)
    image_size = (1920, 1080)
    preview_size = (300, 300)

    def __init__(self):

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

        nature_image = Image.open("nature.jpg")
        nature_preview = nature_image.resize(self.preview_size)
        nature_preview = ImageTk.PhotoImage(nature_preview)
        nature_full = nature_image.resize(self.image_size)
        # nature_full = ImageTk.PhotoImage(nature_full)

        punk_image = Image.open("punk.jpg")
        punk_preview = punk_image.resize(self.preview_size)
        punk_preview = ImageTk.PhotoImage(punk_preview)
        punk_full = punk_image.resize(self.image_size)
        # punk_full = ImageTk.PhotoImage(punk_full)

        space_image = Image.open("spacebackground.jpg")
        space_preview = space_image.resize(self.preview_size)
        space_preview = ImageTk.PhotoImage(space_preview)
        space_full = space_image.resize(self.image_size)
        # space_full = ImageTk.PhotoImage(space_full)

        self.backgrounds_preview.append(nature_preview)
        self.backgrounds_preview.append(punk_preview)
        self.backgrounds_preview.append(space_preview)

        self.backgrounds_full.append(nature_full)
        self.backgrounds_full.append(punk_full)
        self.backgrounds_full.append(space_full)

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

    def take_picture(self):
        self.picture_number += 1
        image_path = self.camera.take_picture(self.picture_number)

        f = open('config.cfg', 'w')
        f.write(str(self.picture_number))
        f.close()
        merge_path = ImageMerge.merge(image_path, self.backgrounds_full[self.background_choice], self.image_size)
        # Send to image manipulation class

        self.dropbox.upload_picture(merge_path, self.dropbox_folder, self.picture_number)
        self.twitter.tweet_picture(merge_path, "Picture Number " + str(self.picture_number) + ". #KatieChris2019")
