import cv2
import numpy as np

# Specify input and output coordinates that is used
# to calculate the transformation matrix
input_pts = np.float32([[80, 1286], [3890, 1253], [3890, 122], [450, 115]])
output_pts = np.float32([[100, 100], [100, 3900], [2200, 3900], [2200, 100]])

# Compute the perspective transform M
M = cv2.getPerspectiveTransform(input_pts, output_pts)
print(M)
# http://www.smallbulb.net/2013/351-opencv-convert-projection-matrix-to-maps
# findHomography
# https://tech-genesis.cn/others/opencv_tutorial2.4.13/modules/imgproc/doc/geometric_transformations.html
# https://maplab.asl.ethz.ch/docs/devel/restore_maplab_server/api/classaslam_1_1MappedUndistorter.html
# https://agmanic.com/optics-basics-camera-calibration/
# InitUndistortRectifyMap

