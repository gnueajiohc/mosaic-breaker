import numpy as np
from src.utils import solve_least_squares_with_knowns


class MosaicResolver:
    def resolve(self, mosaic_registry):
        self.registry = mosaic_registry
        self._build_system()
        self._solve_system()
        self._fill_resolved_pixels()
        return self.resolved_img
    
    def _build_system(self):
        self._initialize_resolved_img()
        self._find_known_pixels()
        self._build_system_from_registry()
        self._convert_system_index_to_matrix()
    
    def _initialize_resolved_img(self):
        info = self.registry.get_all()[0]
        img = info.mosaiced_img
        width, height = len(img[0]), len(img)
        self.resolved_img = np.zeros((height, width), dtype=tuple)
    
    def _find_known_pixels(self):
        self.known_mask = np.zeros_like(self.resolved_img, dtype=bool)
        for info in self.registry:
            self._find_known_pixels_from_info(info)
        self.intermediate_img = self.resolved_img.copy()
            
    def _find_known_pixels_from_info(self, info):
        img = info.mosaiced_img
        start_y = info.top
        start_x = info.left
        size = info.size
        
        width, height = len(img[0]), len(img)
        for y in range(height):
            for x in range(width):
                if start_y <= y < start_y + size and start_x <= x < start_x + size:
                    continue
                if self.known_mask[y][x]:
                    continue
                self.known_mask[y][x] = True
                self.resolved_img[y][x] = img[y][x]
    
    def _build_system_from_registry(self):
        self.system_A = []
        self.system_b_R = []
        self.system_b_G = []
        self.system_b_B = []
        self.system_index_to_pixel_index = []
        self.pixel_index_to_system_index = {}
        self.known_index = []
        self.known_index_set = set()
        self.known_values_R = []
        self.known_values_G = []
        self.known_values_B = []
        for info in self.registry:
            self._build_system_from_info(info)
            
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
                if self.known_mask[y][x] and system_index not in self.known_index_set:
                    self.known_index.append(system_index)
                    self.known_index_set.add(system_index)
                    self.known_values_R.append(self.resolved_img[y][x][0])
                    self.known_values_G.append(self.resolved_img[y][x][1])
                    self.known_values_B.append(self.resolved_img[y][x][2])
        
        R, G, B = value
        self.system_A.append(system_indices)
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
    
    def _solve_system(self):
        self.known_index = np.array(self.known_index)
        self.known_values_R = np.array(self.known_values_R)
        self.known_values_G = np.array(self.known_values_G)
        self.known_values_B = np.array(self.known_values_B)
        self.x_R, _ = solve_least_squares_with_knowns(self.system_A, self.system_b_R, self.known_index, self.known_values_R)
        self.x_G, _ = solve_least_squares_with_knowns(self.system_A, self.system_b_G, self.known_index, self.known_values_G)
        self.x_B, _ = solve_least_squares_with_knowns(self.system_A, self.system_b_B, self.known_index, self.known_values_B)
        
    def _fill_resolved_pixels(self):
        width, height = len(self.resolved_img[0]), len(self.resolved_img)
        
        for y in range(height):
            for x in range(width):
                if self.known_mask[y][x]:
                    continue
                system_index = self.pixel_index_to_system_index[(y, x)]
                R = int(round(self.x_R[system_index]))
                G = int(round(self.x_G[system_index]))
                B = int(round(self.x_B[system_index]))
                self.resolved_img[y][x] = (R, G, B)
        