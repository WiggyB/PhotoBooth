

from PIL import Image
from PIL import ImageFilter
import os
for filename in os.listdir("."): # parse through file list in the current directory
     if filename[-3:] == "jpg":
          img = Image.open(filename)
          img = img.convert("RGBA")
          pixdata = img.load()
          for y in range(img.size[1]):
               for x in range(img.size[0]):
                    r, g, b, a = img.getpixel((x, y))
                    if (r < 64 and r > 48) and (g < 158 and g > 148) and (b < 116 and b > 109):
                         pixdata[x, y] = (255, 255, 255, 0)
                    #Remove anti-aliasing outline of body.
                    if r == 0 and g == 0 and b == 0:
                         pixdata[x, y] = (255, 255, 255, 0)
          #     img2 = img.filter(ImageFilter.GaussianBlur(radius=1))
          img.save(filename + "output", "JPEG")
