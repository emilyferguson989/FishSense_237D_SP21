import cv2 as cv
import numpy as np
import csv
import os

# delete the original mean points info since this file is of mode 'a'
# to avoid appending
if os.path.exists("mean_points.txt"):
    os.remove("mean_points.txt")

for index in range (106):
    # skip these images because they are too close to the camera
    # so their depth vales are mostly 0 and thus useless
    # skip the image(s) that cannot be detected by the ML pipeline
    if index == 0:
        continue
    if index == 11:
        continue
    if index >= 46 and index <= 66:
        continue
    if index == 71 or index == 72:
        continue
    if index >= 99 and index <= 104:
        continue

    # bounding box
    vertices = []
    with open("./bbox_data/"+str(index)+".txt") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ' ')
        for row in csv_reader:
            vertices = row
    #print(vertices)

    # string to int
    bbox = np.ones((4,), dtype = int)
    for i in range (4):
        bbox[i] = int(float(vertices[i]))
    #print(bbox)

    # set range for bbox
    left_top_j = bbox[0]
    left_top_i = bbox[1]
    right_bottom_j = bbox[2]
    right_bottom_i = bbox[3]
    #print(left_top_j, left_top_i, right_bottom_j, right_bottom_i)

    # read in color image
    color = cv.imread("./color_depth_data/"+str(index)+".png")

    # roi region and rectangle
    rect = (left_top_j, left_top_i, right_bottom_j-left_top_j, right_bottom_i-left_top_i)
    roi = color[left_top_i:right_bottom_i, left_top_j:right_bottom_j, :]

    # original image mask
    mask = np.zeros(color.shape[:2], dtype = np.uint8)

    # initial foregroung and background models
    bgdmodel = np.zeros((1, 65), np.float64)
    fgdmodel = np.zeros((1, 65), np.float64)

    # grabcut algorithm
    cv.grabCut(color, mask, rect, bgdmodel, fgdmodel, 5, mode = cv.GC_INIT_WITH_RECT)

    # grab foreground and possible foreground region
    mask2 = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')

    # take only region of fish from fish image
    result = cv.bitwise_and(color, color, mask = mask2)
    result_gray = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
    cv.imshow('roi', roi)
    cv.imshow("result", result)

    # read in depth image
    depth = []
    with open("./color_depth_data/"+str(index)+"_r.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for row in csv_reader:
            depth.append(row)

    # change from list of string to array of float
    depth_arr = np.zeros((color.shape[0], color.shape[1]))+0.0
    for i in range (color.shape[0]):
        for j in range (color.shape[1]):
            depth_arr[i][j] = float(depth[i][j])

    # choose points from head and tail, separately
    head = []
    for j in range (left_top_j, left_top_j+18):
        for i in range (result.shape[0]):
            if result_gray[i][j] != 0 and depth_arr[i][j] != 0:
                head.append((i, j, depth_arr[i][j]))
    head_mean = np.mean(head, axis = 0)

    tail = []
    for j in range (right_bottom_j, right_bottom_j-18, -1):
        for i in range (result.shape[0]):
            if result_gray[i][j] != 0 and depth_arr[i][j] != 0:
                tail.append((i, j, depth_arr[i][j]))
    tail_mean = np.mean(tail, axis = 0)

    #print(head_mean)
    #print(tail_mean)

    # write back the mean points
    f = open("mean_points.txt", 'a')
    f.write(str(index)+":"+str(head_mean[0])+","+str(head_mean[1])+","+str(head_mean[2])+","+str(tail_mean[0])+","+str(tail_mean[1])+","+str(tail_mean[2])+"\n")

    cv.waitKey(200)

cv.destroyAllWindows()
