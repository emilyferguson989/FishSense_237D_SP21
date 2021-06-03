import numpy as np
from medpy.filter.smoothing import anisotropic_diffusion
import matplotlib.pyplot as plt 

img = np.random.uniform(size=(32,32))
img_filtered = anisotropic_diffusion(img)

plt.figure(figsize=(20, 40))
if img_filtered.shape[0] == 3:
    img_filtered = img_filtered.transpose(1,2,0)
    plt_idx = i+1
    plt.subplot(2, 2, plt_idx)
    plt.imshow(img_filtered, format)
plt.savefig("./mygraph3.png")