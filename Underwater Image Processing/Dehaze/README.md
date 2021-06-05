## Dehazing
Dehaze the underwater images with haze using the idea of "dark channel prior" proposed by [He. at el].


Explanations:

dehaze.py: first dehaze the images, then brighten them, since this dehazing algorithm will make the images darker.

`dehaze/`: original images after dehazing

`brighten/`: haze-free images after brightening

Note: before running the program, feel free to remove all the images in `dehaze/` or `brighten/` if you want to see your own results.


How to run the program:

In current directory, run `python3 dehaze_brighten.py`, then the haze-free images and brightened images will be generated in `dehaze/` and `brighten/`, seperately.
