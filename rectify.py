import cv2
import numpy as np
from matplotlib import pyplot as plt

camera_mtx = np.array([[511.03573247, 0.000000, 311.80346835], [0.000000, 508.22913692, 261.56701122], [0.000000, 0.000000, 1.000000]])
R = np.array([[1.000000, 0.000000, 0.000000], [0.000000, 1.000000, 0.000000], [0.000000, 0.000000, 1.000000]])

image = cv2.imread("sample/thermal-25080.tiff")
height, width, _ = image.shape
map1,map2=cv2.initUndistortRectifyMap(camera_mtx, None, None, None, (width, height), cv2.CV_32FC1)

mapped = cv2.remap(image, map1, map2, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))

plt.figure()
plt.imshow(image, interpolation='nearest')

plt.figure()
plt.imshow(mapped, interpolation='nearest')
plt.show()


