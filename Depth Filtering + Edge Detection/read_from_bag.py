# https://leetcode.com/problems/max-area-of-island/discuss/491213/Easy-Python-DFS-Solution

import argparse
from typing import List
import pyrealsense2 as rs
import numpy as np
import cv2
import os
import copy
import sys
 
sys.setrecursionlimit(10**6)

def maxAreaOfIsland(grid) -> int:
    grid_copy = copy.deepcopy(grid) 
    area,count = 0,0

    def dfs(i,j):
        nonlocal count 
        if i >= len(grid_copy) or i < 0 or j >= len(grid_copy[0]) or j < 0 or grid_copy[i][j] != 1:
            return count
        if grid_copy[i][j] == 1:
            count += 1
        grid_copy[i][j] = -1
        dfs(i+1,j)
        dfs(i-1,j)
        dfs(i,j-1)
        dfs(i,j+1)

    for i in range(len(grid_copy)):
        for j in range(len(grid_copy[0])):
            dfs(i,j)
            area = max(count,area)
            count = 0
    return area

def main():

    # test_arr = [[0,0,0,0],
    #             [180,0,210,80],
    #             [190,0,0,0],
    #             [20,0,0,0]]
    # for i in range(len(test_arr)):
    #     for j in range(len(test_arr[0])):
    #         if test_arr[i][j] > 150 and test_arr[i][j] < 200:
    #             test_arr[i][j] = 1
    #         else:
    #             test_arr[i][j] = 200
    # print("area: ", maxAreaOfIsland(test_arr))
    # print(test_arr)
    # print(maxAreaOfIsland(test_arr))


    if not os.path.exists(args.directory):
        os.mkdir(args.directory)
    try:
        config = rs.config()
        rs.config.enable_device_from_file(config, args.input)
        pipeline = rs.pipeline()
        config.enable_stream(rs.stream.depth, rs.format.z16, 30)
        # config.enable_stream(rs.stream.color, rs.format.bgr8, 30)
        pipeline.start(config)
        i = 0
        while True:
            print("Saving frame:", i)
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            depth_array = np.asanyarray(depth_frame.get_data())
            print(depth_array[300][386], depth_array[337][411])
            for x in range(len(depth_array)):
                for y in range(len(depth_array[0])):
                    # within bounding box and depth threshold
                    if depth_array[x][y] > 570 and depth_array[x][y] < 800 and x > 200 and x < 340 and y > 200 and y < 800:
                        depth_array[x][y] = 1
                    else:
                        depth_array[x][y] = 200
            print(maxAreaOfIsland(depth_array))
            depth_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_array, alpha=255/depth_array.max()), cv2.COLORMAP_RAINBOW)
            cv2.imwrite(args.directory + "/" + str(i).zfill(6) + ".png", cv2.cvtColor(depth_image, cv2.COLOR_RGB2BGR))
            i += 1
    finally:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, help="Path to save the images")
    parser.add_argument("-i", "--input", type=str, help="Bag file to read")
    args = parser.parse_args()

    main()