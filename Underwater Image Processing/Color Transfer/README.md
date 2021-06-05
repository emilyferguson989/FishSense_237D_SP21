## Color Transfer
Given a bunch of source images and a target image, transfer the source images to the same color style as the target one using the idea proposed by [Reinhard. at el].


Explanations:

target.png: target image

color_transfer.py: do the transformation as mentioned above

`blue/`: original images that was totally blue

`green/`: original images that was totally green

`blue_trans/`: transferred images from `blue/`

`green_trans/`: transferred images from `green/`

Note: before running the program, feel free to remove all the images in `blue_trans/` or `green_trans/` if you want to see your own results.


How to run the program:

In current directory, run `python3 color_transfer.py`, then the transferred images from `blue/` and `green/` will be generated in `blue_trans/` and `green_trans/`, seperately.

Note: 
1. all images from `blue/` and `green/` are from https://github.com/IPNUISTlegal/underwater-test-dataset-U45-/tree/master/upload/U45, while the target.png is from https://sites.google.com/view/reside-dehaze-datasets.
2. Reference paper: Color Transfer between Images, Erik Reinhard, Michael Ashikhmin, Bruce Gooch, and Peter Shirley, September/October 2001, 0272-1716/01/$10.00 © 2001 IEEE


