class MosaicFinder:
    def __init__(self, mosaic_kernel_size):
        self.mosaic_kernel_size = mosaic_kernel_size
    
    def find_mosaic(self, img):
        self.img = img
        self._build_mosaic_mask()
        mosaic_bottom_right, mosaic_len = self._find_largest_mosaic_square()
        mosaic_bottom, mosaic_right = mosaic_bottom_right
        mosaic_top = mosaic_bottom - mosaic_len + 1
        mosaic_left = mosaic_right - mosaic_len + 1
        return mosaic_top, mosaic_left, mosaic_len
    
    def _build_mosaic_mask(self):
        width, height = len(self.img[0]), len(self.img)
        self.mosaic_mask = [[False] * width for _ in range(height)]
        
        for y in range(height - self.mosaic_kernel_size + 1):
            for x in range(width - self.mosaic_kernel_size + 1):
                self._mark_kernel_if_uniform(y, x)
                
    def _mark_kernel_if_uniform(self, start_y, start_x):
        expected = self.img[start_y][start_x]

        for y in range(start_y, start_y + self.mosaic_kernel_size):
            for x in range(start_x, start_x + self.mosaic_kernel_size):
                if self.img[y][x] != expected:
                    return
        
        for y in range(start_y, start_y + self.mosaic_kernel_size):
            for x in range(start_x, start_x + self.mosaic_kernel_size):
                self.mosaic_mask[y][x] = True
    
    def _find_largest_mosaic_square(self):
        width, height = len(self.mosaic_mask[0]), len(self.mosaic_mask)
        len_largest_square_mosaic = 0
        largest_square_mosaic_bottom_right = None
        dp = [[0] * width for _ in range(height)]
        for y in range(height):
            for x in range(width):
                if self.mosaic_mask[y][x]:
                    if y == 0 or x == 0:
                        dp[y][x] = 1
                    else:
                        dp[y][x] = 1 + min(dp[y-1][x], dp[y][x-1], dp[y-1][x-1])
                        
                    if dp[y][x] > len_largest_square_mosaic:
                        len_largest_square_mosaic = dp[y][x]
                        largest_square_mosaic_bottom_right = (y, x)
                        
        return largest_square_mosaic_bottom_right, len_largest_square_mosaic
            