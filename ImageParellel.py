from PIL import Image
import math
import multiprocessing
import itertools
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

input_img = Image.open('image8.png')
output_img = Image.new("RGBA", input_img.size)
nature_image = Image.open("nature.jpg")
background = nature_image.resize(input_img.size)
changed = 0
not_changed = 0
# def merge(path, background, image_size):

a = range(input_img.size[1])
b = range(input_img.size[0])
print("input a: " + str(input_img.size[1]))
print("input b: " + str(input_img.size[0]))

print("output a: " + str(output_img.size[1]))
print("output b: " + str(output_img.size[0]))

print("background: " + str(background.size[1]))
print("background: " + str(background.size[0]))

param_list = list(itertools.product(a, b))


def parallel_func(params):
    x = params[1] -1
    y = params
    input_img.show()
    p = input_img.getpixel((x, y))
    d = math.sqrt(math.pow(p[0] - 10, 2) + math.pow((p[1] - 255), 2) + math.pow(p[2] - 10, 2))
    if d < 185:
        #background_pixel = app.core.backgrounds_full[app.background_choice].getpixel((x,y))
        background_pixel = background.getpixel((x, y))
        output_img.putpixel((x, y), (background_pixel[0], background_pixel[1], background_pixel[2], 255))
    else:
        output_img.putpixel((x, y), (p[0], p[1], p[2], 255))


# Generate processes equal to the number of cores
pool = multiprocessing.Pool()

# Distribute the parameter sets evenly across the cores
res = pool.map(parallel_func, param_list)

output_img.save('test_output.png', "PNG")




