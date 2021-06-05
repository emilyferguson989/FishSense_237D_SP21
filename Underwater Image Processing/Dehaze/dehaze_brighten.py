import cv2 as cv
import numpy as np
import glob

# reference from Rachel Zhang
# percent = under_50/total
# percent < 0.1%, w = 0.8
# 0.1% < percent < 1%, w = 0.6
# 1% < percent < 2%, w = 0.4
# else: not use haze-free-adjust
w0 = 0.8
t0 = 0.1

images = glob.glob('*.png')
for fname in images:
    img = cv.imread(fname)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #cv.imshow("original image", img)
    #cv.imshow("original gray image", img_gray)

    ## dehazing ##
    # histogram for the gray image
    # x-axis(index): grayscale, 0~255
    # y-axis(array value): frequency
    # hist.shape = (256, )
    hist = np.zeros(256)
    for i in range (img_gray.shape[0]):
        for j in range (img_gray.shape[1]):
            hist[img_gray[i][j]] += 1

    # calculate the percentage of grayscale under 50
    under_50 = 0
    for i in range (50):
        under_50 += hist[i]
    total = img.shape[0]*img.shape[1]*img.shape[2]
    percent = under_50/total

    try:
        if percent > 0.01 and percent <= 0.02:
            w0 = 0.4
        elif percent > 0.001 and percent <= 0.01:
            w0 = 0.6
        #elif percent <= 0.001: w0 = 0.6 default
    except percent > 0.02:
        print("no need to do haze-free-adjustment")
        raise

    # get the minimum grayscale value of each pixel for all channels
    min_img = np.zeros_like(img_gray)+0.0
    for i in range (img_gray.shape[0]):
        for j in range (img_gray.shape[1]):
            min_img[i, j] = np.min(img[i, j, :])

    # see the definition of dark_channel from the paper
    dark_channel = np.max(min_img)+0.0
    t = 1-w0*(min_img/dark_channel)

    # compare each value in t with t0, choose the maximum one
    t[np.where(t <= t0)] = t0

    img_d = img+0.0
    img_dehazed = np.zeros_like(img)
    for i in range (img.shape[2]):
        img_dehazed[:, :, i] = (img_d[:, :, i]-dark_channel)/t+dark_channel

    #cv.imshow("dehazed image", img_dehazed)
    #img_dehazed_gray = cv.cvtColor(img_dehazed, cv.COLOR_BGR2GRAY)
    #cv.imshow("dehazed image gray", img_dehazed_gray)

    cv.imwrite("./dehaze/"+fname.split(".")[0]+"_dehazed.png", img_dehazed)
    
    ## brighten ##
    blank_img = np.zeros_like(img)
    c = 1.5
    b = 3
    img_brightened = cv.addWeighted(img_dehazed, c, blank_img, 1-c, b)
    cv.imwrite("./brighten/"+fname.split(".")[0]+"_brighten.png", img_brightened)

    # show the original image, haze-free image, and the brightened image
    imgs = np.hstack((img, img_dehazed, img_brightened))
    cv.imshow("images", imgs)

    cv.waitKey(200)

cv.destroyAllWindows()


