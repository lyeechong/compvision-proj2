"""Unit tests for the stereo module.

Implement your stereo module so that all tests pass.
An example of how to run these tests is given in run_tests.sh.

The tests below will be used to test the correctness of your
implementation.

You should add additional detailed tests as you add more
of your own functions to your implementation!
"""

import cv2
import stereo
import numpy
import unittest


class TestStereo(unittest.TestCase):
    """Tests the functionality of the stereo module."""

    def setUp(self):
        """Initializes shared state for unit tests."""
        pass

    def _matrix_diff(self, expected, actual, name):
        """Compares matrices, returning the norm of their difference."""
        difference = numpy.absolute(expected - actual)
        difference_magnitude = numpy.linalg.norm(difference)

        print "Expected", name, ":"
        print expected
        print "Actual", name, ":"
        print actual
        print "Difference"
        print difference
        print "Magnitude of difference:", difference_magnitude
        return difference_magnitude

    def test_rectify_pair(self):
        left = cv2.imread('test_data/kitchen_left.jpg')
        right = cv2.imread('test_data/kitchen_right.jpg')

        F, H_left, H_right = stereo.rectify_pair(left, right)

        # Check accuracy against known fundamental matrix and homographies.
        max_difference_magnitude = 0.5

        F_expected = numpy.array(
            [[2.38958660e-07, -2.30078185e-05, -3.82577705e-03],
             [-4.57131715e-05, -2.03219010e-06, 1.42189842e-01],
             [-5.01095221e-03, -1.09146504e-01, 1.00000000e+00]])
        F_diff = self._matrix_diff(F_expected, F, "fundamental matrix")
        self.assertLessEqual(F_diff, max_difference_magnitude)

        H_left_expected = numpy.array(
            [[-9.78273713e-02, 6.04430191e-02, -1.69179548e+01],
             [-4.78698812e-03, -1.09671985e-01, 2.31661658e-01],
             [4.25159162e-05, -8.17208264e-07, -1.32607389e-01]])
        H_left_diff = self._matrix_diff(H_left_expected, H_left,
                                        "left rectifying homography")

        H_right_expected = numpy.array(
            [[1.04725916e+00, 1.32521331e-01, -7.95404897e+01],
             [-2.73716541e-02, 1.00451089e+00, 5.43598999e+00],
             [1.96336656e-04, 2.48446573e-05, 9.32407071e-01]])
        H_right_diff = self._matrix_diff(H_right_expected, H_right,
                                         "right rectifying homography")

    def test_disparity_map(self):
        left = cv2.imread('test_data/tsukuba/left.png')
        right = cv2.imread('test_data/tsukuba/right.png')

        # Load the ground-truth disparity map.
        disparity_expected = cv2.imread('test_data/tsukuba/disparity_left.png',
                                        cv2.CV_LOAD_IMAGE_GRAYSCALE)

        # Compute disparity using the function under test.
        disparity = stereo.disparity_map(left, right)

        # Compute the difference between the two. Useful to visualize this!
        disparity_diff = cv2.absdiff(disparity, disparity_expected)

        # The median difference between the expected and actual disparity
        # should be less than the specified threshold.
        differences = disparity_diff.flatten().tolist()
        median_diff = sorted(differences)[len(differences) / 2]
        self.assertLessEqual(median_diff, 5)

    def test_point_cloud(self):
        disparity = cv2.imread('test_data/tsukuba/disparity_left.png',
                               cv2.CV_LOAD_IMAGE_GRAYSCALE)
        colors = cv2.imread('test_data/tsukuba/left.png')
        focal_length = 10

        ply_string = stereo.point_cloud(disparity, colors, focal_length)
        # View me in Meshlab!
        with open("tsukuba.ply", 'w') as f:
            f.write(ply_string)
        # Trivial test. We'll also inspect the cloud visually.
        self.assertGreater(len(ply_string), 0)

if __name__ == '__main__':
    unittest.main()
