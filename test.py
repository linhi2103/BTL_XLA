import cv2
import numpy as np

def show(img):
    value = np.max(img)
    img = img*(255/value)
    img = img.astype(np.uint8) 
    return img

def convert_to_grayscale(img):
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    finally:
        return img
    
def FTransform(img):
    dft = np.fft.fft2(img)
    dft_shift = np.fft.fftshift(dft)
    return dft_shift

def tang_tuong_phan(img, alpha=0, beta=255):
    newImg = convert_to_grayscale(img)
    newImg = cv2.normalize(newImg, None, alpha, beta, cv2.NORM_MINMAX)
    return show(newImg)

def inverseFTransform(fshift):
    f_ishift = np.fft.ifftshift(fshift)
    img = np.abs(np.fft.ifft2(f_ishift))
    img = tang_tuong_phan(img, 0, 1)[0]
    return img      
  
def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def kernelIdeal(img, D=30):
    rows, cols = img.shape[:2]
    kernel = np.zeros((rows, cols))
    center = (rows / 2, cols / 2)
    for i in range(rows):
        for j in range(cols):
            s = distance((i, j), center)
            kernel[i, j] = 1 if s <= D else 0
    return kernel

def LPF(img):
    img = convert_to_grayscale(img)
    dft_shift = FTransform(img)
    maskIdeal = kernelIdeal(img)
    ideal = inverseFTransform(dft_shift * maskIdeal)
    cv2.imshow('1234',ideal)
    return ideal

img=cv2.imread('./img/bila.jpg')
cv2.imshow('123',img)
LPF(img)
cv2.waitKey()
cv2.destroyAllWindows()