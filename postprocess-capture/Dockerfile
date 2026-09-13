FROM librealsense/librealsense

RUN apt-get update -y && apt-get install -y \
    python3-pip \
    libxcb-cursor0 \
    libgl1

RUN pip install pyrealsense2 opencv-python

WORKDIR /app

COPY postprocess.py .

RUN ln -s /bin/python3 /bin/python

# Shows a list of connected Realsense devices
CMD [ "/bin/bash"]