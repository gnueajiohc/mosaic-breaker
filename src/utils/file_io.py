from PIL import Image

def load_img(img_path):
    img = Image.open(img_path).convert("RGB")
    width, height = img.size
    
    pixel_array = [
        [img.getpixel((x, y)) for x in range(width)] for y in range(height)
    ]
    return pixel_array


def save_img(pixel_array, img_path):
    width, height = len(pixel_array[0]), len(pixel_array)
    img = Image.new("RGB", (width, height))
    
    for y in range(height):
        for x in range(width):
            img.putpixel((x, y), pixel_array[y][x])
    
    img.save(img_path)
    