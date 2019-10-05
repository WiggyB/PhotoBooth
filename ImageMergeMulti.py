from PIL import Image
import multiprocessing
import math
import time


def chroma_key(chunks_list):

    for y in range(chunks_list[0].size[1]):
        for x in range(chunks_list[0].size[0]):
            p = chunks_list[0].getpixel((x, y))
            d = math.sqrt(math.pow(p[0] - 10, 2) + math.pow((p[1] - 255), 2) + math.pow(p[2] - 10, 2))
            if d < 200:
                background_pixel = chunks_list[1].getpixel((x, y))
                chunks_list[0].putpixel((x, y), (background_pixel[0], background_pixel[1], background_pixel[2]))
    return chunks_list[0]


def merge(foreground, background):

    start = time.time()
    number_of_chunks = multiprocessing.cpu_count() * 8
    # Load images
    image_size = foreground.size
    output_img = Image.new("RGBA", image_size)
    chunk_size = int(image_size[0] / number_of_chunks)
    image_chunks = []

    # Create image chunks for Multiprocessing
    x_value = 0
    for c in range(number_of_chunks):
        fore_chunk = foreground.crop((x_value, 0, x_value + chunk_size, image_size[1]))
        back_chunk = background.crop((x_value, 0, x_value + chunk_size, image_size[1]))
        image_chunks.append([fore_chunk, back_chunk])
        x_value += chunk_size

    # Generate process pool
    pool = multiprocessing.Pool()
    # Distribute the parameter sets evenly across the cores
    result = pool.map(chroma_key, image_chunks)
    pool.close()
    pool.join()

    # Reassemble chunks
    for c in range(number_of_chunks):
        output_img.paste(result[c], (chunk_size*c, 0, chunk_size*(c + 1), image_size[1]))
    return output_img
