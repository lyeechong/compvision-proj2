import stereo
import cv2

print 'start'

left = cv2.imread('set_left.jpg')
right = cv2.imread('set_right.jpg')

print "shapes, ", left.shape, right.shape

disparity = stereo.disparity_map(left, right)

cv2.imshow('disparity', disparity)
cv2.waitKey(5000)

colors = left
focal_length = 5

ply_string = stereo.point_cloud(disparity, colors, focal_length)

with open("test.ply", 'w') as f:
    f.write(ply_string)
