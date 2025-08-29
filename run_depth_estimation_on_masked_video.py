import depth_pro
import os
import torch
import numpy as np
from depth2loc.utils.basic_io import * 
import tqdm
from  calibrateKinectv2.calibrateKinect import *
import hydra
from omegaconf import DictConfig
         
def depth_pro_init():
    model, transform = depth_pro.create_model_and_transforms(device=torch.device("cuda:0") ,precision= torch.float16)
    model.eval()
    return model, transform

def depth_pro_infer(image_path, model, transform,cfg):
    image, _, f_px = depth_pro.load_rgb(image_path)
    if cfg.model.has_gt_fl:
        color_intrinsics = read_color_intrinsics(cfg.dataset.paths.color_intrinsics_file)
        f_px = np.mean([color_intrinsics[0,0], color_intrinsics[1,1]]).astype(np.float32)
    image = transform(image)
    prediction = model.infer(image, f_px=f_px)
    depth = prediction["depth"]  # Depth in [m].
    depth = depth.detach().cpu().numpy()
    return depth

@hydra.main(config_path="/home/hhan2/Scripts/hof", config_name="config",version_base=None)
def main(cfg: DictConfig):
    extract_rgb_frames_smart_termination_if_done_before(cfg.model.paths.rgb_f,cfg.model.paths.rgb_F)
    imgs_path = list_images_with_human_presence(cfg)
    model, transform = depth_pro_init()

    for img_path in tqdm.tqdm(imgs_path, desc="Estimating depth"):
        depth = depth_pro_infer(os.path.join(cfg.model.paths.rgb_F, img_path), model, transform,cfg)
        save_predicted_depth_in_png_and_npy(depth,img_path,cfg)

if __name__ == "__main__":
    main()
