# FishSense
Studying Fish in their Natual Habitat

## Motivation
Fish are a vital part of our global ecosystem and in order to best protect and preserve them, we must be able to effectively learn about them. We need to not only learn about fish on an individual level, but on a global level too. This can prove difficult, however, as the ocean is their home, not ours! One method that has been used for millennia is to simply go fishing, and analyze characteristics of the fish you catch: species, length, weight, health, location, etc. This invasive method, while accurate, does not capture the full picture. You only are able to report on the fish you catch, and you do not see the interactions between fish, or between fish and their habitat.

Say then you dive underwater to view the fish in the wild. Now you have the opposite problem: fish are not keen on letting you grab them and measure them. Recent advancements in underwater imaging technology such as laser calipers and stereo camera rigs have made measurement a little easier, but they present additional problems. These include being too bulky for divers to efficiently operate, being unable to fully capture interactions between fish or the habitat, or being inaccurate, especially when fish are not lined up perfectly.


## Project Overview
We present FishSense as a solution for capturing all characteristics of fish in their natural habitat. Our ergonomic diver operated handheld system brings cutting edge 3D imaging technology below the surface of the ocean. With this device we are able to directly measure geometric and volumetric information about the fish and their environment directly, without needing to perform expensive and specialized post-processing. The extra dimension in the data will also improve AI models for fish detection and classification, which will allow fisheries’ research to scale up dramatically.

In this quarter, we have focused on automating the fish length measurement process to alleviate the cost of catching and measuring fish by hand, one-by-one. We are using an Intel RealSense camera which captures depth images as well as RGB images to capture images of fish underwater. Our contributions include the following:


Setup (Calibration and Alignment of RGB and Depth Images) [1].

| ![Calibration](https://github.com/emilyferguson989/FishSense_237D_SP21/tree/main/images/calibration_method.png) |
| :---: |
| Method Used to Calibrate Intel RealSense Camera |

| ![RGB Depth Alignment](https://github.com/emilyferguson989/FishSense_237D_SP21/tree/main/images/rgb_depth_alignment_demo.png) |
| :---: |
| Demonstration of the Alignment of RGB and Depth Images |

Developing a Fish Length Detection Algorithm for this Context [2].

| ![Length Detection Algorithm](https://github.com/emilyferguson989/FishSense_237D_SP21/tree/main/images/length_detection_algorithm_demo.png) |
| :---: |
| Fish Length Detection Algorithm Demonstration |

Denoising Underwater Images [3].

| ![Denoising (Demo to come)](https://path_to_image) |
| :---: |
| Overview of the Underwater Image  Noise Filtering Process |

Calculating the Length of Fish Given Underwater Images [2].

| ![Underwater Length Detection (Demo to Come)](https://path_to_image) |
| :---: |
| Results of Calculating the Length of Fish in Underwater Images |

## Team Members
- Xilin Gao

- Zixiang Zhou

- Emily Ferguson

## Project Milestones and Schedule



## Repository Organization
### Files
align-p2p.cpp: Alignment of RGB and depth images

data_manipulation.cpp: Length measurement algorithm

### Installation
1. Run `git clone https://github.com/{our_repo}`
2. Change directory `cd {repo name}/`
3. ...

## Learn More About Our Contributions
[Final Video (coming soon)]()

[Final Report (coming soon)]()

[Final Presentation Slides (coming soon)]()

## Learn More About the FishSense Project
[FishSense Website](http://e4e.ucsd.edu/fishsense)
