# rgbd-pipeline
Utilities to process stereoscopic and monocular videos into a rgbd format for ML applications

The expected folder structure for the output is the following:
- rgb: contains base image with color
- depth: contains depth map of corresponding rgb image (same name)
- masks: contains the mask map of corresponding image (same name)

## Step 0: process MP4
Run the following command to extract frames from a given mp4 video:
```
ffmpeg -i file_name.mp4 -vf fps=5 frame_%04d.png
```
This example command will result in extracting 5 frames from each second of the video.
Move the resulting images into the `rgb` folder.