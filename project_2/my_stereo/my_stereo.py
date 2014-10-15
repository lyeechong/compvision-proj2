import stereo
import cv2
import numpy as np

left = cv2.imread('4l.jpg')
right = cv2.imread('4r.jpg')

disparity = stereo.disparity_map(left, right)
cv2.imwrite('disparity.png', disparity)

cloud = stereo.point_cloud(disparity, right, -3)
with open("cloud.ply", 'w') as f:
    f.write(cloud)