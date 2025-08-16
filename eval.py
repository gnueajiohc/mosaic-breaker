from src.utils import load_img, ssim

original_img = load_img("./data/tiger_128.png")
mosaic_img1 = load_img("./data/mosaic_tiger_100.png")
mosaic_img2 = load_img("./data/mosaic_tiger_200.png")
mosaic_img3 = load_img("./data/mosaic_tiger_300.png")
resolved_img = load_img("./result/resolved_tiger.png")

print("Mosaic 1 SSIM:", ssim(original_img, mosaic_img1))
print("Mosaic 2 SSIM:", ssim(original_img, mosaic_img2))
print("Mosaic 3 SSIM:", ssim(original_img, mosaic_img3))
print("Resolved SSIM:", ssim(original_img, resolved_img))
