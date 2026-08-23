#! /bin/bash
# Setup dirs
mkdir -p ${DATASET}/rgbd-video
mkdir -p ${DATASET}/rgb
mkdir -p ${DATASET}/depth

# Run depth estimation model
docker run --rm --runtime=nvidia -v ${DATASET}:/app/input --user ${uid}:${gid} depth-estimation-video:latest
# Extract frames from depth video and original video
ffmpeg -i ${DATASET}/rgbd-video/video_src.mp4 -vf fps=20 ${DATASET}/rgb/frame_%04d.png
ffmpeg -i ${DATASET}/rgbd-video/video_vis.mp4 -vf format=gray,fps=20 ${DATASET}/depth/frame_%04d.png
# Run mask generation model
docker run --rm --runtime=nvidia -e MASK_PROMPT="${OBJECT_PROMPT}" -v ${DATASET}:/app/input --user ${uid}:${gid} mask-generation:latest