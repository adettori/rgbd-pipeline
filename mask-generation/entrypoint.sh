#!/bin/bash
# ENVS needed: 
#     MASK_PROMPT: prompt describing initial object to mask

if [[ -z "${MASK_PROMPT}" ]]; then
  echo "MASK_PROMPT env not set, exiting..."
  exit 1
fi

# Download models if needed
if [ ! -f "/app/XMem/saves/XMem-s012.pth" ]; then
  cd /app/XMem && bash ./scripts/download_models.sh
fi

# delete dataset folder if already present
if [ -d "./dataset" ]; then
  rm -r ./dataset
fi

# Create dirs to store inputs according to XMem dir structure
mkdir -p ./dataset/JPEGImages/object
mkdir -p ./dataset/Annotations//object
mkdir -p ./input/masks # Note that docker needs to map the dataset folder to 

cp ./input/rgb/* dataset/JPEGImages/object

# Run mask generation to obtain initial mask for XMem
python3 ./mask-generation.py

# Run XMem to produce video-consistent masks
python3 XMem/eval.py --dataset G --generic_path dataset/ --output ./dataset/masks --model XMem/saves/XMem-s012.pth

# Mv masks from subfolder to final destination
mv ./dataset/masks/object/* ./input/masks/