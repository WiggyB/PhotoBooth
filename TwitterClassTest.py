class TwitterObject:

    def __init__(self, token, token_secret, consumer_key, consumer_secret):

        self.token = token
        self.token_secret = token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    # image is a string path to location of image file
    def tweet_picture(self, image, text):
        return
