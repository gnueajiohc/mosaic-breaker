from dataclasses import dataclass, field


@dataclass
class MosaicInfo:
    mosaiced_img: list = field(default_factory=list)
    left: int = 0
    top: int = 0
    size: int = 0
    kernel_size: int = 2


class MosaicRegistry:
    def __init__(self):
        self._registry = []
    
    def add_mosaic(self, mosaic_info):
        self._registry.append(mosaic_info)
    
    def get_all(self):
        return list(self._registry)

    def __len__(self):
        return len(self._registry)

    def __iter__(self):
        return iter(self._registry)
    