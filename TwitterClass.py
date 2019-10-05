from twitter import *
import io
import os
from PIL import Image


# A wrapper around the twitter module
class TwitterObject:

    def __init__(self, token, token_secret, consumer_key, consumer_secret):

        # This object will create tweets
        self.t_tweet = Twitter(
            auth=OAuth(token, token_secret, consumer_key, consumer_secret))

        # This object will upload images
        self.t_upload = Twitter(domain='upload.twitter.com',
                                auth=OAuth(token, token_secret, consumer_key, consumer_secret))
        exists = os.path.isfile('twitter_uploads.cfg')
        if not exists:
            # File does not exist create it
            f = open('twitter_uploads.cfg', 'x')
            f.close()

    # image is a string path to location of image file
    def tweet_picture(self, image, text, image_number):
        try:
            img_byte = io.BytesIO()
            image.save(img_byte, format='PNG')
            img_byte = img_byte.getvalue()
            id_img = self.t_upload.media.upload(media=img_byte)["media_id_string"]
            self.t_tweet.statuses.update(status=text, media_ids=id_img)

            # if dropbox_uploads is not empty, try uploading them
            if os.stat("twitter_uploads.cfg").st_size != 0:
                self.try_uploads()

        except Exception as e:
            print(e)
            image.save('twitter_image_' + str(image_number) + '.png', "png")
            f = open('twitter_uploads.cfg', 'a')
            f.write('twitter_image_' + str(image_number) + '.png\n')
            f.write(text + '\n')
            f.close()

    def try_uploads(self):
        f = open('twitter_uploads.cfg', 'r')
        lines = f.readlines()
        print(lines)
        f.close()
        line_number = 0
        print("amount of times in loop twitter: " + str(int(len(lines) / 2)))
        for image in range(int(len(lines) / 2)):
            # Read two lines from the uploads file
            file_name = lines[line_number].rstrip()
            line_number += 1
            text = lines[line_number].rstrip()
            try:
                # Open image and convert to byte array
                image = Image.open(file_name)
                img_byte = io.BytesIO()
                image.save(img_byte, format='PNG')
                img_byte = img_byte.getvalue()
                id_img = self.t_upload.media.upload(media=img_byte)["media_id_string"]
                self.t_tweet.statuses.update(status=text, media_ids=id_img)
                print("twitter")
                print(lines)
                del lines[0]
                del lines[0]
                print("twitter")
                print(lines)
                line_number = 0
                os.remove(file_name)
                print("successful upload in try uploads")
            except Exception as e:
                print("Error in try uploads")
                print(e)
        if lines:
            with open('twitter_uploads.cfg', 'a') as f:
                for line in lines:
                    print("writing to cfg twitter cfg file this")
                    print(lines)
                    f.write(line + "\n")
        else:
            with open('twitter_uploads.cfg', 'w') as f:
                f.write("")
