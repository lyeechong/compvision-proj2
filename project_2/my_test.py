"""
Our own little test thing
"""

import cv2
import math
import numpy as np
import stereo

def warp_image(image, homography):
    """Warps 'image' by 'homography'

    Arguments:
      image: a 3-channel image to be warped.
      homography: a 3x3 perspective projection matrix mapping points
                  in the frame of 'image' to a target frame.

    Returns:
      - a new 4-channel image containing the warped input, resized to contain
        the new image's bounds. Translation is offset so the image fits exactly
        within the bounds of the image. The fourth channel is an alpha channel
        which is zero anywhere that the warped input image does not map in the
        output, i.e. empty pixels.
      - an (x, y) tuple containing location of the warped image's upper-left
        corner in the target space of 'homography', which accounts for any
        offset translation component of the homography.
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    h, w, _ = image.shape

    pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
    trans = cv2.perspectiveTransform(pts, homography)
    t_x = trans[0][0][0]
    t_y = trans[0][0][1]

    x, y = np.ptp(trans, axis=0)[0]
    t_homography = _translate_homography(homography, t_x, t_y)
    warped = cv2.warpPerspective(image, t_homography, (x, y))
    return (warped, (t_x, t_y))


def _translate_homography(homography, t_x, t_y):
    t_matrix = (
        np.float32([1, 0, (-1 * t_x), 0, 1, (-1 * t_y), 0, 0, 1])
        .reshape(3, 3)
    )
    return np.dot(t_matrix, homography)

image_a = cv2.imread('test_data/kitchen_left.jpg')
image_b = cv2.imread('test_data/kitchen_right.jpg')

_, h1, h2 = stereo.rectify_pair(image_a, image_b)

i_a = warp_image(image_a, h1)[0]
i_b = warp_image(image_b, h2)[0]

cv2.imwrite('test_data/left.jpg', i_a)
cv2.imwrite('test_data/right.jpg', i_b)
