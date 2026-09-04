from PIL import Image
import numpy as np
import os, sys, logging

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout)) # defaults to sys.stderr

def invert_depth(in_path, out_path):
    # Load and preprocess an image.
    image = Image.open(in_path)
    image_arr = np.asarray(image).astype("int32")

    depth = (image_arr - image_arr.max()) * (-1) # Flip values so that the objects near the sensor are white and the background black
    image_depth = Image.fromarray(depth.astype("uint16"))
    image_depth.save(out_path)

if __name__ == "__main__":
    images_path = os.environ["DIR_IMAGES"]
    
    for entry in os.scandir(images_path):  
        if entry.is_file():  # check if it's a file
            invert_depth(images_path + "/" + os.path.basename(entry), images_path + "/" + os.path.basename(entry))