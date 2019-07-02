from PIL import Image
import math


# Looks at each pixel to determine if it is part of the background or not. If it is it replaces it with the
#  corresponding pixel in the background image
def merge(path, background, image_size, progress_bar):
    input_img = Image.open(path)
    output_img = Image.new("RGB", image_size)

    for y in range(input_img.size[1]):
        # Update progress bar
        progress_bar['value'] = y
        for x in range(input_img.size[0]):
            p = input_img.getpixel((x, y))
            d = math.sqrt(math.pow(p[0] - 10, 2) + math.pow((p[1] - 255), 2) + math.pow(p[2] - 10, 2))
            if d < 185:
                background_pixel = background.getpixel((x, y))
                output_img.putpixel((x, y), (background_pixel[0], background_pixel[1], background_pixel[2]))
            else:
                output_img.putpixel((x, y), (p[0], p[1], p[2]))
    output_img.save(path[:-4] + '_output.jpg', "JPEG")
    return path[:-4] + '_output.jpg'
