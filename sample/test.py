import cv2
import numpy as np
def norm(img):
    img = img - np.percentile(img, 5)
    img = img / np.percentile(img, 95)

    img = np.uint8(255*np.clip(img, 0, 1))
    return img

img = cv2.imread(r'thermal-25080.tiff', -1)
img8 = norm(img)
h, w = img.shape
img8 = cv2.resize(img8, (w*2, h*2))
img8 = cv2.rotate(img8, cv2.ROTATE_180)
cv2.imshow('img', img8)
cv2.waitKey(0)