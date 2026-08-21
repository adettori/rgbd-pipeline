# rgbd-pipeline
Utilities to process stereoscopic and monocular videos into a rgbd format for ML applications

The expected folder structure for the output is the following:
- object root folder:
    - rgb: contains base image with color
    - depth: contains depth map of corresponding rgb image (same name)
        - Integer representation of metric depth (in millimeters) of the object, represented using uint16
    - masks: contains the mask map of corresponding image (same name)
        - Binary representation of object boundaries, represented using uint8, with 255 (white) representing the object and 0 (black) everything else

## Step 0: process MP4
Run the following command to extract frames from a given mp4 video:
```
ffmpeg -i file_name.mp4 -vf fps=20 frame_%04d.png
```
This example command will result in extracting 20 frames from each second of the video.
Move the resulting images into the `rgb` folder.

## Step 1: depth estimation
```
docker build -t depth-estimation rgbd-pipeline/depth-estimation
docker run --rm --runtime=nvidia -v OBJECT_ROOT_HERE:/app/input depth-estimation:latest 
```

## Step 2: mask generation
```
docker build -t mask-generation rgbd-pipeline/mask-generation
docker run --rm --runtime=nvidia -v OBJECT_ROOT_HERE:/app/input mask-generation:latest
```