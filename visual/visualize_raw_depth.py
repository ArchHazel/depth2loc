
import hydra
from omegaconf import DictConfig
from calibrateKinectv2.utils.depth_utils import visualize_depth, read_gt_depth_given_frame_idx
from depth2loc.utils.basic_io import load_per_frame_action_labels
import os

@hydra.main(config_path="/home/hhan2/Scripts/hof/",config_name="config",version_base=None)
def main(cfg: DictConfig):
        mask_per_frame = load_per_frame_action_labels(cfg)
        for idx, category in mask_per_frame.items():
            if int(category) in cfg.model.HAR6.visible_s:
                depth_data = read_gt_depth_given_frame_idx(int(idx), cfg.model.paths.depth_F, cfg.dataset.depth_interval)
                visualize_depth(depth_data, cfg.model.paths.depth_gt_with_human_F, int(idx), cfg.model.to_visual_depth_as_png.scaling_factor, to_meter_sf=0.001) # gt depth is in mm, convert to meter



if __name__ == "__main__":
    main()