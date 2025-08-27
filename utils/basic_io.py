import json
from depth2loc.params import *

def save_per_frame_action_labels(action_labels_per_frame):
    json.dump(action_labels_per_frame, open(per_frame_action_labels_path, 'w'))
    print(f"Saved per frame action labels to {per_frame_action_labels_path}")