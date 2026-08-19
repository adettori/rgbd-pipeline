from PIL import Image
import depth_pro
import torch
import os, sys

logger = logging.getLogger("logger")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler(sys.stdout)) # defaults to sys.stderr

def setup(base_in_dir):
    # Prepare dirs
    list_subdirs = ["depth"]
    
    for subdir in list_subdirs:
        dir_path = base_in_dir + "/" + subdir
        try:
            os.mkdir(dir_path)
        except FileExistsError:
            pass

    # Load model and preprocessing transform
    model, transform = depth_pro.create_model_and_transforms(device=torch.device("cuda"))
    model = model.eval()

def predict_depth(model, transform, in_path, out_path):
    # Load and preprocess an image.
    image, _, f_px = depth_pro.load_rgb(in_path)
    image = transform(image)
    
    # Run inference.
    prediction = model.infer(image, f_px=f_px)
    predicted_depth = prediction["depth"]  # Depth in [m].
    
    depth = (predicted_depth - predicted_depth.min()) / (predicted_depth.max() - predicted_depth.min())
    depth = depth.detach().cpu().numpy() * 100
    image_depth = Image.fromarray(depth.astype("uint8"))
    image_depth.save(out_path)


if __name__ == "__main__":
    base_in_dir = "./input"
    base_out_dir = base_in_dir + "/depth"
    setup(base_in_dir)
    
    # Load model and preprocessing transform
    model, transform = depth_pro.create_model_and_transforms(device=torch.device("cuda"))
    model = model.eval()

    rgb_in_dir = base_in_dir + "/rgb" 
    
    for entry in os.scandir(rgb_in_dir):  
        if entry.is_file():  # check if it's a file
            predict_depth(model, transform, entry, base_out_dir + "/" + os.path.basename(entry))