import stereo
import cv2

left = cv2.imread('set_left.jpg')
right = cv2.imread('set_right.jpg')

disparity = stereo.disparity_map(left, right)
cv2.imwrite("set_disparity.jpg", disparity)

colors = left
focal_length = 5
ply_string = stereo.point_cloud(disparity, colors, focal_length)

with open("set.ply", 'w') as f:
    f.write(ply_string)
