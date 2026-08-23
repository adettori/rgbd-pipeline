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

# Install Apple's ml-depth-pro depth estimation method
RUN git clone https://github.com/apple/ml-depth-pro
RUN pip install -e /app/ml-depth-pro

# Download model's weights
RUN pip install huggingface-hub 
RUN mkdir -p apple/DepthPro
RUN hf download --local-dir checkpoints apple/DepthPro

# Copy script
COPY depth-estimation.py /app

CMD ["python3", "/app/depth-estimation.py"]