import cv2 as cv
import numpy as np


def CRF_merge_Debevec(prefix,count,extension):
    # Loading exposure images into a list
    img_fn = [prefix+str(i)+"."+extension for i in range(1,count+1)]

    img_list = [cv.imread(fn) for fn in img_fn]
    exposure_times = np.array([1./80, 1./25, 1./200], dtype=np.float32)

    # Merge exposures to HDR image
    merge_debevec = cv.createMergeDebevec()
    hdr_debevec = merge_debevec.process(img_list, times=exposure_times.copy())

    # Tonemap HDR image
    tonemap = cv.createTonemapMantiuk()
    res_debevec = tonemap.process(hdr_debevec.copy())

    # Convert datatype to 8-bit and save
    res_debevec_8bit = np.clip(res_debevec*255, 0, 255).astype('uint8')
    cv.imwrite("img/ldr_debevec.jpg", res_debevec_8bit)

def CRF_merge_Robertson(prefix,count,extension):
    # Loading exposure images into a list
    img_fn = [prefix+str(i)+"."+extension for i in range(1,count+1)]
    img_list = [cv.imread(fn) for fn in img_fn]
    exposure_times = np.array([1./80, 1./25, 1./200], dtype=np.float32)

    # Merge exposures to HDR image
    merge_Robertson = cv.createMergeRobertson()
    hdr_Robertson = merge_Robertson.process(img_list, times=exposure_times.copy())

    # Tonemap HDR image
    tonemap = cv.createTonemapMantiuk()
    res_Robertson = tonemap.process(hdr_Robertson.copy())

    # Convert datatype to 8-bit and save
    res_Robertson_8bit = np.clip(res_Robertson*255, 0, 255).astype('uint8')
    cv.imwrite("img/ldr_robertson.jpg", res_Robertson_8bit)

def LDR_fusion_Mertens():
    # Loading exposure images into a list
    img_fn = ["img/img1.jpg", "img/img2.jpg", "img/img3.jpg"]
    img_list = [cv.imread(fn) for fn in img_fn]
    
    # Exposure fusion using Mertens
    merge_mertens = cv.createMergeMertens()
    res_mertens = merge_mertens.process(img_list)

    # Convert datatype to 8-bit and save
    res_mertens_8bit = np.clip(res_mertens*255, 0, 255).astype('uint8')
    cv.imwrite("img/fusion_mertens.jpg", res_mertens_8bit)

def HDR_TMO_Mantiuk(fn,g):
    hdr_image = cv.imread(fn, cv.IMREAD_ANYDEPTH)
    tonemap = cv.createTonemapMantiuk(gamma=g)
    result = tonemap.process(hdr_image.copy())
    result_8bit = np.clip(result*255, 0, 255).astype('uint8')
    cv.imwrite("img/TMO_Mantiuk.jpg", result_8bit)
    
def HDR_TMO_Reinhard(fn,g):
    hdr_image = cv.imread(fn, cv.IMREAD_ANYDEPTH)
    tonemap = cv.createTonemapReinhard(gamma=g)
    result = tonemap.process(hdr_image.copy())
    result_8bit = np.clip(result*255, 0, 255).astype('uint8')
    cv.imwrite("img/TMO_Reinhard.jpg", result_8bit)

#===========================
# Opérateurs de tone mapping
#===========================

def TMO_norm(fn):

    # lecture de l'image    
    hdr_image = cv.imread(fn, cv.IMREAD_ANYDEPTH)

    # Je resize l'image car je ne sais pas coder en python
    small_to_large_image_size_ratio = 0.2
    tone_img = cv.resize(hdr_image, # original image
                        (0,0), # set fx and fy, not the final size
                        fx=small_to_large_image_size_ratio, 
                        fy=small_to_large_image_size_ratio, 
                        interpolation=cv.INTER_NEAREST)

    # On cherche la luminance max Vmax
    Vmax = 0
    for group in tone_img:
        for pix in group:
            
            Vin = 1./61 * (pix[0] * 20 + pix[1] * 40 + pix[2])
            if Vin >= Vmax:
                Vmax = Vin

    # Tone mapping
    tone_img = tone_img / (Vmax+1)

    # Conversion et sauvegarde
    result_8bit = np.clip(tone_img*255, 0, 255).astype('uint8')
    cv.imwrite("img/TMO_norm.jpg", result_8bit)

    return

def TMO_gamma(fn,g):
    
    # lecture de l'image    
    hdr_image = cv.imread(fn, cv.IMREAD_ANYDEPTH)
    
    # Tone mapping gamma
    res_gamma = cv.pow(hdr_image, 1.0/g)

    # Conversion et sauvegarde
    result_8bit = np.clip(res_gamma*255, 0, 255).astype('uint8')
    cv.imwrite("img/TMO_gamma.jpg", result_8bit)

    return

def TMO_log(fn, k, q):

    # lecture de l'image    
    hdr_image = cv.imread(fn, cv.IMREAD_ANYDEPTH)

    # vectorisation et prod vectoriel (merci nabil) pour trouver Lmax
    cvt = hdr_image[:]
    vec = [0.2126, 0.7152, 0.0722]
    L_array = np.dot(hdr_image,vec)
    Lmax=np.max(L_array)
   
    # Tone map log
    L_d = np.log10(1 + L_array * q) / np.log10(1 + Lmax * k)
    cvt *= L_d[..., np.newaxis] / L_array[..., np.newaxis]

    # Conversion et sauvegarde
    result_8bit = np.clip(cvt*255, 0, 255).astype('uint8')
    cv.imwrite("img/TMO_log.jpg", result_8bit)

    return

def TMO_exp(fn, k, q):

    # lecture de l'image
    hdr_image = cv.imread(fn, cv.IMREAD_ANYDEPTH)

    q = 1 if q < 1 else q
    k = 1 if k < 1 else k

    # vectorisation et prod vectoriel (merci nabil) pour trouver Lmax
    cvt = hdr_image[:]
    vec = [0.2126, 0.7152, 0.0722]
    L_array = np.dot(hdr_image,vec)
    L_a=np.average(L_array)
   
    # Tone map
    L_d = 1 - np.exp(-(L_array * q) / (L_a * k))
    cvt*= L_d[..., np.newaxis] / L_array[..., np.newaxis]

    # Conversion et sauvegarde
    result_8bit = np.clip(cvt * 255, 0, 255).astype('uint8')
    cv.imwrite("img/TMO_exp.jpg", result_8bit)

    return

def TMO_local(fn, alpha):

    # lecture de l'image
    hdr_image = cv.imread(fn, cv.IMREAD_ANYDEPTH)

    #
    hdr_image_vec = hdr_image[:]
    vec = [0.2126, 0.7152, 0.0722]
    L_array = np.dot(hdr_image,vec)
    V_array = cv.GaussianBlur(L_array,(15,15),-1)
    
    itm = np.divide(L_array, np.power(V_array, 1-alpha))
    hdr_image_vec *= itm[..., np.newaxis] / L_array[..., np.newaxis]  # new luminance for each pixel

    

    # Conversion et sauvegarde
    result_8bit = np.clip(hdr_image_vec*255, 0, 255).astype('uint8')
    cv.imwrite("img/TMO_local.jpg", result_8bit)
    
    return

def TMO_durand(fn):

    # lecture de l'image
    hdr_image = cv.imread(fn, cv.IMREAD_ANYDEPTH)
    target_contrast = np.log2(10)
    #
    hdr_image_vec = hdr_image[:]
    vec = [0.2126, 0.7152, 0.0722]
    L_array = np.dot(hdr_image,vec)
    L_array_log = np.log2(np.dot(hdr_image,vec))

    large_scale = cv.bilateralFilter(L_array_log.astype('float32'),-1,2,2)
    details = L_array_log - large_scale

    max_L = np.max(large_scale)
    k = target_contrast / (max_L - np.min(large_scale))
    offset = max_L * k
    out_log = details + large_scale * k - offset

    O = np.exp(out_log + details)

    itm = np.divide(L_array, O)
    hdr_image_vec *= itm[..., np.newaxis] / L_array[..., np.newaxis]  # new luminance for each pixel

    # Conversion et sauvegarde
    result_8bit = np.clip(hdr_image_vec*255, 0, 255).astype('uint8')
    cv.imwrite("img/TMO_durand.jpg", result_8bit)
    
    return

