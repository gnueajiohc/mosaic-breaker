from src.demosaic import MosaicFinder, MosaicInfo, MosaicRegistry, MosaicResolver
from src.utils import load_img, save_img

def register_mosaic_info():
    registry = MosaicRegistry()
    for kernel_size in range(2, 3):
        finder = MosaicFinder(mosaic_kernel_size=kernel_size)
        for i in range(100 * (kernel_size-2) + 1, 100 * (kernel_size-1) + 1):
            img = load_img(f"./data/mosaic_tiger_{i}.png")
            mosaic_top, mosaic_left, mosaic_len = finder.find_mosaic(img)
            info = MosaicInfo(img, left=mosaic_left, top=mosaic_top, size=mosaic_len, kernel_size=kernel_size)
            registry.add_mosaic(info)
    return registry

registry = register_mosaic_info()
resolver = MosaicResolver()
resolved_img = resolver.resolve(registry)
save_img(resolver.intermediate_img, f"./result/intermediate_tiger.png")
save_img(resolved_img, f"./result/resolved_tiger.png")
