import numpy as np
import skimage
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import os
import scipy.misc as sm
import math
import cv2

# TODO: need head and tail bounding boxes for this
def get_head_tail_edges(img, bbox):
    indices = np.where(img != [0])
    coordinates = list(zip(indices[0], indices[1]))
    for x,y in coordinates:
        # create bounding boxes for head and tail using whole fish bounding box
        if y < bbox[0] or y > bbox[2] or (y > (bbox[0] + 30) and y < (bbox[2] - 30)):
            img[x][y] = 0
            coordinates.remove((x,y))
    coordinates = sorted(coordinates , key=lambda k: [k[0], k[1]])
    # half = len(coordinates)//2
    # coord1 = coordinates[:half]
    # coord2 = coordinates[half:]
    # return (coord1, coord2)
    return coordinates

def get_avg_from_points(list_of_points):
    sumx = 0
    sumy = 0
    for x,y in list_of_points:
        sumx += x
        sumy += y
    avgx = int(sumx/len(list_of_points))
    avgy = int(sumy/len(list_of_points))
    return (avgx, avgy)

def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def load_data(dir_name = 'depth_filtered_images'):    
    '''
    Load images from the "faces_imgs" directory
    Images are in JPG and we convert it to gray scale images
    '''
    imgs = []
    for filename in os.listdir(dir_name):
        if os.path.isfile(dir_name + '/' + filename):
            img = mpimg.imread(dir_name + '/' + filename)
            img = rgb2gray(img)
            imgs.append(img)
    return imgs


def get_coordinates(imgs, bboxes, format=None, gray=False):
    for i, img in enumerate(imgs):
        bbox = bboxes[i]
        coordinates = get_head_tail_edges(img, bbox)
        # write coordinates of head and tail edges to corresponding files
        # in 'coordinates' directory
        filename = './coordinates/' + str(i).zfill(6) + '.txt'
        with open(filename, 'w') as f:
            for t in coordinates:
                f.write(' '.join(str(s) for s in t) + '\n')
        f.close()
        # visualize detected edges and save png to 'results_images' directory
        image_file = './edge_detected_images/' + str(i).zfill(6) + '.png'
        cv2.imwrite(image_file, img)


    