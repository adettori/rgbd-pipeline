from PIL import Image
import numpy as np
import os, sys, logging, pathlib

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout)) # defaults to sys.stderr

def save_image_as_npy(in_path, out_path):
    # Load and convert image to numpy format
    image = Image.open(in_path)
    image_arr = np.asarray(image).astype(np.float32)

    with open(out_path, 'wb') as f:
        np.save(f, image_arr)

if __name__ == "__main__":
    images_in_path = os.environ["DIR_IN_IMAGES"]
    npy_out_path = os.environ["DIR_OUT_NPY"]
    
    for entry in os.scandir(images_in_path):  
        if entry.is_file():  # check if it's a file
            save_image_as_npy(images_in_path + "/" + os.path.basename(entry), npy_out_path + "/" + pathlib.Path(entry).stem + ".npy")