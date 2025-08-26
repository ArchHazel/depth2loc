from depth2loc.utils.helper import *
import cv2
from tqdm import trange

def slice_video(rgb_ts_f_txt, segment_file):
    segments, acts = load_segment_file_to_datetime(segment_file) # by default, we have 38 actions
    segment_idx = 0
    frame_idx = 0
    is_background = True
    action_label = {}
    
    with open(rgb_ts_f_txt, 'r') as f:
        lines = f.readlines()
        for line in lines:
            frame_ts = float(line.strip()  )
            if segment_idx >= len(segments):
                action_label[frame_idx] = -1
                continue    
            if frame_ts < segments[segment_idx][0] and is_background:
                # print("frame_ts < segments[segment_idx][0] and is_background: ", frame_ts, segments[segment_idx][0])
                action_label[frame_idx] = -1
            elif frame_ts > segments[segment_idx][1]:
                # print("frame_ts > segments[segment_idx][1]: ", frame_ts, segments[segment_idx][1])
                if not is_background:
                    segment_idx += 1
                    is_background = True
                action_label[frame_idx] = -1
            else:
                # print("frame_ts is within segment: ", frame_ts, segments[segment_idx])
                action_label[frame_idx] = segment_idx
                is_background = False

            frame_idx += 1
        actions_num = len(segments) 

    return action_label, actions_num

if __name__ == "__main__":
    action_labels, actions_num = slice_video(rgb_ts_f_txt, seg_f_txt)
    for i in trange(actions_num):
        new_video_path  = rgb_f.replace("rgb.avi",f"rgb_{i:02d}.avi")
        out = cv2.VideoWriter(new_video_path, cv2.VideoWriter_fourcc(*'XVID'), 15, (1920, 1080))
        for j in range(len(action_labels)):
            if action_labels[j] == i:
                frame = cv2.imread(f"{rgb_F}/frame_{j:05d}.png")
                h, w, _ = frame.shape
                out.write(frame)
        out.release()
