from PIL import Image
import numpy as np
import os, sys, logging, pathlib

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout)) # defaults to sys.stderr

def save_npy_as_image(in_path, out_path):
    # Load and convert npy to image
    with open(in_path, 'rb') as f:
        image_arr = np.load(f).astype(np.uint16)
        image = Image.fromarray(image_arr)
        image.save(out_path)

if __name__ == "__main__":
    npy_in_path = os.environ["DIR_IN_NPY"]
    images_out_path = os.environ["DIR_OUT_IMAGES"]
    
    for entry in os.scandir(npy_in_path):  
        if entry.is_file():  # check if it's a file
            save_npy_as_image(npy_in_path + "/" + os.path.basename(entry), images_out_path + "/" + pathlib.Path(entry).stem + ".png")