
import hydra
from omegaconf import DictConfig
from calibrateKinectv2.depth_utils import visualize_depth, read_gt_depth
from depth2loc.utils.basic_io import load_per_frame_action_labels
import os

@hydra.main(config_path="/home/hhan2/Scripts/hof/",config_name="config",version_base=None)
def main(cfg: DictConfig):
        mask_per_frame = load_per_frame_action_labels(cfg)
        for idx, category in mask_per_frame.items():
            if int(category) in cfg.model.HAR6.visible_s:
                depth_data = read_gt_depth(cfg.model.paths.depth_F,int(idx),cfg.dataset.depth_interval)
                visualize_depth(depth_data, cfg.model.paths.depth_gt_with_human_F,int(idx), cfg.model.to_visual_depth_as_png.scaling_factor/1000)



if __name__ == "__main__":
    main()