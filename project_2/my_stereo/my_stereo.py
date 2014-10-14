import stereo
import cv2
import numpy as np

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
    return warped

def _translate_homography(homography, t_x, t_y):
    t_matrix = (
        np.float32([1, 0, (-1 * t_x), 0, 1, (-1 * t_y), 0, 0, 1])
        .reshape(3, 3)
    )
    return np.dot(t_matrix, homography)
    

print 'start'

left = cv2.imread('my_left.jpg')
right = cv2.imread('my_right.jpg')

f_mat, H1, H2 = stereo.rectify_pair(left, right)

print "rectified"

rect_left = warp_image(left, H1)
rect_right = warp_image(right, H2)

cv2.imshow('left', rect_left)
cv2.imshow('right', rect_right)

cv2.waitKey(10000)
 
print "warped"

disparity = stereo.disparity_map(rect_left[0:888, 0:1200], rect_right[0:888, 0:1200])

print "disparity"

cv2.imshow('disparity', disparity)