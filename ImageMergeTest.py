from PIL import Image
import math
import time

pth = "images/test_image.png"
bg = Image.open("images/BG1.png")
img_size = (2592, 1944)


# Looks at each pixel to determine if it is part of the background or not. If it is it replaces it with the
#  corresponding pixel in the background image
def merge(path, background, image_size):
    input_img = Image.open(path)

    # for counting loops
    number = 0

    for y in range(input_img.size[1]):
        print(y)
        # Update progress bar
        # progress_bar['value'] = y
        for x in range(input_img.size[0]):
            number += 1
            p = input_img.getpixel((x, y))
            d = math.sqrt(math.pow(p[0] - 10, 2) + math.pow((p[1] - 255), 2) + math.pow(p[2] - 10, 2))
            if d < 185:
                input_img.putpixel((x, y), background.getpixel((x, y)))
    print(number)
    print(time.time() - start)
    input_img.save('NOMP_output.png', "PNG")
    return


start = time.time()
merge(pth, bg, img_size)
