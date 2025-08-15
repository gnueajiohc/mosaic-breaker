from copy import deepcopy


class Mosaicer:
    def __init__(self, mosaic_kernel_size):
        self.mosaic_kernel_size = mosaic_kernel_size
        
    def apply(self, img, start_y, start_x, mosaic_size):
        self.mosaiced_img = deepcopy(img)
        width, height = len(img[0]), len(img)
        
        for y in range(start_y, start_y + mosaic_size, self.mosaic_kernel_size):
            if y + self.mosaic_kernel_size > height:
                break
            for x in range(start_x, start_x + mosaic_size, self.mosaic_kernel_size):
                if x + self.mosaic_kernel_size > width:
                    break
                self._apply_block_avg(img, y, x)
        return self.mosaiced_img
        
    def _apply_block_avg(self, img, start_y, start_x):
        sum_r = sum_g = sum_b = 0
        for y in range(start_y, start_y + self.mosaic_kernel_size):
            for x in range(start_x, start_x + self.mosaic_kernel_size):
                r, g, b = img[y][x]
                sum_r += r
                sum_g += g
                sum_b += b
        
        area = self.mosaic_kernel_size * self.mosaic_kernel_size
        avg_r = int(round(sum_r / area))
        avg_g = int(round(sum_g / area))
        avg_b = int(round(sum_b / area))
        
        for y in range(start_y, start_y + self.mosaic_kernel_size):
            for x in range(start_x, start_x + self.mosaic_kernel_size):
                self.mosaiced_img[y][x] = (avg_r, avg_g, avg_b)
                