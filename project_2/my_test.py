"""
Our own little test thing
"""

import cv2
import math
import numpy
import stereo

image_a = cv2.imread('test_data/tsukuba/left.png')
image_b = cv2.imread('test_data/tsukuba/right.png')

stereo.find_fundamental_mat(image_a, image_b)
