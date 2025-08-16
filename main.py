from src.demosaic import MosaicFinder, MosaicInfo, MosaicRegistry, MosaicResolver
from src.mosaic import Mosaicer
from src.utils import load_img, save_img

KERNEL_SIZE = 2

def print_matrix(matrix):
    for row in matrix:
        print(row)

def make_mosaiced_imgs(img):
    count = 1
    for y in range(7, 10):
        for x in range(7, 10):
            mosaiced_img = mosaicer.apply(img, start_y=y, start_x=x, mosaic_size=7)
            save_img(mosaiced_img, f"./data/mosaic_{count}.png")
            count += 1

def register_mosaic_info():
    registry = MosaicRegistry()
    finder = MosaicFinder(mosaic_kernel_size=KERNEL_SIZE)
    for i in range(1, 10):
        img = load_img(f"./data/mosaic_{i}.png")
        mosaic_top, mosaic_left, mosaic_len = finder.find_mosaic(img)
        info = MosaicInfo(img, left=mosaic_left, top=mosaic_top, size=mosaic_len, kernel_size=KERNEL_SIZE)
        registry.add_mosaic(info)
    return registry

img = load_img("./data/image.png")
mosaicer = Mosaicer(mosaic_kernel_size=KERNEL_SIZE)
make_mosaiced_imgs(img)
registry = register_mosaic_info()
resolver = MosaicResolver()
resolved_img = resolver.resolve(registry)
save_img(resolved_img, f"./data/resolved_image.png")
