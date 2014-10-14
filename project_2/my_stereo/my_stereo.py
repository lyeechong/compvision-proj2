import stereo
import cv2

print 'start'

left = cv2.imread('my_left.jpg')
right = cv2.imread('my_right.jpg')
disparity = stereo.disparity_map(left, right)

print "disparity"

# cv2.imshow('disparity', disparity)