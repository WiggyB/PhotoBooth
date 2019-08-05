import dropbox
from dropbox.files import WriteMode
import io


# A wrapper around the dropbox module
class DropboxObject:

    def __init__(self, token):
        # Create an instance of a Dropbox class, which can make requests to the API.
        self.dbx = dropbox.Dropbox(token)

    def upload_picture(self, image, path, image_number):
        try:
            img_byte = io.BytesIO()
            image.save(img_byte, format='PNG')
            img_byte = img_byte.getvalue()
            # Path is name of folder e.g Wedding
            self.dbx.files_upload(img_byte, '/' + path + '/image_' + str(image_number) + '.png',
                                  mode=dropbox.files.WriteMode.add)
        except:
            print("A DROPBOX EXECPTION HAS OCCURED")
            image.save('image_' + str(image_number) + '.png', "png")


