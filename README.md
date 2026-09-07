# rgbd-pipeline
Utilities to process stereoscopic and monocular videos into a rgbd format for ML applications

The expected folder structure for the final output is the following:
- object root folder:
    - rgb: contains base image with color
    - depth: contains depth map of corresponding rgb image (same name)
        - Integer representation of metric depth (in millimeters) of the object, represented using uint16, with higher values representing the object and lower ones everything else
    - masks: contains the mask map of corresponding image (same name)
        - Binary representation of object boundaries, represented using uint8, with 255 (white) representing the object and 0 (black) everything else

The models used are [Video Depth Anything](https://github.com/DepthAnything/Video-Depth-Anything) for depth estimation starting from an mp4 video and mask generation via [tiiuae/falcon-perception](https://github.com/tiiuae/falcon-perception)

## Step 1: build all docker images
```
cd rgbd-pipeline
bash build.sh
```

### Step 1.1: process ROS2 bag (optional)
Use [ros2-unabag](https://github.com/ika-rwth-aachen/ros2_unbag) to extract the rgb and depth frames from the bag, potentially doing resampling of the frames.
If needed invert the depth map values to conform to the expect format outlined above by using the `utils/invert_depth.py` script. Note that it clips depth values to 2000 (mm).

## Step 2: depth estimation + mask generation
```
DATASET=$(pwd)/path/to/dataset OBJECT_PROMPT="description used to mask the object here" bash rgbd-pipeline/run-pipeline.sh
```
The dataset folder should contain a `video.mp4` to process and the results will be written to the rgb, depth and masks.