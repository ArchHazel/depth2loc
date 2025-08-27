from depth2loc.utils.helper import *
import cv2
from tqdm import trange
import subprocess
import argparse
from depth2loc.utils.basic_io import save_per_frame_action_labels

def get_per_frame_action_label(rgb_ts_f_txt, segment_file):
    segments, acts = load_segment_file_to_datetime(segment_file) # by default, we have 38 actions
    segment_idx = 0
    frame_idx = 0
    is_background = True
    action_label = {}

    with open(rgb_ts_f_txt, 'r') as f:
        lines = f.readlines()
        for line in lines:
            frame_ts = float(line.strip())
            if segment_idx >= len(segments):
                action_label[frame_idx] = -1
                frame_idx += 1
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
        actions_amount = len(segments) 
        action_label_per_frame = action_label

    return action_label_per_frame, actions_amount


def slice_video_using_ffmpeg_with_per_frame_action_label(rgb_f_parent, action_labels_per_frame, action_amount):

    for i in trange(action_amount):
        continued = True
        has_start = False
        has_end = False
        os.remove(f"{rgb_f_parent}/frames_{i:02d}.txt") if os.path.exists(f"{rgb_f_parent}/frames_{i:02d}.txt") else None
        os.remove(f"{rgb_f_parent}/rgb_{i:02d}.mp4") if os.path.exists(f"{rgb_f_parent}/rgb_{i:02d}.mp4") else None
        for j in range(len(action_labels_per_frame)):
            if action_labels_per_frame[j] == i:
                if not has_start:
                    has_start = True
                if has_end:
                    continued = False
                with open(f"{rgb_f_parent}/frames_{i:02d}.txt", "a") as f:
                    f.write(f"file '{rgb_F}/frame_{j:05d}.png'\n")
                    f.write(f"duration {1/fps}\n")
            elif has_start and not has_end:
                has_end = True

        if continued==False or has_start==False:
            print(f"Warning: action {i} is not continuous or does not exist. Please check the timetable and rgb_ts_f_txt.")
            continue

        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", f"{rgb_f_parent}/frames_{i:02d}.txt",
            "-r", "15",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",

            f"{rgb_f_parent}/rgb_{i:02d}.mp4"
        ]
        subprocess.run(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Slice video into segments")
    parser.add_argument("--slice_video", action="store_true", help="Whether to slice video into segments")
    args = parser.parse_args()

    action_labels_per_frame, act_amount = get_per_frame_action_label(rgb_ts_f_txt, seg_f_txt)
    if act_amount != action_amount:
        print(f"Warning: action amount {act_amount} != {action_amount} in params.yaml")
    else:
        print(f"Fortunately, we have {act_amount} actions as expected.")

    save_per_frame_action_labels(action_labels_per_frame)


    if args.slice_video:
        slice_video_using_ffmpeg_with_per_frame_action_label(rgb_f.rsplit('/', 1)[0], action_labels_per_frame, action_amount)

