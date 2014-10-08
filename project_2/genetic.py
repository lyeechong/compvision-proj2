#!/lusr/bin/python

import cv2
import random
import stereo
from random import randint
import numpy
from multiprocessing.pool import ThreadPool
import time

disparity_expected = None
best = 0
best_weights = []

def test_weights(left, right, weights):
    num_threads = 100
    pool = ThreadPool(processes=num_threads)
    results = {}
    swag = {}
    for x in range(0,num_threads):
        weights = tuple(randomize())        
        print "starting thread", x, "with", weights
        results[weights] = pool.apply_async(evaluate_weights, (left, right, weights,))
    for key in results:
        res = results[key].get(timeout=30)
        print res, key
        swag[key] = res

    sorted_swag = sorted(swag, key=lambda key: swag[key])
    print "hellooooooo"
    print sorted_swag[0], swag[sorted_swag[0]]
        
def randomize():
    weights = random.sample(xrange(100), 10)
    weights[1] = randint(0,10) * 16
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
    
    test_weights(left, right, weights)
    
   
