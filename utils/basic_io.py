import json
from depth2loc.params import *
import os
import numpy as np

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
    print("length of mask:", len(mask))
    mask_boolean = np.array([mask[str(i)] != -1 for i in range(len(mask))])
    rgb_images = np.array(list_and_sort_files(rgb_F, key=lambda x: int(x.split('.')[0].split('_')[-1])))
    print("length of rgb_images:", len(rgb_images))
    return rgb_images[mask_boolean]