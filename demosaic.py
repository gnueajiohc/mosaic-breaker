from src.demosaic import MosaicFinder, MosaicRegistry, MosaicResolver
from src.utils import load_img, save_img

def register_mosaic_info():
    registry = MosaicRegistry()
    finder = MosaicFinder()
    for i in range(1, 301):
        img = load_img(f"./data/mosaic_tiger_{i}.png")
        info = finder.find_mosaic(img)
        print(i, info.kernel_size)
        registry.add_mosaic(info)
    return registry

registry = register_mosaic_info()
resolver = MosaicResolver()
resolved_img = resolver.resolve(registry)
save_img(resolver.intermediate_img, f"./result/intermediate_tiger.png")
save_img(resolved_img, f"./result/resolved_tiger.png")
