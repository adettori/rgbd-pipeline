#! /bin/bash

BAG_DIR=./
BAG_NAME="bag.db3"
DATASET_DIR=bag_output
MASK_PROMPT="black box near hands"

mkdir -p $DATASET_DIR
docker run --rm --runtime=nvidia -v $BAG_DIR:/app/input -e BAG_NAME="$BAG_NAME" -e DATASET_DIR="$DATASET_DIR" --user ${uid}:${gid} postprocess-capture:latest bash -c "python /app/postprocess.py /app/input/$BAG_NAME /app/input/$DATASET_DIR"
docker run --rm --runtime=nvidia -v $DATASET_DIR:/app/input -e MASK_PROMPT="$MASK_PROMPT" -v ./rgbd-pipeline/mask-generation/XMem:/app/XMem --user ${uid}:${gid} mask-generation:latest
