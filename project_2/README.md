Project 2: Stereo
========

## Due: 14 Oct 2014, 11:59pm

<img src="https://raw.githubusercontent.com/ut-cs378-vision-2014fall/course-info/master/images/stereo_header.png"/>

In this project, you'll reconstruct a 3D scene from stereo image pairs.

At a minimum, your stereo reconstruction implementation will:
* identify epipolar geometry of a stereo pair
* compute a fundamental matrix relating epipolar geometry from one image to the other
* compute homographies to rectify the stereo images so epipolar lines are in corresponding rows
* compute disparities between rectified stereo images
* convert disparities to a 3D model

### Rectify a stereo image pair (30 points)

[Epipolar geometry](http://en.wikipedia.org/wiki/Epipolar_geometry) relates two stereo cameras and images by constrainting where corresponding points lie in their images. Most stereo algorithms rely on epipolar lines lying in corresponding image rows of a stereo pair. The process of converting a pair of input images to a new pair where epipolar lines lie on corresponding image rows is called image rectification.

#### Feature matching

Just as when we were matching images for panorama stitching, the first thing we need to do to compute epipolar geometry from a pair of images is to establish some correspondences between the images. One common way of doing this is to identify "interest points" or "key points" in both images, summarize their appearances using descriptors, and then establish matches between these "features" (interest points combined with their descriptors)  by choosing features with similar descriptors from each image.

You're welcome to establish correspondences any way you like. I would recommend you consider extracting keypoints and descriptors using the [cv2.SIFT](http://docs.opencv.org/modules/nonfree/doc/feature_detection.html#sift) interface to compute interest points and descriptors, and using one of [the descriptor matchers OpenCV provides](http://docs.opencv.org/modules/features2d/doc/common_interfaces_of_descriptor_matchers.html) under a common interface.

#### Computing the fundamental matrix

The [fundamental matrix](http://en.wikipedia.org/wiki/Fundamental_matrix_(computer_vision)) maps points in one stereo image to epipolar lines in the other. It can be computed using corresponding points in two images recovered in the feature matching stage. In particular, [`cv2.findFundamentalMat()`](http://docs.opencv.org/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#findfundamentalmat) implements just this approach. Here's an example of epipolar lines mapped using the fundamental matrix between stereo images:

<img src="https://raw.githubusercontent.com/ut-cs378-vision-2014fall/course-info/master/images/epipolar_lines.png"/>

#### Rectifying the images

Once we know the fundamental matrix, we can compute homographies that warp the images in the pair so that corresponding rows in the two images are epipolar lines. See [`cv2.stereoRectifyUncalibrated()`](http://docs.opencv.org/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#stereorectifyuncalibrated).

<img src="https://raw.githubusercontent.com/ut-cs378-vision-2014fall/course-info/master/images/rectified.png"/>

You may find it helpful to crop the images to just the mutually overlapping regions of the rectified images, to avoid computation where there are no corresponding pixels present in one or the other image.

### Disparity computation (20 points)

Once we have a rectified stereo pair, the next step is to compute disparities between correponding pixels. There are many strategies and algorithms to do this, and most have plenty of parameters to tune. You may want to start by looking at [`StereoBM`](http://docs.opencv.org/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#stereobm) and [`StereoSGBM`](http://docs.opencv.org/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#stereosgbm) which are part of the OpenCV library.

To get the best results from disparity computation, you'll need to carefully consider each parameter and its effect on the disparity image output. There is a lot of "art" to tuning disparity computation, so you'll probably want to look at many inputs, not just the one used in the unit test. For a bunch of example inputs, most with ground-truth disparities, see the [Middlebury Stereo Datasets](http://vision.middlebury.edu/stereo/data/) page.

### Point cloud conversion (10 points)

Disparity can be converted to depth if we know the focal length of the camera. Although we can't know this focal length exactly for an uncalibrated camera like our cell phone, we can take a guess and see the results in 3D.

Implement a function that converts a disparity image to a [PLY](http://en.wikipedia.org/wiki/PLY_(file_format)) point cloud, given a focal length. For an example of one way to do this, see the [`stereo_match.py`](https://github.com/Itseez/opencv/blob/master/samples/python2/stereo_match.py) example from the OpenCV source code, although beware that their Q projection matrix is buggy. You will want a projection matrix similar to:

```
[ 1  0             0   image_width / 2 ]
[ 0  1             0  image_height / 2 ]
[ 0  0  focal_length                 0 ]
[ 0  0             0                 1 ]
```

You can view your PLY point clouds in [Meshlab](http://meshlab.sourceforge.net/).

<img src="https://raw.githubusercontent.com/ut-cs378-vision-2014fall/course-info/master/images/point_cloud.png"/>

### Results (20 points)

Capture at least one stereo pair of images using any camera you like (your phone's camera will probably do fine) and create a disparity image and 3D point cloud using your implemenation. Add the source images, the disparity image, the point cloud, and a script that can regenerate the outputs from your implementation into the `my_stereo` folder. Include a `README.txt` or `README.md` (Markdown format) explaining how to regenerate your panos.

You'll find that it can be tough to make a good stereo scene. Try to move the camera deliberately to capture a clear change of viewpoint, but not too much, so there is still a lot of shared surfaces visible on both images. Include textured objects in your scene so that disparity computation algorithms have a better chance of success. Play around and see what works best.

### Code quality and review (20 points)

Above and beyond just passing the pep8 style checker, you should strive to write readable, modular, well-factored code. As in project 1, each group will review three other groups code, and then receive ratings on the quality of their review. You'll receive up to 10 points for the quality of your groups review. After you revise your code in response to review, we'll go over your final code and rate it's quality for up to another 10 points. Hint: the style and comments of OpenCV tutorials is not a model you should emulate :)

### Extra credit (maximum of 50 points)

There's a lot more to stereo than the minimum specified above. Complete any of the additional work below for extra credit.

Be sure to include code for the extra credit as part of your check-in. Also, please add a PDF write-up describing which extra credit you implemented including your results called `extra_credit.pdf` in the project_2 directory so we can see your results.

#### Implement your own disparity computation (20 points)

Implement any algorithm for computing disparity from a rectified stereo pair. There is an excellent overview of many popular algorithms [here](http://vision.middlebury.edu/stereo/taxonomy-IJCV.pdf). 

Prove that your implementation works by using it to produce a disparity image from a rectified stereo pair.

#### Implement multi-view stereo reconstruction of 3D models (30 points)

Multi-view stereo uses not just 2 but N images of a scene or object to extract a more complete 3D model of the scene. See [this site](http://vision.middlebury.edu/mview/) for an overview of several multi-view stereo methods, as well as example input data sets that you can use to test your implementation.

Prove that your implementation works by using it to produce a 3D model of an object. It's fine to use one of the example inputs, but consider trying to make a 3D model of an interesting object you have lying around!

## Logistics

You will work on this project in randomly assigned groups of three. All group members should have identical submissions in each of their private repositories by the project due date. We will select one group member's repository, clone it, and use it to compute the grade for all group members.

If the group chooses to turn in a project N days late, each individual in the group will lose N of their remaining late days for the semester. If one or more students have no more late days left, they'll lose credit without affecting the other group members' grades.


