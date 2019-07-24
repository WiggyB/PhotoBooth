
def parallel_func(params):

    x = params[1]
    y = params[0]
    p = input_img.getpixel((x, y))
    d = math.sqrt(math.pow(p[0] - 10, 2) + math.pow((p[1] - 255), 2) + math.pow(p[2] - 10, 2))
    if d < 185:
        lock.acquire()
        background_pixel = background.getpixel((x, y))
        output_img.putpixel((x, y), (background_pixel[0], background_pixel[1], background_pixel[2], 255))
        lock.release()
    else:
        lock.acquire()
        output_img.putpixel((x, y), (p[0], p[1], p[2], 255))
        lock.release()