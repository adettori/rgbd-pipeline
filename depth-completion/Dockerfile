FROM pytorch/pytorch:2.13.0-cuda12.6-cudnn9-devel

ENV CUDA_HOME="/usr/local/cuda-12.6"

RUN apt update -y && apt install -y \
    python3.12-venv \
    git

WORKDIR /app

# Setup venv to avoid issues with system deps
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install conda and update the PATH environment variable
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
RUN bash /tmp/miniconda.sh -b -p /opt/miniconda
ENV PATH=/opt/miniconda/bin:$PATH
RUN rm /tmp/miniconda.sh
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# Install DepthLab dependencies
WORKDIR /app
COPY ./DepthLab/environment.yaml .
RUN conda env create -f ./environment.yaml

# Make RUN commands use the conda environment
SHELL ["conda", "run", "-n", "DepthLab", "/bin/bash", "-c"]

# Install hf cmd utility
RUN pip install huggingface-hub

# Copy scripts
COPY ./entrypoint.sh .
COPY ./convert_image_npy.py .
COPY ./convert_npy_image.py .

CMD ["bash", "./entrypoint.sh"]