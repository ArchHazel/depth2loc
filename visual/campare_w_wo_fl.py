# © 2025 Huijun Han @ MOCALAB. All rights reserved.
# Date: 2025-09-01
from omegaconf import DictConfig
from depth2loc.utils.basic_draw import *
from calibrateKinectv2.utils.depth_utils import *
from calibrateKinectv2.run_and_visualized_diff import get_depth_diff_folder_wise
import hydra

@hydra.main(config_path="/home/hhan2/Scripts/hof", config_name="config",version_base=None)
def main(cfg: DictConfig):
    diff_folder_png = cfg.model.experiments.paths.depth_F_png.replace("{expr}",cfg.model.experiments.expr[3])
    stitched_folder = cfg.model.experiments.paths.depth_F_png.replace("{expr}",cfg.model.experiments.expr[2]) 
    output_video = f"{stitched_folder}/../depth_d_video.mp4"
    with_folder_png = cfg.model.experiments.paths.depth_F_png.replace("{expr}",cfg.model.experiments.expr[0])
    without_folder_png = cfg.model.experiments.paths.depth_F_png.replace("{expr}",cfg.model.experiments.expr[1])
    with_folder_npy = cfg.model.experiments.paths.depth_F_npy.replace("{expr}",cfg.model.experiments.expr[0])
    without_folder_npy = cfg.model.experiments.paths.depth_F_npy.replace("{expr}",cfg.model.experiments.expr[1])
    wanted_diff = True
    if wanted_diff:
        get_depth_diff_folder_wise(with_folder_npy, without_folder_npy, diff_folder_png)
        stitch_three_images_side_by_side_and_save(with_folder_png, without_folder_png, diff_folder_png, stitched_folder)
        from_frame_folder_to_video(stitched_folder, cfg.dataset.fps, output_video)
    else:
        stitch_two_images_side_by_side_and_save(with_folder_png, without_folder_png, stitched_folder)
        from_frame_folder_to_video(stitched_folder, cfg.dataset.fps, output_video)

def ad_hoc_make_video_from_frames():
    frames_folder = "/mnt/data01/DepthPro/Sensor Node 6 (HAR6)/2025_04_22_15_10_07_SB-29937C/depth"
    output_video = "/mnt/data01/DepthPro/Sensor Node 6 (HAR6)/2025_04_22_15_10_07_SB-29937C/depth_gt.mp4"
    from_frame_folder_to_video(frames_folder, 15, output_video)


if __name__ == "__main__":
    main()