#! /bin/bash

MASK_PROMPT="black box near hands"
DATASET_DIR=./ref_views/black-aligned

docker run --rm --runtime=nvidia -v $DATASET_DIR:/app/input -e MASK_PROMPT="$MASK_PROMPT" -v ./rgbd-pipeline/mask-generation/XMem:/app/XMem --user ${uid}:${gid} mask-generation:latest

docker run --rm --runtime nvidia -v $DATASET_DIR:/app/input -v ./rgbd-pipeline/depth-completion/DepthLab:/app/DepthLab --user ${uid}:${gid} depth-completion:latest