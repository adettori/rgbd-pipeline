#! /bin/bash

# Activate conda
source /opt/miniconda/etc/profile.d/conda.sh DepthLab
conda activate DepthLab

# Prepare models dest folder
mkdir -p ./DepthLab/checkpoints

# Download checkpoints, if needed
if [ ! -d ./DepthLab/checkpoints/marigold-depth-v1-0 ]; then
  huggingface-cli download prs-eth/marigold-depth-v1-0 --local-dir ./DepthLab/checkpoints/marigold-depth-v1-0
fi

if [ ! -d ./DepthLab/checkpoints/CLIP-ViT-H-14-laion2B-s32B-b79K ]; then
  huggingface-cli download laion/CLIP-ViT-H-14-laion2B-s32B-b79K --local-dir ./DepthLab/checkpoints/CLIP-ViT-H-14-laion2B-s32B-b79K
fi

if [ ! -d ./DepthLab/checkpoints/DepthLab ]; then
  huggingface-cli download Johanan0528/DepthLab --local-dir ./DepthLab/checkpoints/DepthLab
fi

# Prepare depth inputs for DepthLab
mkdir -p depth_npy
# Convert depth pngs into depth vectors in npy format
DIR_IN_IMAGES="./input/depth" DIR_OUT_NPY="./depth_npy" python3 convert_image_npy.py

# Inference section
pretrained_model_name_or_path='./DepthLab/checkpoints/marigold-depth-v1-0'
image_encoder_path='./DepthLab/checkpoints/CLIP-ViT-H-14-laion2B-s32B-b79K'
denoising_unet_path='./DepthLab/checkpoints/DepthLab/denoising_unet.pth'
reference_unet_path='./DepthLab/checkpoints/DepthLab/reference_unet.pth'
mapping_path='./DepthLab/checkpoints/DepthLab/mapping_layer.pth'

export CUDA_VISIBLE_DEVICES=0

python3 ./DepthLab/infer.py  \
    --seed 1234 \
    --denoise_steps 50 \
    --processing_res 480 \
    --normalize_scale 1 \
    --strength 0.8 \
    --pretrained_model_name_or_path $pretrained_model_name_or_path --image_encoder_path $image_encoder_path \
    --denoising_unet_path $denoising_unet_path \
    --reference_unet_path $reference_unet_path \
    --mapping_path $mapping_path \
    --output_dir '/app/' \
    --input_image_paths ./input/rgb/0000.png \
    --known_depth_paths ./depth_npy/0000.npy \
    --masks_paths ./input/masks/0000.png \
    --refine

# Convert depth data back from numpy to png
mkdir -p ./input/test
DIR_IN_NPY="./depth_npy/" DIR_OUT_IMAGES="./input/test/" python3 convert_npy_image.py 