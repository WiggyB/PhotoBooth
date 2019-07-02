from twitter import *


# A wrapper around the twitter module
class TwitterObject:

    def __init__(self, token, token_secret, consumer_key, consumer_secret):

        # This object will create tweets
        self.t_tweet = Twitter(
            auth=OAuth(token, token_secret, consumer_key, consumer_secret))

        # This object will upload images
        self.t_upload = Twitter(domain='upload.twitter.com',
                                auth=OAuth(token, token_secret, consumer_key, consumer_secret))

    # image is a string path to location of image file
    def tweet_picture(self, image, text):
        with open(image, "rb") as image_file:
            image_data = image_file.read()
        id_img = self.t_upload.media.upload(media=image_data)["media_id_string"]

        self.t_tweet.statuses.update(status=text, media_ids=id_img)
