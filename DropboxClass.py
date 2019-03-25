import dropbox


class DropboxObject:

    def __init__(self, token):
        # Create an instance of a Dropbox class, which can make requests to the API.
        self.dbx = dropbox.Dropbox(token)

    def upload_picture(self, filename, path, image_number):

        # Filename example girl.jpg
        # Path is name of folder e.g Wedding
        file = open(filename, 'rb')
        self.dbx.files_upload(file.read(), '/' + path + '/image_' + str(image_number) + '.jpg')
