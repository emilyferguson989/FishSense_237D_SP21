## Length measurement (in Air)

RGBD alignment and simple length calculation method:

align-p2p.cpp: when the realsense camera is connected to a computer, each time, for a captured frame, do a point-to-point mapping from depth image to color image, then get the color image with its pixel-wise corresponding depth information.

data_manipulation.cpp: given the pixel coordinates and depth data of two points (average head and average tail), and the intrinsic matrix, distortion model & coefficients from the camera, calculate the Euclidean distance between these two points, namely the length of a fish. Save results in length_full.txt (head and tail points in 3D space & fish length) and length_only.txt (indecies with corresponding length)

Makefile: compile for align-p2p.cpp

color_depth_data: RGB images (.png) and corresponding Depth images (.csv). Those csv files with "_r" are generated afterwards, feel free to remove them by typing  `rm *_r.csv` in the terminal under this directory.

bbox_data: RGB images with bounding box (.png) and corresponding coordinate information (.txt). The coordinates of each bounding box is in this format: (xmin, ymin, xmax, ymax). Note here, x is the horizontal axis, and y is the vertical axis.

revise_depth.py: modify the Depth pixel value if some points inside the fish is unmapped. It will generate a new csv file, e.g. new Depth file 1_r.csv for the original Depth file 1.csv.

grabcut.py: get mean points for head and tail, separately. Save results in mean_points.txt, where the format is: "index:i_head,j_head,depth_head,i_tail,j_tail,depth_tail".

run_demo_m.sh: first run grabcut.py, then compile and run data_manipulation.cpp.

length.py: given lengths, plot the values and get mean & standard deviation. Save results as length_info.txt and fish_length_result.png.

Note that this way of calculation also works for underwater, unless we can get the camera matrices and distortion coefficients (and distortion model).


How to run the program:
1) `make`
2) `python3 revise_depth.py`
3) `./run_demo_m.sh`
4) `python3 length.py`
