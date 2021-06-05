## Dehazing
Dehaze the underwater images with haze using the idea of "dark channel prior" proposed by [He. at el].


Explanations:

dehaze.py: first dehaze the images, then brighten them, since this dehazing algorithm will make the images darker.

`dehaze/`: original images after dehazing

`brighten/`: haze-free images after brightening

Note: before running the program, feel free to remove all the images in `dehaze/` or `brighten/` if you want to see your own results.


How to run the program:

In current directory, run `python3 dehaze_brighten.py`, then the haze-free images and brightened images will be generated in `dehaze/` and `brighten/`, seperately.

Note:
1. all images in current directory are from https://github.com/IPNUISTlegal/underwater-test-dataset-U45-/tree/master/upload/U45/haze.
2. reference paper: Single Image Haze Removal Using Dark Channel Prior, Kaiming He, Jian Sun, Xiaoou Tang, 978-1-4244-3991-1/09/$25.00 ©2009 IEEE
