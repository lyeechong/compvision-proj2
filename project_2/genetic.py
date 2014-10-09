#!/lusr/bin/python

import cv2
import random
import stereo
from random import randint
import numpy
from multiprocessing.pool import ThreadPool
import time

def test_weights(left, right):
    num_threads = 500
    pool = ThreadPool(processes=num_threads)
    results = {}
    swag = {}
    for x in range(0,num_threads):
        weights = tuple(randomize())        
        # print "starting thread", x, "with", weights
        results[weights] = pool.apply_async(evaluate_weights, (left, right, weights,))
    print "spun up all processes, waiting on results.."
    for key in results:
        res = 9001
        try:
            res = results[key].get(timeout=1)
        except Exception as e:
            # yolo
            pass
        #print res, key
        swag[key] = res

    sorted_swag = sorted(swag, key=lambda key: swag[key])
    print "best found for this pass:"
    print sorted_swag[0], swag[sorted_swag[0]]
    return sorted_swag[0], swag[sorted_swag[0]] # list of weights, median

def repeat(left, right):
    num_repeat = 500
    curr_best_median = 9001
    curr_best_weights = []
    for x in range(0,num_repeat):
        print "beginning pass", x
        local_best = test_weights(left, right)
        if(local_best[1] < curr_best_median):
            curr_best_median = local_best[1]
            curr_best_weights = local_best[0]
    print "==== DONE ==="
    print "Best median found:", curr_best_median
    print "Best weights found:", curr_best_weights

def randomize():
    # (1, 32, 47, 9, 13, 76, 41, 45, 30, 96) 6
    # (3, 80, 79, 11, 11, 166, 16, 60, 41, 151) 6
    weights = random.sample(xrange(200), 10)
    weights[0] = randint(1,12)
    weights[1] = randint(0,12) * 16 # multiple of 16
    weights[4] = randint(5,16)
    weights[5] = randint(0,200)
    return weights

def evaluate_weights(left, right, weights):
     # Compute disparity using the function under test.
    disparity = stereo.disparity_map_with_params(left, right, weights)

    # Compute the difference between the two. Useful to visualize this!
    disparity_diff = cv2.absdiff(disparity, disparity_expected)

    # The median difference between the expected and actual disparity
    # should be less than the specified threshold.
    differences = disparity_diff.flatten().tolist()
    median_diff = sorted(differences)[len(differences) / 2]

    return median_diff

if __name__ == '__main__':
    # Change the directory to the images we want to test on
    directory = 'Aloe'

    left = cv2.imread('disparity_test_data/' + directory + '/view1.png')
    right = cv2.imread('disparity_test_data/' + directory + '/view5.png')

    # Load the ground-truth disparity map.
    disparity_expected = cv2.imread('disparity_test_data/' + directory + '/disp1.png',
                                  cv2.CV_LOAD_IMAGE_GRAYSCALE)
    
    weights = [3, 96, 0, 16, 15, 100, 32, 1, 23, 50]
    
    repeat(left, right)
    
   
