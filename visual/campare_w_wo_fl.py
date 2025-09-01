import os
from omegaconf import DictConfig
from depth2loc.utils.basic_io import list_and_sort_files
from depth2loc.utils.basic_draw import from_frames_to_video, stitch_two_images_side_by_side_and_save

def main():
    stitched_folder = "/mnt/data01/DepthPro/Sensor Node 6 (HAR6)/2025_04_22_15_10_07_SB-29937C/wwo/depth_d_png"
    output_video = "/mnt/data01/DepthPro/Sensor Node 6 (HAR6)/2025_04_22_15_10_07_SB-29937C/wwo/depth_d_video.mp4"
    with_folder = "/mnt/data01/DepthPro/Sensor Node 6 (HAR6)/2025_04_22_15_10_07_SB-29937C/wgtfl/depth_d_png"
    without_folder = "/mnt/data01/DepthPro/Sensor Node 6 (HAR6)/2025_04_22_15_10_07_SB-29937C/wogtfl/depth_d_png"
    os.makedirs(stitched_folder, exist_ok=True)
    stitch_two_images_side_by_side_and_save(with_folder, without_folder, stitched_folder)

    stitched_files_list = list_and_sort_files(stitched_folder)

    from_frames_to_video(stitched_files_list, 15, output_video)

def main2():
    stitched_folder = "/mnt/data01/DepthPro/Sensor Node 6 (HAR6)/2025_04_22_15_10_07_SB-29937C/depth"
    output_video = "/mnt/data01/DepthPro/Sensor Node 6 (HAR6)/2025_04_22_15_10_07_SB-29937C/depth_gt.mp4"
    stitched_files_list = list_and_sort_files(stitched_folder)
    

    from_frames_to_video(stitched_files_list, 15, output_video)


if __name__ == "__main__":
    main2()
