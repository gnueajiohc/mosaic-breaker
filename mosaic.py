from src.mosaic import Mosaicer
from src.utils import load_img, save_img

count = 1

def make_mosaiced_imgs(img):
    for kernel_size in range(2, 5):
        make_mosaiced_imgs_with_kernel_size(img, kernel_size=kernel_size)

def make_mosaiced_imgs_with_kernel_size(img, kernel_size):
    global count
    mosaicer = Mosaicer(mosaic_kernel_size=kernel_size)
    width, height = len(img[0]), len(img)
    
    center_h = height // 2
    center_w = width // 2
    
    for y in range(center_h - 25, center_h - 15):
        for x in range(center_w - 10, center_w):
            mosaiced_img = mosaicer.apply(img, start_y=y, start_x=x, mosaic_size=30)
            save_img(mosaiced_img, f"./data/mosaic_tiger_{count}.png")
            count += 1

img = load_img("./data/tiger_128.png")
make_mosaiced_imgs(img)
