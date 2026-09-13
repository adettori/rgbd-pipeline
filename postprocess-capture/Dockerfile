FROM ros:humble
ARG USERNAME=ros2user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME
RUN useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Update
RUN apt-get -y update
RUN apt-get update && apt-get upgrade -y

# Install a few important dependencies
RUN apt-get install -y \
    usbutils \
    ament-cmake \
    ccls \
    python3-colcon-common-extensions \
    python3-pip \
    vim \
    clang \
    clang-format \
    clang-tidy \
    ros-humble-turtlesim \
    ros-humble-realsense2-* \
    libxcb-cursor0
    
RUN pip install ros2-unbag \
    pyrealsense2

RUN echo "source /opt/ros/humble/setup.bash" >> /home/$USERNAME/.bashrc
ENV SHELL=/bin/bash
ENV PATH="$PATH:/home/ros2user/.local/bin"

WORKDIR /app

RUN ln -s /bin/python3 /bin/python

# Set the default user
USER $USERNAME

COPY postprocess.py .

CMD ["/bin/bash"]