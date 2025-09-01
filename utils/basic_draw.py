import os
from depth2loc.utils.basic_io import list_and_sort_files
import cv2

def from_frames_to_video(frame_paths_list, fps:int, output_video_f):
    import subprocess

    rgb_f_parent = os.path.dirname(output_video_f)
    print(f"Saving video to {rgb_f_parent}")


    with open(f"{rgb_f_parent}/frames.txt", "a") as f:
        for i, item in enumerate(frame_paths_list):
            f.write(f"file '{item}'\n")
            f.write(f"duration {1/fps}\n")
    
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", f"{rgb_f_parent}/frames.txt",
        "-r", "15",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        f"{output_video_f}"
    ]

    
    subprocess.run(cmd)
    os.remove(f"{rgb_f_parent}/frames.txt")

def stitch_two_images_side_by_side_and_save(left_img_F , right_img_F,output_F):
    left_pngs = list_and_sort_files(left_img_F)
    right_pngs = list_and_sort_files(right_img_F)
    assert len(left_pngs) == len(right_pngs), "Left and right image folders must have the same number of images."
    stitched_images = []
    for left_img, right_img in zip(left_pngs, right_pngs):
        left = cv2.imread(left_img)
        right = cv2.imread(right_img)
        stitched = cv2.hconcat([left, right])
        stitched_image_path = os.path.join(output_F, os.path.basename(left_img))
        cv2.imwrite(stitched_image_path, stitched)
        break
