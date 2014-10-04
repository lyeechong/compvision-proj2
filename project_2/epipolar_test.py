"""
Our own little test thing
"""

import cv2
import math
import numpy as np
import stereo
from matplotlib import pyplot as plt

def drawlines(img1,img2,lines,pts1,pts2):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r,c = img1.shape
    img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)

    
    for r,pt1,pt2 in zip(lines,pts1,pts2):
        color = tuple(np.random.randint(0,255,3).tolist())
        x0,y0 = map(int, [0, -r[2]/r[1] ])
        x1,y1 = map(int, [c, -(r[2]+r[0]*c)/r[1] ])
        cv2.line(img1, (x0,y0), (x1,y1), color,1)

        # print "tuple ", pt1
        # print "color " + str(color)
        cv2.circle(img1,(int(pt1[0][0]),int(pt1[0][1])),5,color,-1)
        cv2.circle(img2,(int(pt2[0][0]),int(pt2[0][1])),5,color,-1)

    return img1,img2

image_a = cv2.imread('test_data/kitchen_left.jpg',0)
image_b = cv2.imread('test_data/kitchen_right.jpg',0)

# Find epilines corresponding to points in right image (second image) and
# drawing its lines on left image

pts1, pts2 = stereo.find_feature_points(image_a, image_b)
F, fundamental_mask = cv2.findFundamentalMat(pts1, pts2, cv2.RANSAC) 

lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1,1,2), 2,F)
lines1 = lines1.reshape(-1,3)
img5,img6 = drawlines(image_a,image_b,lines1,pts1,pts2)


# Find epilines corresponding to points in left image (first image) and
# drawing its lines on right image
lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1,1,2), 1,F)
lines2 = lines2.reshape(-1,3)
img3,img4 = drawlines(image_b,image_a,lines2,pts2,pts1)

cv2.imwrite("epi_left.jpg", img5)
cv2.imwrite("epi_right.jpg", img3)

plt.subplot(121),plt.imshow(img5)
plt.subplot(122),plt.imshow(img3)
plt.show()


