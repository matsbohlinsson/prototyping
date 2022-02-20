from pathlib import Path

import cv2 #opencv-python
#read image
img = cv2.imread(Path('KosterSkargard1.jpg').as_posix())
#print its shape
print('Image Dimensions :', img.shape)
