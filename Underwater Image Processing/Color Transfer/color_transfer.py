import cv2 as cv
import numpy as np
import glob

# read in target image
target = cv.imread("target.png")
cv.imshow("target", target)

# convert from BGR to LAB
tc = cv.cvtColor(target, cv.COLOR_BGR2LAB)

# get mean and standard derivation
t_mean, t_std = cv.meanStdDev(tc)

    
# read in source images
images = glob.glob('blue/*.png')
images = images+glob.glob('green/*.png')
for fname in images:
    source = cv.imread(fname)

    # convert from BGR to LAB
    sc = cv.cvtColor(source, cv.COLOR_BGR2LAB)

    # get mean and standard derivation
    s_mean, s_std = cv.meanStdDev(sc)

    # convert shape from 3*1 to source.shape*3
    s_mean_trans = np.ones_like(source)+0.0
    s_std_trans = np.ones_like(source)+0.0
    t_mean_trans = np.ones_like(source)+0.0
    t_std_trans =  np.ones_like(source)+0.0
    for i in range (source.shape[2]):
        s_mean_trans[:, :, i] *= s_mean[i, 0]
        s_std_trans[:, :, i] *= s_std[i, 0]
        t_mean_trans[:, :, i] *= t_mean[i, 0]
        t_std_trans[:, :, i] *= t_std[i, 0]
    
    # color transfer
    rt = (sc-s_mean_trans)*(t_std_trans/s_std_trans)+t_mean_trans
    # edge cases
    rt[np.where(rt < 0)] = 0
    rt[np.where(rt > 255)] = 255

    # convert from LAB back to BGR
    result = cv.cvtColor(cv.convertScaleAbs(rt), cv.COLOR_LAB2BGR)
    if fname.split("/")[0] == "green":
        cv.imwrite("green_trans/"+fname.split("/")[1].split(".")[0]+"_trans.png", result)
    elif fname.split("/")[0] == "blue":
        cv.imwrite("blue_trans/"+fname.split("/")[1].split(".")[0]+"_trans.png", result)

    # show the original image and the converted images
    imgs = np.hstack((source, result))
    cv.imshow("source, result", imgs)
    cv.waitKey(500)

cv.destroyAllWindows()
