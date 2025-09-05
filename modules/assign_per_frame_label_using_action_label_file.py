from depth2loc.utils.helper import *
from tqdm import trange
from depth2loc.utils.basic_io import save_per_frame_action_labels
from depth2loc.utils.basic_draw import from_frames_list_to_video
import hydra
from omegaconf import DictConfig

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




def slice_video_using_ffmpeg_with_per_frame_action_label(rgb_f_parent, action_labels_per_frame, action_amount,cfg: DictConfig):

    for i in trange(action_amount):
        continued = True
        has_start = False
        has_end = False
        os.remove(f"{rgb_f_parent}/frames_{i:02d}.txt") if os.path.exists(f"{rgb_f_parent}/frames_{i:02d}.txt") else None
        os.remove(f"{rgb_f_parent}/rgb_{i:02d}.mp4") if os.path.exists(f"{rgb_f_parent}/rgb_{i:02d}.mp4") else None
        frame_path_lists = []
        for j in range(len(action_labels_per_frame)):
            if action_labels_per_frame[j] == i:
                if not has_start:
                    has_start = True
                if has_end:
                    continued = False
                frame_path_lists.append(f"{cfg.model.paths.rgb_F}/frame_{j:05d}.png")
            elif has_start and not has_end:
                has_end = True

        if continued==False or has_start==False:
            print(f"Warning: action {i} is not continuous or does not exist. Please check the timetable and rgb_ts_f_txt.")
            continue

        from_frames_list_to_video(frame_path_lists, cfg.dataset.fps, f"{rgb_f_parent}/rgb_{i:02d}.mp4")




@hydra.main(config_path="/home/hhan2/Scripts/hof", config_name="config",version_base=None)
def main(cfg: DictConfig):


    action_labels_per_frame, act_amount = get_per_frame_action_label(cfg.model.paths.rgb_ts_f_txt, cfg.model.paths.seg_f_txt)
    if act_amount != cfg.dataset.actions.total_amount:
        print(f"Warning: action amount {act_amount} != {cfg.dataset.actions.total_amount} in params.yaml")
    else:
        print(f"Fortunately, we have {act_amount} actions as expected.")

    save_per_frame_action_labels(action_labels_per_frame,  cfg)

    if cfg.model.visualize_sliced_video:
        slice_video_using_ffmpeg_with_per_frame_action_label(cfg.model.paths.rgb_f.rsplit('/', 1)[0], action_labels_per_frame, act_amount, cfg)

if __name__ == "__main__":
    main()