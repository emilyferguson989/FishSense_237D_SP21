## Color Transfer
Given a bunch of source images and a target image, transfer the source images to the same color style as the target one using the idea proposed by [Reinhard. at el].


Explanations:

color_transfer.py: do the transformation as mentioned above

`blue/`: original images that was totally blue

`green/`: original images that was totally green

`blue_trans/`: transferred images from `blue/`

`green_trans/`: transferred images from `green/`

Note: before running the program, feel free to remove all the images in `blue_trans/` or `green_trans/` if you want to see your own results.


How to run the program:

In current directory, run `python3 color_transfer.py`, then the transferred images from `blue/` and `green/` will be generated in `blue_trans/` and `green_trans/`, seperately.

