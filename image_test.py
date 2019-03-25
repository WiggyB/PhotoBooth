#!/usr/bin/python

from PIL import Image
import sys
import math

# if len(sys.argv) < 3:
#     sys.exit('usage: gs.py <input> <output>')
#
# input_filename = sys.argv[1]
# output_filename = sys.argv[2]


#input_img = Image.open("image4.jpg")
input_img = Image.open("image4.jpg").convert("RGBA")
output_img = Image.new("RGBA", input_img.size)
input_image_size = input_img.size


background_img = Image.open("space.jpg").convert("RGBA")
cropped_background = background_img.crop((0, 0, input_image_size[0], input_image_size[1]))

for y in range(input_img.size[1]):
    for x in range(input_img.size[0]):
        p = input_img.getpixel((x, y))
        d = math.sqrt(math.pow(p[0], 2) + math.pow((p[1] - 255), 2) + math.pow(p[2], 2))

        if d > 128:
            d = 255
        0, 0, input_image_size[0], input_image_size[1]
        output_img.putpixel((x, y), (p[0], min(p[2], p[1]), p[2], int(d)))

output_img.save("output.png", "PNG")
#cropped_background.paste(output_img, (0, 0, input_image_size[0], input_image_size[1]))
#cropped_background.show()

print(output_img.getbands())
print(cropped_background.getbands())
finished_image = Image.blend(output_img, cropped_background, 1.0)
finished_image.show()
