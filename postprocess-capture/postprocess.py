## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 RealSense, Inc. All Rights Reserved.

#####################################################
##              Align Depth to Color               ##
#####################################################

import os, argparse
# First import the library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2

def setup(out_path):
    list_dirs = [f"{out_path}/rgb", f"{out_path}/depth"]

    for dir in list_dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

def run(args):
    # Create a pipeline
    pipeline = rs.pipeline()

    # Create a config and configure the pipeline to stream
    #  different resolutions of color and depth streams
    config = rs.config()

    config.enable_device_from_file(args.input_bag, repeat_playback=False)

    # Start streaming
    profile = pipeline.start(config)

    # Getting the depth sensor's depth scale (see rs-align example for explanation)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    print("Depth Scale is: " , depth_scale)

    # We will be removing the background of objects more than
    #  clipping_distance_in_meters meters away
    clipping_distance_in_meters = 1.5 #1 meter
    clipping_distance = clipping_distance_in_meters / depth_scale

    # Create an align object
    # rs.align allows us to perform alignment of depth frames to others frames
    # The "align_to" is the stream type to which we plan to align depth frames.
    align_to = rs.stream.color
    align = rs.align(align_to)

    # Instance of filters
    hole_filling = rs.hole_filling_filter()
    hole_filling.set_option(rs.option.holes_fill, 2) # nearest value from around
    temporal_filter = rs.temporal_filter()
    spatial_filter = rs.spatial_filter()

    # Keep track of current frame
    frame_id = 0

    # Streaming loop
    try:
        while True:
            # Get frameset of color and depth
            frames = pipeline.wait_for_frames()
            # frames.get_depth_frame() is a 640x360 depth image

            # Align the depth frame to color frame
            aligned_frames = align.process(frames)

            # Get aligned frames
            aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
            color_frame = aligned_frames.get_color_frame()

            # Validate that both frames are valid
            if not aligned_depth_frame or not color_frame:
                continue

            # Fill holes in depth map
            filled_depth_frame = hole_filling.process(aligned_depth_frame)

            # Apply temporal filter
            temporal_depth_frame = temporal_filter.process(filled_depth_frame)

            # Apply spatial filter
            spatial_depth_frame = spatial_filter.process(temporal_depth_frame)

            depth_image = np.asanyarray(spatial_depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Remove background - Set pixels further than clipping_distance to grey
            bg_color= 2000
            depth_bg_removed = np.where((depth_image > clipping_distance) | (depth_image <= 0), bg_color, depth_image)

            image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

            cv2.imwrite(f"{args.dst_base_dir}/rgb/{frame_id:04d}.png", image_rgb)
            cv2.imwrite(f"{args.dst_base_dir}/depth/{frame_id:04d}.png", depth_bg_removed)

            frame_id += 1
    except RuntimeError:
        print("Reached the end of the .bag file.")
    finally:
        pipeline.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process an input bag file and save to a destination path."
    )

    # Positional arguments
    _ = parser.add_argument(
        "input_bag", type=str, help="Path to the input bag file"
    )
    _ = parser.add_argument(
        "dst_base_dir", type=str, help="Destination directory or path for output"
    )

    args = parser.parse_args()

    setup(args.dst_base_dir)
    run(args)