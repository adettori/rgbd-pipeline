from PIL import Image
from transformers import AutoModelForCausalLM
from pycocotools import mask as mask_utils
import numpy as np
import torch
import os, sys, logging

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout)) # defaults to sys.stderr

def setup(base_in_dir):
    # Prepare dirs
    list_subdirs = ["masks"]
    
    for subdir in list_subdirs:
        dir_path = base_in_dir + "/" + subdir
        try:
            os.mkdir(dir_path)
        except FileExistsError:
            pass

    # Load model
    torch.set_float32_matmul_precision('high')

    model = AutoModelForCausalLM.from_pretrained(
        "tiiuae/falcon-perception",
        trust_remote_code=True,
        device_map={"": "cuda:0"},
    )

    return model

def predict_mask(prompt, model, in_path, out_path):
    # Load and preprocess an image.
    image = Image.open(in_path)
    preds = model.generate(image, prompt)[0]

    rle = preds[0]["mask_rle"]
    # pycocotools expects bytes for counts
    m = {"size": rle["size"], "counts": rle["counts"].encode("utf-8")}
    mask = mask_utils.decode(m).astype("uint8") * 255  # H x W
    image = Image.fromarray(mask)
    image.save(out_path)

if __name__ == "__main__":
    prompt = os.environ["MASK_PROMPT"]
    base_in_dir = "./input"
    base_out_dir = base_in_dir + "/masks"
    model = setup(base_in_dir)

    rgb_in_dir = base_in_dir + "/rgb" 
    
    for entry in os.scandir(rgb_in_dir):  
        if entry.is_file():  # check if it's a file
            predict_mask(prompt, model, entry, base_out_dir + "/" + os.path.basename(entry))