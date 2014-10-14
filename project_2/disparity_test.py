#!/lusr/bin/python

import cv2
import stereo
import numpy
import unittest

if __name__ == '__main__':
    # Change the directory to the images we want to test on
    #directory = 'Aloe'
    #directory = 'Baby1'
    directory = 'Plastic'
    
    # If you want the images to show
    showImages = True

    left = cv2.imread('disparity_test_data/' + directory + '/view1.png')
    right = cv2.imread('disparity_test_data/' + directory + '/view5.png')

    # Load the ground-truth disparity map.
    disparity_expected = cv2.imread('disparity_test_data/' + directory + '/disp1.png',
                                  cv2.CV_LOAD_IMAGE_GRAYSCALE)

    print disparity_expected

    # Compute disparity using the function under test.
    disparity = stereo.disparity_map_with_params(left, right, (9, 112, 107, 9, 5, 167, 22, 12, 25, 195))

    print disparity

    # Compute the difference between the two. Useful to visualize this!
    disparity_diff = cv2.absdiff(disparity, disparity_expected)

    # The median difference between the expected and actual disparity
    # should be less than the specified threshold.
    differences = disparity_diff.flatten().tolist()
    median_diff = sorted(differences)[len(differences) / 2]

    if (showImages):
        cv2.imshow("sbm", disparity)
        cv2.waitKey(4000)
        cv2.imshow("sbm", disparity_expected)
        cv2.waitKey(4000)

    print "median ", median_diff
