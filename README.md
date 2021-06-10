# FishSense
Studying Fish in their Natual Habitat

## Motivation
Fish are a vital part of our global ecosystem and in order to best protect and preserve them, we must be able to effectively learn about them. We need to not only learn about fish on an individual level, but on a global level too. This can prove difficult, however, as the ocean is their home, not ours! One method that has been used for millennia is to simply go fishing, and analyze characteristics of the fish you catch: species, length, weight, health, location, etc. This invasive method, while accurate, does not capture the full picture. You only are able to report on the fish you catch, and you do not see the interactions between fish, or between fish and their habitat.

Say then you dive underwater to view the fish in the wild. Now you have the opposite problem: fish are not keen on letting you grab them and measure them. Recent advancements in underwater imaging technology such as laser calipers and stereo camera rigs have made measurement a little easier, but they present additional problems. These include being too bulky for divers to efficiently operate, being unable to fully capture interactions between fish or the habitat, or being inaccurate, especially when fish are not lined up perfectly.


## Project Overview
We present FishSense as a solution for capturing all characteristics of fish in their natural habitat. Our ergonomic diver operated handheld system brings cutting edge 3D imaging technology below the surface of the ocean. With this device we are able to directly measure geometric and volumetric information about the fish and their environment directly, without needing to perform expensive and specialized post-processing. The extra dimension in the data will also improve AI models for fish detection and classification, which will allow fisheries’ research to scale up dramatically.

In this quarter, we have focused on automating the fish length measurement process to alleviate the cost of catching and measuring fish by hand, one-by-one. We are using an Intel RealSense camera which captures depth images as well as RGB images to capture images of fish underwater. Our contributions include the following:


### Setup (Calibration and Alignment of RGB and Depth Images) [1].

| Calibration             |  RGB Depth Alignment |
:-------------------------:|:-------------------------:
<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/calibration_method.png" width=400>  |  <img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/rgb_depth_alignment_demo.png" width=400>

### Developing a Fish Length Detection Algorithm for this Context [2].

| ![Length Detection Algorithm](https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/length_detection_algorithm_demo.png) |
| :---: |
| Fish Length Detection Algorithm Demonstration |

### Denoising Underwater Images [3].

| ![Denoising (Fusion)](https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/Fusion_Output.png) |
| :---: |
| Overview of the Underwater Image Using Fusion to Denoise |


| Before Removal of Backscatters             |  After Removal of Backscatters |
:-------------------------:|:-------------------------:
<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/org-3.png" width=400>  |<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/enh-3.png" width=400>


| Before Gaussian Blur + Canny Edge Detection             |  After Gaussian Blur + Canny Edge Detection |
:-------------------------:|:-------------------------:
<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/may_15.jpg" width=400>  |<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/may_15_edge_detection.png" width=400>

| Before Noise Filtration             |  CLAHE                   |  HE              |       ICM             |    RGHS             |
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/before noise filtration.png" width=160>  |<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/CLAHE.jpg" width=160>  |<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/HE.jpg" width=160>   |<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/ICM.jpg" width=160>   |<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/RGHS.jpg" width=160>

| Before Dehazing             |  After Dehazing |
:-------------------------:|:-------------------------:
<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/img_haze.png" width=400>  |<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/img_haze_free.png" width=400>

| Before Transferring             |  Target                   |  After Transferring |         
:-------------------------:|:-------------------------:|:-------------------------:
<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/before transfer.png" width=266>  |<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/target.png" width=266>  |<img src="https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/images/after transfer.png" width=266>

### Head and Tail Coordinate Detection [5].
[Coordinate Edge Detection (Demo)](https://drive.google.com/file/d/1oiDrLLz70NtVc4AjmGsEZQQApX-Uol-S/view?usp=sharing)

### Calculating the Length of Fish in Air [4].

[Underwater Length Detection (Demo)](https://drive.google.com/file/d/1RAAKjmvraCTCtuozXDL0KcUBxqVNtvJx/view?usp=sharing)

## Team Members
- Xilin Gao

- Zixiang Zhou

- Emily Ferguson

## Project Milestones and Schedule

[Schedule](https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/237D%20Documents/FishSense%20Milestones%20and%20Schedule.pdf)

## Repository Organization
### Files

`237D Documents/` Required documents regarding the project submitted for 237D assignments

`Length Measurement/` Code used to setup the system as well as perform length calculations

`Underwater Image Processing/` Code used to do underwater image processing to help with further detection

`images/` Images used to demonstrate the project

`Depth Filtering + Edge Detection/` Code used to perform depth filtering and detect the edges of the heads and tails of fish

### Installation
0. Install the realsense library following the instructions from Intel realsense: https://github.com/IntelRealSense/librealsense
1. Install OpenCV from its official website: https://docs.opencv.org/master/df/d65/tutorial_table_of_content_introduction.html
2. Setup the realsense camera with proper USB (e.g. USB 3.0 for D455)
3. Run `git clone https://github.com/emilyferguson989/FishSense_237D_SP21.git`
4. Change directory `cd FishSense_237D_SP21/`

## Learn More About Our Contributions
[Final Video (coming soon)]()

[Final Report](https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/237D%20Documents/FishSense%20Final%20report.pdf)

[Final Presentation Slides](https://github.com/emilyferguson989/FishSense_237D_SP21/blob/main/237D%20Documents/FishSense%20Final%20Oral%20Presentation.pdf)

## Learn More About the FishSense Project
[FishSense Website](http://e4e.ucsd.edu/fishsense)
