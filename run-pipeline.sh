#! /bin/bash
# Setup dirs
mkdir -p ${DATASET}/rgb
mkdir -p ${DATASET}/depth
mkdir -p ${DATASET}/masks

# Run depth estimation model
docker run --rm --runtime=nvidia -v ${DATASET}:/app/input --user ${uid}:${gid} depth-estimation-video:latest
# Run mask generation model
docker run --rm --runtime=nvidia -e MASK_PROMPT="${OBJECT_PROMPT}" -v ${DATASET}:/app/input --user ${uid}:${gid} mask-generation:latest