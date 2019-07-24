from PIL import Image
import multiprocessing
import math
import time


def chroma_key(foreground_chunk, background_chunk ):

    for y in range(foreground_chunk.size[1]):
        for x in range(foreground_chunk.size[0]):
            p = foreground_chunk.getpixel((x, y))
            d = math.sqrt(math.pow(p[0] - 10, 2) + math.pow((p[1] - 255), 2) + math.pow(p[2] - 10, 2))
            if d < 185:
                background_pixel = background_chunk.getpixel((x, y))
                foreground_chunk.putpixel((x, y), (background_pixel[0], background_pixel[1], background_pixel[2]))
    return foreground_chunk


def merge(path, background):
    # Load images
    foreground = Image.open("images/test_image.png")
    image_size = foreground.size
    output_img = Image.new("RGBA", image_size)
    chunk_size = int(image_size[0] / multiprocessing.cpu_count())
    image_chunks = []

    # Create image chunks for Multiprocessing
    x_value = 0
    for c in range(multiprocessing.cpu_count()):
        fore_chunk = foreground.crop((x_value, 0, x_value + chunk_size, image_size[1]))
        back_chunk = background.crop((x_value, 0, x_value + chunk_size, image_size[1]))
        image_chunks.append([fore_chunk, back_chunk])
        x_value += chunk_size

    # Generate process pool
    pool = multiprocessing.Pool()
    print("Pool created")

    # Distribute the parameter sets evenly across the cores
    print("Starting Work")
    start = time.time()
    result = pool.starmap(chroma_key, image_chunks)
    pool.close()
    pool.join()
    print("Work Finished")
    print(time.time() - start)

    # Reassemble chunks
    for c in range(multiprocessing.cpu_count()):
        output_img.paste(result[c], (chunk_size*c, 0, chunk_size*(c + 1), image_size[1]))

    output_img.save(path[:-4] + '_output.png', "PNG")
    return path[:-4] + '_output.jpg'

