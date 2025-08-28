import json
from depth2loc.params import *
import os
import numpy as np
import cv2
from calibrateKinectv2.depth_preprocessing import visualize_depth

def save_per_frame_action_labels(action_labels_per_frame):
    json.dump(action_labels_per_frame, open(per_frame_action_labels_path, 'w'))
    print(f"Saved per frame action labels to {per_frame_action_labels_path}")

def load_per_frame_action_labels():
    return json.load(open(per_frame_action_labels_path, 'r'))

def list_and_sort_files(folder,key=None):
    files = os.listdir(folder)
    if key is not None:
        files.sort(key=key)
    else:
        files.sort()
    return files

def list_images_with_human_presence():
    mask = load_per_frame_action_labels()
    mask_boolean = np.array([mask[str(i)] in visible_s for i in range(len(mask))])
    rgb_images = np.array(list_and_sort_files(rgb_F, key=lambda x: int(x.split('.')[0].split('_')[-1])))
    return rgb_images[mask_boolean]

def save_predicted_depth_in_png_and_npy(depth, img_path):
    os.makedirs(depth_F_npy, exist_ok=True)
    np.save(os.path.join(depth_F_npy, img_path.split('.')[0] + '.npy'), depth)
    os.makedirs(depth_F_png, exist_ok=True)
    visualize_depth(depth, depth_F_png, int(img_path.split('.')[0].split('_')[-1]), sf_for_d)
