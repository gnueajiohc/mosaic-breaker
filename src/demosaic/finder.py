from .types import MosaicInfo


class MosaicFinder:
    def find_mosaic(self, img):
        self.img = img
        self._build_mosaic_mask()
        self._find_largest_mosaic_square()
        self._find_mosaic_kernel_size()

        return MosaicInfo(
            mosaiced_img=self.img,
            left=self.mosaic_left,
            top=self.mosaic_top,
            size=self.mosaic_size,
            kernel_size=self.mosaic_kernel_size
        )
    
    def _build_mosaic_mask(self):
        width, height = len(self.img[0]), len(self.img)
        self.mosaic_mask = [[False] * width for _ in range(height)]
        
        for y in range(height - 1):
            for x in range(width - 1):
                self._mark_block_if_uniform(y, x)
                
    def _mark_block_if_uniform(self, start_y, start_x):
        expected = self.img[start_y][start_x]

        for y in range(start_y, start_y + 2):
            for x in range(start_x, start_x + 2):
                if self.img[y][x] != expected:
                    return
        
        for y in range(start_y, start_y + 2):
            for x in range(start_x, start_x + 2):
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
        
        self.mosaic_top = largest_square_mosaic_bottom_right[0] - len_largest_square_mosaic + 1
        self.mosaic_left = largest_square_mosaic_bottom_right[1] - len_largest_square_mosaic + 1
        self.mosaic_size = len_largest_square_mosaic

    def _find_mosaic_kernel_size(self):
        largest_kernel_size = 2
        for kernel_size in range(3, self.mosaic_size+1):
            if self.mosaic_size % kernel_size != 0:
                continue
            for y in range(self.mosaic_top, self.mosaic_top + self.mosaic_size, kernel_size):
                for x in range(self.mosaic_left, self.mosaic_left + self.mosaic_size, kernel_size):
                    if self._check_kernel_size(y, x, kernel_size):
                        largest_kernel_size = kernel_size
            
        self.mosaic_kernel_size = largest_kernel_size
    
    def _check_kernel_size(self, start_y, start_x, kernel_size):
        expected = self.img[start_y][start_x]

        for y in range(start_y, start_y + kernel_size):
            for x in range(start_x, start_x + kernel_size):
                if self.img[y][x] != expected:
                    return False
        return True
    