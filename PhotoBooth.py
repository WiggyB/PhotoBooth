import CameraClass
import TwitterClass
import DropboxClass


class PhotoBooth:

    # Dropbox Tokens
    dropbox_token = "LXdgcDzVpX4AAAAAAAADw175Brf7pYw6KLYUkXkyMhJnQzXiQ4uXW5ngtskcF-Wj"

    # Twitter Tokens
    token = "1097906118603558912-8qi7HRS0dBIOPg5igxxlcL2Z6P27IY"
    token_secret = "6qFafsqUFPwUKtljd5WYGvt1xTtfUMYJH5UYuLzCj7inF"
    consumer_key = "wQy0diWcyl1G4GP4eF1arBPtS"
    consumer_secret = "B3JsT7UuB57ncKhZD174iR6k3kQ8lhKa6xj51h9i9l0mfO7S8F"

    def __init__(self):
        self.twitter = TwitterClass.TwitterObject(token=self.token, token_secret=self.token_secret,
                                            consumer_key=self.consumer_key, consumer_secret=self.consumer_secret)
        self.camera = CameraClass.CameraObject()
        self.dropbox = DropboxClass.DropboxObject(self.dropbox_token)

    def take_picture(self, number):
        self.camera.take_picture(number)
