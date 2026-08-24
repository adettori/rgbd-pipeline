FROM pytorch/pytorch:2.13.0-cuda12.6-cudnn9-devel

ENV CUDA_HOME="/usr/local/cuda-12.6"

RUN apt update -y && apt install -y \
    python3.12-venv \
    git \
    ffmpeg

WORKDIR /app

# Setup venv to avoid issues with system deps
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install VDA dependencies
RUN git clone https://github.com/adettori/Video-Depth-Anything
WORKDIR /app/Video-Depth-Anything
RUN pip install -U torch==2.6.0 torchvision==0.21.0 xformers --index-url https://download.pytorch.org/whl/cu126
RUN pip install --no-build-isolation setuptools \
    numpy==1.26.4 \
    opencv-python \
    matplotlib==3.7.3 \
    pillow \
    imageio==2.37.0 \
    imageio-ffmpeg==0.4.7 \
    decord \
    einops==0.4.1 \
    easydict \
    tqdm \
    OpenEXR==3.3.1 \
    triton \
    open3d==0.19.0

# Download model's weights
RUN mkdir checkpoints && \
    cd checkpoints && \
    wget https://huggingface.co/depth-anything/Metric-Video-Depth-Anything-Base/resolve/main/metric_video_depth_anything_vitb.pth && \
    echo "f6f58576b9680a112f2428d4f39aff92656d3ae85745b0164675ace8d5b1fade metric_video_depth_anything_vitb.pth" > SHA256SUMS && \
    sha256sum -c SHA256SUMS

RUN useradd -ms /bin/bash tmp_user
USER tmp_user

CMD ["python3", "run.py", "--input_video", "/app/input/video.mp4", "--output_dir", "/app/input/rgbd-video", "--encoder", "vitb", "--metric"]