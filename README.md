# rgbd-pipeline
Utilities to process stereoscopic and monocular videos into a rgbd format for ML applications

The expected folder structure for the output is the following:
- object root folder:
    - rgb: contains base image with color
    - depth: contains depth map of corresponding rgb image (same name)
        - Integer representation of metric depth (in millimeters) of the object, represented using uint16, with higher values representing the object and lower ones everything else
    - masks: contains the mask map of corresponding image (same name)
        - Binary representation of object boundaries, represented using uint8, with 255 (white) representing the object and 0 (black) everything else

The models used are [Video Depth Anything](https://github.com/DepthAnything/Video-Depth-Anything) for depth estimation starting from an mp4 video and mask generation via [tiiuae/falcon-perception](https://github.com/tiiuae/falcon-perception)

## Step 1: build docker images
```
cd rgbd-pipeline
bash build.sh
```

## Step 2: depth estimation + mask generation + implicit frame extraction 
```
DATASET=$(pwd)/path/to/dataset OBJECT_PROMPT="description used to mask the object here" bash rgbd-pipeline/run-pipeline.sh
```
The dataset folder should contain a `video.mp4` to process and the results will be written to the rgb, depth and masks.