import math
import cv2
import numpy as np

def convert_to_grayscale(img):
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    finally:
        return img

def show(img):
    value = np.max(img)
    img = img*(255/value)
    img = img.astype(np.uint8)  
    return img

def can_bang_histogram(img):
    newImg = convert_to_grayscale(img)
    newImg = cv2.equalizeHist(newImg)
    return [newImg]

def tach_nguong(img, thresh=127, maxVal=255):
    newImg = convert_to_grayscale(img)
    newImg = cv2.threshold(newImg, thresh, maxVal, cv2.THRESH_BINARY)[1]
    return [show(newImg)]

def am_ban(img):
    newImg = convert_to_grayscale(img)
    newImg = 255 - newImg
    return [show(newImg)]

def logarith(img):
    newImg = convert_to_grayscale(img)
    newImg = cv2.log(1.0 + newImg)
    return [show(newImg)]

def tang_tuong_phan(img, alpha=0, beta=255):
    newImg = convert_to_grayscale(img)
    newImg = cv2.normalize(newImg, None, alpha, beta, cv2.NORM_MINMAX)
    return [show(newImg)]

def loc_trung_binh(img, kernel=(5, 5)):
    newImg = cv2.blur(img, kernel)
    return [show(newImg)]

def loc_trung_vi(img, kernel=5):
    newImg = cv2.medianBlur(img, kernel)
    return [show(newImg)]

def loc_gauss(img, kernel=(5, 5), sigma=0):
    newImg = cv2.GaussianBlur(img, kernel, sigma)
    return [show(newImg)]

def loc_sac_net(img, alpha=1.5, beta=-0.5, gamma=0):
    newImg = cv2.addWeighted(img, alpha, loc_gauss(img)[0], beta, gamma)
    return [show(newImg)]

def gradient(img, ddepth=-1):
    newImg = convert_to_grayscale(img)
    sobelX = cv2.Sobel(newImg, ddepth, 1, 0)
    sobelY = cv2.Sobel(newImg, ddepth, 0, 1)
    return [sobelX, sobelY]

def nhan_dien_bien(img):
    res = gradient(img, cv2.CV_32F)
    gx, gy = res[0], res[1]
    magnitude = cv2.magnitude(gx, gy)
    return tach_nguong(magnitude)

#tính khoảng cách từ center của nhân
def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

#lọc Ideal
def kernelIdeal(img, D=30):
    rows, cols = img.shape[:2]
    kernel = np.zeros((rows, cols))
    center = (rows / 2, cols / 2)
    for i in range(rows):
        for j in range(cols):
            s = distance((i, j), center)
            kernel[i, j] = 1 if s <= D else 0
    return kernel

#lọc Butter
def kernelButter(img, D=30, n=2):
    rows, cols = img.shape[:2]
    kernel = np.zeros((rows, cols))
    center = (rows / 2, cols / 2)
    for i in range(rows):
        for j in range(cols):
            s = distance((i, j), center)
            kernel[i, j] = 1.0 / (1.0 + (s / D) ** (2 * n))
    return kernel

#lọc Gauss
def kernelGauss(img, D=30):
    rows, cols = img.shape[:2]
    kernel = np.zeros((rows, cols))
    center = (rows / 2, cols / 2)
    for i in range(rows):
        for j in range(cols):
            s = distance((i, j), center)
            kernel[i, j] = math.exp(-(s ** 2 / D ** 2 / 2))
    return kernel

def FTransform(img):
    fft = np.fft.fft2(img)
    shift_fft = np.fft.fftshift(fft)
    return shift_fft

def inverseFTransform(fshift):
    f_ishift = np.fft.ifftshift(fshift)
    img = np.abs(np.fft.ifft2(f_ishift))
    img = tang_tuong_phan(img, 0, 1)[0]
    return img

def thong_thap_LPF(img):
    img = convert_to_grayscale(img)
    dft_shift = FTransform(img)
    maskIdeal = kernelIdeal(img)
    maskButter = kernelButter(img)
    maskGauss = kernelGauss(img)
    ideal = inverseFTransform(dft_shift * maskIdeal)
    butter = inverseFTransform(dft_shift * maskButter)
    gauss = inverseFTransform(dft_shift * maskGauss)
    return [ideal]

def thong_cao_HPF(img):
    img = convert_to_grayscale(img)
    dft_shift = FTransform(img)
    maskIdeal = 1 - kernelIdeal(img)
    maskButter = 1 - kernelButter(img)
    maskGauss = 1 - kernelGauss(img)
    ideal = inverseFTransform(dft_shift * maskIdeal)
    butter = inverseFTransform(dft_shift * maskButter)
    gauss = inverseFTransform(dft_shift * maskGauss)
    return [ideal]

def bilateral(img, d=7, sigmaColor=75, sigmaSpace=75):
    newImg = cv2.bilateralFilter(img, d, sigmaColor, sigmaSpace)
    return [show(newImg)]

def nonLocalMeans(img):
    newImg = cv2.fastNlMeansDenoising(img)
    return [show(newImg)]
