from PIL import Image
import math


def merge(path, background, image_size):

    input_img = Image.open(path)
    output_img = Image.new("RGBA", image_size) #input_img.size)

    for y in range(input_img.size[1]):
        for x in range(input_img.size[0]):
            p = input_img.getpixel((x, y))
            d = math.sqrt(math.pow(p[0] - 10, 2) + math.pow((p[1] - 255), 2) + math.pow(p[2] - 10, 2))
            if d < 185:
                #background_pixel = app.core.backgrounds_full[app.background_choice].getpixel((x,y))
                background_pixel = background.getpixel((x, y))
                output_img.putpixel((x, y), (background_pixel[0], background_pixel[1], background_pixel[2], 255))
            else:
                output_img.putpixel((x, y), (p[0], p[1], p[2], 255))
    output_img.save(path[:-4] + '_output.png', "PNG")
    return path[:-4] + '_output.png'




