import dropbox
from dropbox.files import WriteMode
import io
import os
from PIL import Image


# A wrapper around the dropbox module
class DropboxObject:

    def __init__(self, token):
        # Create an instance of a Dropbox class, which can make requests to the API.
        self.dbx = dropbox.Dropbox(token)

        exists = os.path.isfile('dropbox_uploads.cfg')
        if not exists:
            # File does not exist create it
            f = open('dropbox_uploads.cfg', 'x')
            f.close()

    def upload_picture(self, image, path, image_number):
        # Attempt to upload the file
        try:
            img_byte = io.BytesIO()
            image.save(img_byte, format='PNG')
            img_byte = img_byte.getvalue()
            # Path is name of folder e.g Wedding
            self.dbx.files_upload(img_byte, '/' + path + '/image_' + str(image_number) + '.png',
                                  mode=dropbox.files.WriteMode.add)
            # if dropbox_uploads is not empty, try uploading them
            if os.stat("dropbox_uploads.cfg").st_size != 0:
                self.try_uploads()

        # Records any failed uploads in cfg file
        except Exception as e:
            print(e)
            image.save('dropbox_image_' + str(image_number) + '.png', "png")
            f = open('dropbox_uploads.cfg', 'a')
            f.write('dropbox_image_' + str(image_number) + '.png\n')
            f.write('/' + path + '/dropbox_image_' + str(image_number) + '.png\n')
            f.close()

    # Attempts to upload any stored, failed uploads
    def try_uploads(self):
        f = open('dropbox_uploads.cfg', 'r')
        lines = f.readlines()
        print(lines)
        f.close()
        line_number = 0
        print("amount of times in loop: " + str(int(len(lines) / 2)))
        for image in range(int(len(lines)/2)):
            # Read two lines from the uploads file
            file_name = lines[line_number].rstrip()
            line_number += 1
            path_arg = lines[line_number].rstrip()
            try:
                # Open image and convert to byte array
                image = Image.open(file_name)
                img_byte = io.BytesIO()
                image.save(img_byte, format='PNG')
                img_byte = img_byte.getvalue()
                self.dbx.files_upload(img_byte, path_arg, mode=dropbox.files.WriteMode.add)
                print("dropbox")
                print(lines)
                del lines[0]
                del lines[0]
                print("dropbox")
                print(lines)
                line_number = 0
                os.remove(file_name)
                print("successful upload in try uploads")
            except Exception as e:
                print("Error in try uploads")
                print(e)
        if lines:
            with open('dropbox_uploads.cfg', 'a') as f:
                print("writing to cfg dropbox cfg file this")
                print(lines)
                for line in lines:
                    f.write(line + "\n")
        else:
            with open('dropbox_uploads.cfg', 'w') as f:
                f.write("")
