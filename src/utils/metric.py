import numpy as np
from scipy.ndimage import gaussian_filter


def rgb_to_y(img):
    return 0.299 * img[..., 0] + 0.587 * img[..., 1] + 0.114 * img[..., 2]


def ssim(img1, img2, window_size=7, K1=0.01, K2=0.03):
    img1 = np.array(img1)
    img2 = np.array(img2)
    
    y1 = rgb_to_y(img1)
    y2 = rgb_to_y(img2)
    
    L = 255
    C1 = (K1 * L) ** 2
    C2 = (K2 * L) ** 2
    
    sigma = window_size / 4.0
    truncate = ((window_size - 1) / 2.0) / sigma
    
    mu1 = gaussian_filter(y1, sigma, truncate=truncate, mode="reflect")
    mu2 = gaussian_filter(y2, sigma, truncate=truncate, mode="reflect")
    
    mu1_square = mu1 * mu1
    mu2_square = mu2 * mu2
    mu1_mu2 = mu1 * mu2
    
    y1_square = y1 * y1
    y2_square = y2 * y2
    y1_y2 = y1 * y2
    
    sigma1_square = gaussian_filter(y1_square, sigma, truncate=truncate, mode="reflect") - mu1_square
    sigma2_square = gaussian_filter(y2_square, sigma, truncate=truncate, mode="reflect") - mu2_square
    sigma12 = gaussian_filter(y1_y2, sigma, truncate=truncate, mode="reflect") - mu1_mu2
    
    numerator = (2 * mu1_mu2 + C1) * (2 * sigma12 + C2)
    denominator = (mu1_square + mu2_square + C1) * (sigma1_square + sigma2_square + C2)
    ssim_map = numerator / denominator
    
    return float(ssim_map.mean())
    