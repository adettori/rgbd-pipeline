#! /bin/bash
# Run depth estimation model
docker run --rm --runtime=nvidia -v ${DATASET}:/app/input --user ${uid}:${gid} depth-estimation-video:latest
# Run mask generation model
docker run --rm --runtime=nvidia -e MASK_PROMPT="${MASK_PROMPT}" -v ./rgbd-pipeline/mask-generation/XMem:/app/XMem -v ${DATASET_DIR}:/app/input --user ${uid}:${gid} mask-generation:latest