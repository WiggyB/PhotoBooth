# import CameraClass
# import TwitterClass
# import DropboxClass
import CameraClassTest
import DropboxClassTest
import TwitterClassTest


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
        self.twitter = TwitterClassTest.TwitterObject(token=self.token,
                                                      token_secret=self.token_secret,
                                                      consumer_key=self.consumer_key,
                                                      consumer_secret=self.consumer_secret)
        self.camera = CameraClassTest.CameraObject()
        self.dropbox = DropboxClassTest.DropboxObject(self.dropbox_token)
        self.image_number = 0
        self.dropbox_folder = "Wedding"    # The folder the file will be stored in
        self.picture_number = 0             # add a config file to track numbers

    def main_use_case(self):
        print("main use case has been triggered")
        image_path = self.camera.take_picture(self.picture_number)

        # Send to image manipulation class

        self.dropbox.upload_picture(image_path, self.dropbox_folder, self.image_number)
        self.twitter.tweet_picture(image_path, "This is some test text #TestyMcTestface")
