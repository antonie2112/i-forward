from PIL import Image
import collections

img = Image.open('public/images_hq/7101070.png')
# Count pixels with RGB near #F2F2F2
gray_pixels = 0
total_pixels = img.width * img.height
for p in img.getdata():
    if p[3] > 100: # Not transparent
        if 235 < p[0] < 250 and 235 < p[1] < 250 and 235 < p[2] < 250:
            gray_pixels += 1

print(f"Total non-transparent gray pixels: {gray_pixels} out of {total_pixels} ({gray_pixels/total_pixels*100:.2f}%)")
