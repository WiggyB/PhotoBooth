from PIL import Image
from PIL import ImageFilter
import sys
import math

path = 'image9.png'

img = Image.open(path)

def image_process(image):
    number = 0
    #for filename in os.listdir("."): # parse through file list in the current directory
        #if filename[-3:] == "jpg":
            #img = Image.open(filename)
    img = image.convert("RGBA")
    pixdata = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = img.getpixel((x, y))
            if (r < 150 and r > 35) and (g < 216 and g > 91) and (b < 194 and b > 52):
                number += 1
                pixdata[x, y] = (255, 255, 255, 0)
                #Remove anti-aliasing outline of body.
                if r == 0 and g == 0 and b == 0:
                    pixdata[x, y] = (255, 255, 255, 0)
      #     img2 = img.filter(ImageFilter.GaussianBlur(radius=1))
    img.save(path + "output.png", "PNG")
    print(number)

image_process(img)

