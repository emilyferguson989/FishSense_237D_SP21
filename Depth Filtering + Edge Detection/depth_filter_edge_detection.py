from scipy import ndimage
from scipy.ndimage.filters import convolve
from scipy import misc
import numpy as np
from utils import utils
from medpy.filter.smoothing import anisotropic_diffusion
import argparse
from typing import List
import pyrealsense2 as rs
import cv2
import os
import copy
import sys

# Gaussian Blur & Edge detector code from https://github.com/FienSoP/canny_edge_detector applied
# to our setting

class cannyEdgeDetector:
    def __init__(self, imgs, sigma=1, kernel_size=5, weak_pixel=75, strong_pixel=255, lowthreshold=0.05, highthreshold=0.15):
        self.imgs = imgs
        self.imgs_final = []
        self.img_smoothed = None
        self.gradientMat = None
        self.thetaMat = None
        self.nonMaxImg = None
        self.thresholdImg = None
        self.weak_pixel = weak_pixel
        self.strong_pixel = strong_pixel
        self.sigma = sigma
        self.kernel_size = kernel_size
        self.lowThreshold = lowthreshold
        self.highThreshold = highthreshold
        return 
    
    def gaussian_kernel(self, size, sigma=1):
        size = int(size) // 2
        x, y = np.mgrid[-size:size+1, -size:size+1]
        normal = 1 / (2.0 * np.pi * sigma**2)
        g =  np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
        return g
    
    def sobel_filters(self, img):
        Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
        Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)

        Ix = ndimage.filters.convolve(img, Kx)
        Iy = ndimage.filters.convolve(img, Ky)

        G = np.hypot(Ix, Iy)
        G = G / G.max() * 255
        theta = np.arctan2(Iy, Ix)
        return (G, theta)
    

    def non_max_suppression(self, img, D):
        M, N = img.shape
        Z = np.zeros((M,N), dtype=np.int32)
        angle = D * 180. / np.pi
        angle[angle < 0] += 180


        for i in range(1,M-1):
            for j in range(1,N-1):
                try:
                    q = 255
                    r = 255

                   #angle 0
                    if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                        q = img[i, j+1]
                        r = img[i, j-1]
                    #angle 45
                    elif (22.5 <= angle[i,j] < 67.5):
                        q = img[i+1, j-1]
                        r = img[i-1, j+1]
                    #angle 90
                    elif (67.5 <= angle[i,j] < 112.5):
                        q = img[i+1, j]
                        r = img[i-1, j]
                    #angle 135
                    elif (112.5 <= angle[i,j] < 157.5):
                        q = img[i-1, j-1]
                        r = img[i+1, j+1]

                    if (img[i,j] >= q) and (img[i,j] >= r):
                        Z[i,j] = img[i,j]
                    else:
                        Z[i,j] = 0


                except IndexError as e:
                    pass

        return Z

    def threshold(self, img):

        highThreshold = img.max() * self.highThreshold;
        lowThreshold = highThreshold * self.lowThreshold;

        M, N = img.shape
        res = np.zeros((M,N), dtype=np.int32)

        weak = np.int32(self.weak_pixel)
        strong = np.int32(self.strong_pixel)

        strong_i, strong_j = np.where(img >= highThreshold)
        zeros_i, zeros_j = np.where(img < lowThreshold)

        weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))

        res[strong_i, strong_j] = strong
        res[weak_i, weak_j] = weak

        return (res)

    def hysteresis(self, img):

        M, N = img.shape
        weak = self.weak_pixel
        strong = self.strong_pixel

        for i in range(1, M-1):
            for j in range(1, N-1):
                if (img[i,j] == weak):
                    try:
                        if ((img[i+1, j-1] == strong) or (img[i+1, j] == strong) or (img[i+1, j+1] == strong)
                            or (img[i, j-1] == strong) or (img[i, j+1] == strong)
                            or (img[i-1, j-1] == strong) or (img[i-1, j] == strong) or (img[i-1, j+1] == strong)):
                            img[i, j] = strong
                        else:
                            img[i, j] = 0
                    except IndexError as e:
                        pass

        return img
    
    def detect(self):
        imgs_final = []
        for i, img in enumerate(self.imgs): 
            self.img_smoothed = anisotropic_diffusion(img)
            img = self.img_smoothed
            self.gradientMat, self.thetaMat = self.sobel_filters(img)
            self.nonMaxImg = self.non_max_suppression(self.gradientMat, self.thetaMat)
            self.thresholdImg = self.threshold(self.nonMaxImg)
            img_final = self.hysteresis(self.thresholdImg)
            self.imgs_final.append(img_final)

        return self.imgs_final


# depth filtering functions:
def get_depth_bounds(depth_array, bbox):
    avg_depth = 0
    count = 0
    for x in range(len(depth_array)):
        for y in range(len(depth_array[0])):
            # find average depth in bounding box
            if x > bbox[1] and x < bbox[3] and y > bbox[0] and y < bbox[2]:    
                avg_depth += depth_array[x][y]
                count += 1
                depth_array[x][y] = depth_array[x][y]
            # get rid of depth information which is not within bounding box
            else:
                depth_array[x][y] = 0
    # return depth lower and upper bound thresholds for fish
    avg_depth = avg_depth / count
    print(avg_depth)
    return (avg_depth - 0.25, avg_depth + 0.05)

def isolate_fish_depth(depth_array, lower_bound, upper_bound):
    print(lower_bound, upper_bound)
    for x in range(len(depth_array)):
        for y in range(len(depth_array[0])):
            # within bounding box and depth threshold
            if depth_array[x][y] > lower_bound and depth_array[x][y] < upper_bound:    
                depth_array[x][y] = depth_array[x][y]
            else:
                depth_array[x][y] = 0

def filter_depth_csv(csv_dir, bbox_dir, bboxes):
    i = 0
    for filename in os.listdir(csv_dir):
        depth_csv = os.path.join(csv_dir, filename)
        filename = filename[:len(filename) - 3] + 'txt'
        depth_bbox = os.path.join(bbox_dir, filename)

        # read in one text file containing bounding box coordinates
        with open(depth_bbox) as f:
            bbox = f.readlines()
        bbox = [int(x.strip()) for x in bbox] 
        bboxes.append(bbox)

        # read in one depth csv
        depth_array = np.genfromtxt(depth_csv, delimiter=',')
        print(depth_array[300][20])

        # get depth bounds for fish and get rid of depth info that
        # is not within bounding box
        lower_bound, upper_bound = get_depth_bounds(depth_array, bbox)
        # get rid of depth info which is not within the depth bounds of the fish
        isolate_fish_depth(depth_array, lower_bound, upper_bound)

        depth_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_array, alpha=255/depth_array.max()), cv2.COLORMAP_RAINBOW)
        cv2.imwrite("./depth_filtered_images/" + str(i).zfill(6) + ".png", cv2.cvtColor(depth_image, cv2.COLOR_RGB2BGR))
        i += 1


# depth filtering with whole fish bounding box
sys.setrecursionlimit(10**6)
bboxes = []
filter_depth_csv('depth_csv', 'depth_bbox', bboxes)

# edge detection
imgs = utils.load_data()
detector = cannyEdgeDetector(imgs, sigma=1.2, kernel_size=5, lowthreshold=0.06, highthreshold=0.17, weak_pixel=100)
imgs_final = detector.detect()
utils.get_coordinates(imgs_final, bboxes, 'gray')
