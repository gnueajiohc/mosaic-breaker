import numpy as np
from src.utils.math import solve_least_squares


class MosaicResolver:
    def resolve(self, mosaic_registry):
        self.registry = mosaic_registry
        self._build_system()
    
    def _build_system(self):
        self.system_A = []
        self.system_b_R = []
        self.system_b_G = []
        self.system_b_B = []
        self.system_index_to_pixel_index = []
        self.pixel_index_to_system_index = {}
        for info in self.registry:
            self._build_system_from_info(info)
        self._convert_system_index_to_matrix()
            
    def _build_system_from_info(self, info):
        img = info.mosaiced_img
        start_y = info.top
        start_x = info.left
        size = info.size
        step = info.kernel_size
        
        for y in range(start_y, start_y + size, step):
            for x in range(start_x, start_x + size, step):
                self._build_system_from_block(y, x, step, img[y][x])
                
    def _build_system_from_block(self, top_y, left_x, kernel_size, value):
        area = kernel_size * kernel_size
        system_indices = []
        for y in range(top_y, top_y + kernel_size):
            for x in range(left_x, left_x + kernel_size):
                if (y, x) not in self.pixel_index_to_system_index:
                    self.pixel_index_to_system_index[(y, x)] = len(self.system_index_to_pixel_index)
                    self.system_index_to_pixel_index.append((y, x))
                system_index = self.pixel_index_to_system_index[(y, x)]
                system_indices.append(system_index)
        self.system_A.append(system_indices)
        
        R, G, B = value
        self.system_b_R.append(R * area)
        self.system_b_G.append(G * area)
        self.system_b_B.append(B * area)
    
    def _convert_system_index_to_matrix(self):
        m = len(self.system_A)
        n = len(self.system_index_to_pixel_index)
        
        system_A = np.zeros((m, n))
        for i, system_indices in enumerate(self.system_A):
            for system_index in system_indices:
                system_A[i, system_index] = 1
        self.system_A = system_A
        