import cv2 as cv
import numpy as np

hdr_image = cv.imread("img/272_HDR2.hdr", cv.IMREAD_ANYDEPTH)
small_to_large_image_size_ratio = 0.2
tone_img = cv.resize(hdr_image, # original image
                       (0,0), # set fx and fy, not the final size
                       fx=small_to_large_image_size_ratio, 
                       fy=small_to_large_image_size_ratio, 
                       interpolation=cv.INTER_NEAREST)



Vmax = 0
for group in tone_img:
    for pix in group:
        
        Vin = 1./61 * (pix[0] * 20 + pix[1] * 40 + pix[2])
        if Vin >= Vmax:
            Vmax = Vin

tone_img = tone_img / (Vmax+1)

result_8bit = np.clip(tone_img*255, 0, 255).astype('uint8')
cv.imwrite("img/TMO_norm.jpg", result_8bit)
