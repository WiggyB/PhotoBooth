import os

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

    def __init__(self):
        # self.twitter = TwitterClass.TwitterObject(token=self.token, token_secret=self.token_secret,
        #                                           consumer_key=self.consumer_key, consumer_secret=self.consumer_secret)
        # self.camera = CameraClass.CameraObject()
        # self.dropbox = DropboxClass.DropboxObject(self.dropbox_token)
        self.twitter = TwitterClass.TwitterObject(token=self.token,
                                                  token_secret=self.token_secret,
                                                  consumer_key=self.consumer_key,
                                                  consumer_secret=self.consumer_secret)
        self.camera = CameraClass.CameraObject()
        self.dropbox = DropboxClass.DropboxObject(self.dropbox_token)
        self.dropbox_folder = "Wedding"    # The folder the file will be stored in

        exists = os.path.isfile('config.cfg')
        if exists:
            print("file does exist")
            f = open('config.cfg', 'r')
            self.picture_number = int(f.readline())
            f.close()
        else:
            print('file does not exist')
            f = open('config.cfg', 'x')
            self.picture_number = 0
            f.write(str(self.picture_number))
            f.close()

    def take_picture(self):
        print("main use case has been triggered")
        self.picture_number += 1
        image_path = self.camera.take_picture(self.picture_number)

        f = open('config.cfg', 'w')
        f.write(str(self.picture_number))
        f.close()
        # Send to image manipulation class

        self.dropbox.upload_picture(image_path, self.dropbox_folder, self.picture_number)
        self.twitter.tweet_picture(image_path, "Picture Number " + str(self.picture_number) + ". #KatieChris2019")
