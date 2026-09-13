# rgbd-pipeline
Utilities to process stereoscopic and monocular videos into a rgbd format for ML applications

The expected folder structure for the final output is the following:
- object root folder:
    - rgb: contains base image with color
    - depth: contains depth map of corresponding rgb image (same name)
        - Integer representation of metric depth (in millimeters) of the object, represented using uint16, with higher values representing the object and lower ones everything else
    - masks: contains the mask map of corresponding image (same name)
        - Binary representation of object boundaries, represented using uint8, with 255 (white) representing the object and 0 (black) everything else

The models used for mask generation are [tiiuae/falcon-perception](https://github.com/tiiuae/falcon-perception) for the initial mask leveraging a text prompt that is then leveraged by [hkchengrex/XMem](https://github.com/hkchengrex/XMem) to consistently mask all frames in the video without further prompting.

## Step 1: build all docker images
```
cd rgbd-pipeline
bash build-pipeline.sh
```

### Step 2: tweak parameters in run-pipeline.sh
Change as needed the parameters listed to refer to the correct paths:
```
BAG_DIR: folder to map inside docker that contains bag
BAG_NAME: name of the bag inside BAG_DIR
DATASET_DIR: name of the subfolder in BAG_DIR where to store results of postprocessing
MASK_PROMPT: prompt used to delimit object to mask in images
```
Note: the pipeline/pyrealsense2 seems to require more topics inside the input bag than just color, depth and info from the RealSense camera. Recording from RS Viewer seems to work better.

## Step 3: process raw pyrealsense2 bag + mask generation
Run the pipeline:
```
bash rgbd-pipeline/run-pipeline.sh
```