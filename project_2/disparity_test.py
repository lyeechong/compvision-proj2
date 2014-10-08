import cv2
import stereo
import numpy
import unittest

directory = 'Aloe'
directory = 'Baby1'
directory = 'Plastic'

left = cv2.imread('disparity_test_data/' + directory + '/view1.png')
right = cv2.imread('disparity_test_data/' + directory + '/view5.png')

# Load the ground-truth disparity map.
disparity_expected = cv2.imread('disparity_test_data/' + directory + '/disp1.png',
                              cv2.CV_LOAD_IMAGE_GRAYSCALE)

print disparity_expected

# Compute disparity using the function under test.
disparity = stereo.disparity_map(left, right)

print disparity

# Compute the difference between the two. Useful to visualize this!
disparity_diff = cv2.absdiff(disparity, disparity_expected)

# The median difference between the expected and actual disparity
# should be less than the specified threshold.
differences = disparity_diff.flatten().tolist()
median_diff = sorted(differences)[len(differences) / 2]
print "median ", median_diff
