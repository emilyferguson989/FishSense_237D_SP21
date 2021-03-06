## How to use this subdirectory

#### ** Note: This code deals only with depth images

#### depth_bbox (bounding box coordinate .txt files):
The code requires the coordinates of a bounding box around the entire fish. Place bounding box coordinate .txt files inside of the 'depth_bbox/' directory.
The format required for the bounding box coordinates is the following (each coordinate integer should be on its own line):

Line 1: lower x coordinate

Line 2: lower y coordinate

Line 3: upper x coordinate

Line 4: upper y coordinate


See the following image for reference, and see examples of the format for the bounding box coordinate .txt files in the depth_bbox directory.

<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/example_coordinates.PNG" width=400>

#### depth_csv (csv files holding depth data):
** Please make sure that the name of the csv file is the same as the name of the depth file other than the file extensions.
For example:
my_depth_csv.csv (csv depth data)
my_depth_bbox.txt (bounding box coordinates)
or
1.csv (csv depth data)
1.txt (bounding box coordinates)

### Instructions to run the code:
0. Install required packages per import statements
1. Run 'python3 ./depth_filter_edge_detection.py'

### Results of the code:
1. The resulting depth filtered images will be saved to the 'depth_filtered_images/' directory
2. The resulting edge detected images will be saved to the 'edge_detected_images/' directory
3. The resulting edge coordinates for the edges of the head and the tail of the fish will be saved as (x, y) pairs to the 'coordinates/' directory. 

(The first half of the coordinates saved are for the head, the second half are for the tail)

For example, if the following were the contents of a coordinates file,

(2,3)

(4,5)

(10,20)

(12, 21)

Then (2, 3) and (4, 5) would be along the edge for the head, and (10, 20) and (12, 21) would be along the edge for the tail.

### Reading from .bag file instead of local depth .csv files:
read_from_bag.py includes code for reading depth information from a bag file rather than using local depth .csv files
