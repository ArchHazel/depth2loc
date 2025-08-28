import json
from omegaconf import DictConfig
import os
import numpy as np
from calibrateKinectv2.depth_preprocessing import visualize_depth


def save_per_frame_action_labels(action_labels_per_frame, cfg: DictConfig):
    json.dump(action_labels_per_frame, open(cfg.model.paths.per_frame_action_labels, 'w'))
    print(f"Saved per frame action labels to {cfg.model.paths.per_frame_action_labels}")



def load_per_frame_action_labels(cfg: DictConfig):
    return json.load(open(cfg.model.paths.per_frame_action_labels, 'r'))

def list_and_sort_files(folder,key=None):
    files = os.listdir(folder)
    if key is not None:
        files.sort(key=key)
    else:
        files.sort()
    return files


def list_images_with_human_presence(cfg: DictConfig):
    mask = load_per_frame_action_labels(cfg)
    if cfg.model.sensor_name == "HAR6":
        visible_s = cfg.model.HAR6.visible_s
    mask_boolean = np.array([mask[str(i)] in visible_s for i in range(len(mask))])
    rgb_images = np.array(list_and_sort_files(cfg.model.paths.rgb_F, key=lambda x: int(x.split('.')[0].split('_')[-1])))
    return rgb_images[mask_boolean]



def save_predicted_depth_in_png_and_npy(depth, img_path, cfg: DictConfig):
    os.makedirs(cfg.model.paths.depth_F_npy, exist_ok=True)
    np.save(os.path.join(cfg.model.paths.depth_F_npy, img_path.split('.')[0] + '.npy'), depth)
    os.makedirs(cfg.model.paths.depth_F_png, exist_ok=True)
    visualize_depth(depth, cfg.model.paths.depth_F_png, int(img_path.split('.')[0].split('_')[-1]), cfg.model.to_visual_depth_as_png.scaling_factor)

def from_frames_to_video(frame_paths_list, fps:int, output_video_f):
    import subprocess

    rgb_f_parent = os.path.dirname(output_video_f)
    print(f"Saving video to {rgb_f_parent}")


    with open(f"{rgb_f_parent}/frames.txt", "a") as f:
        for i, item in enumerate(frame_paths_list):
            f.write(f"file '{item}'\n")
            f.write(f"duration {1/fps}\n")
    
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", f"{rgb_f_parent}/frames.txt",
        "-r", "15",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        f"{output_video_f}"
    ]

    
    subprocess.run(cmd)
    os.remove(f"{rgb_f_parent}/frames.txt")