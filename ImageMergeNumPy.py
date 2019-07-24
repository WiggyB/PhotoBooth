#!/usr/bin/env python
import time
import matplotlib.pylab as plt
import math
import numpy

# read in img
input_img = plt.imread('images/image6.jpg')

# output_img = Image.new("RGBA", image_size)

image_size = input_img.shape[0:2]
print(image_size)
bg = plt.imread("images/1.jpg")
the_path = "stuff"


# Looks at each pixel to determine if it is part of the background or not. If it is it replaces it with the
# corresponding pixel in the background image
def merge(path, background, input_image):
    # Create empty array the same size
    output_img = numpy.empty(input_image.shape)
    for y in range(image_size[0]):
        print("y: " + str(y))
        # Update progress bar
        # progress_bar['value'] = y
        for x in range(image_size[1]):
            pixel = input_image[y, x]
            d = math.sqrt(math.pow(pixel[0] - 10, 2) + math.pow((pixel[1] - 255), 2) + math.pow(pixel[2] - 10, 2))
            if d < 185:
                background_pixel = background[y, x]
                output_img[y, x] = (background_pixel[0], background_pixel[1], background_pixel[2])
            else:
                output_img[y, x] = (pixel[0], pixel[1], pixel[2])

    print(time.time() - start)
    fname = 'outputNumpySingle.png'
    output_img /= 255.
    plt.imsave(fname, output_img)
    return fname


start = time.time()
merge(the_path, bg, input_img)

