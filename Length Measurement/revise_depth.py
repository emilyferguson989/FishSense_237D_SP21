import csv
import cv2 as cv
import numpy as np

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
    
    depth = []

    # read in depth image
    with open("./color_depth_data/"+str(index)+".csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for row in csv_reader:
            depth.append(row)

    # change from list of string to array of float
    depth_arr = np.zeros((len(depth), len(depth[0])))+0.0
    for i in range (len(depth)):
        for j in range (len(depth[0])):
            depth_arr[i][j] = float(depth[i][j])

    # fill in the blank of some un-mapped points        
    for i in range (1, len(depth)-1):
        for j in range (1, len(depth[0])-1):
            if depth_arr[i-1][j] and depth_arr[i+1][j] and depth_arr[i][j-1] and depth_arr[i][j+1] and depth_arr[i][j] == 0:
                depth_arr[i][j] = np.mean((depth_arr[i-1][j], depth_arr[i+1][j], depth_arr[i][j-1], depth_arr[i][j+1]))
                #print(i, j, depth_arr[i][j])
            elif depth_arr[i-1][j] and depth_arr[i+1][j] and depth_arr[i][j] == 0:
                depth_arr[i][j] = np.mean((depth_arr[i-1][j], depth_arr[i+1][j]))
                #print(i, j, depth_arr[i][j])
            elif depth_arr[i][j-1] and depth_arr[i][j+1] and depth_arr[i][j] == 0:
                depth_arr[i][j] = np.mean((depth_arr[i][j-1], depth_arr[i][j+1]))
                #print(i, j, depth_arr[i][j])

    #print(index)
            
            
    # save mean points for head and tail
    with open("./color_depth_data/"+str(index)+"_r.csv", mode = 'w') as csv_file:
        writer = csv.writer(csv_file)
        for row in depth_arr:
            writer.writerow(row)
