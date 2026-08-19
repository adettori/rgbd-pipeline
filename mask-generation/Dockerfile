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

# Install requirements
RUN pip install torch==2.13.0 --index-url https://download.pytorch.org/whl/cu126
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Cache model
RUN python -c "from transformers import AutoModelForCausalLM; AutoModelForCausalLM.from_pretrained('tiiuae/falcon-perception', trust_remote_code=True)"

# Copy main script
COPY mask-generation.py /app

CMD ["python3", "/app/mask-generation.py"]