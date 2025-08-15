from src.demosaic import MosaicFinder, MosaicInfo, MosaicRegistry, MosaicResolver
from src.mosaic import Mosaicer
from src.utils import load_img, save_img

def print_matrix(matrix):
    for row in matrix:
        print(row)

def make_mosaiced_imgs(img):
    count = 1
    for y in range(5, 9):
        for x in range(5, 9):
            mosaiced_img = mosaicer.apply(img, start_y=y, start_x=x, mosaic_size=8)
            save_img(mosaiced_img, f"./data/mosaiced_img_{count}.png")
            count += 1

def register_mosaic_info():
    registry = MosaicRegistry()
    finder = MosaicFinder(mosaic_kernel_size=2)
    for i in range(1, 17):
        img = load_img(f"./data/mosaiced_img_{i}.png")
        mosaic_top, mosaic_left, mosaic_len = finder.find_mosaic(img)
        print(mosaic_top, mosaic_left, mosaic_len)
        info = MosaicInfo(img, left=mosaic_left, top=mosaic_top, size=mosaic_len, kernel_size=2)
        registry.add_mosaic(info)
    return registry

img = load_img("./data/image.png")
mosaicer = Mosaicer(mosaic_kernel_size=2)
make_mosaiced_imgs(img)
registry = register_mosaic_info()
resolver = MosaicResolver()
resolver.resolve(registry)
print_matrix(resolver.system_A)
print(resolver.system_b_B)
