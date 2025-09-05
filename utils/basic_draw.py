import os
from depth2loc.utils.basic_io import list_and_sort_files
import cv2
from tqdm import tqdm


def from_frames_list_to_video(frame_paths_list, fps:int, output_video_f):
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

def from_frame_folder_to_video(frame_folder: str, fps: int, output_video_f: str):
    frame_paths_list = list_and_sort_files(frame_folder)
    from_frames_list_to_video(frame_paths_list, fps, output_video_f)

def stitch_two_images_side_by_side_and_save(left_img_F , right_img_F,output_F):
    os.makedirs(output_F, exist_ok=True)
    left_pngs = list_and_sort_files(left_img_F)
    right_pngs = list_and_sort_files(right_img_F)
    assert len(left_pngs) == len(right_pngs), "Left and right image folders must have the same number of images."
    stitched_images = []
    for left_img, right_img in tqdm(zip(left_pngs, right_pngs),total=len(left_pngs)):
        left = cv2.imread(left_img)
        right = cv2.imread(right_img)
        stitched = cv2.hconcat([left, right])
        stitched_image_path = os.path.join(output_F, os.path.basename(left_img))
        cv2.imwrite(stitched_image_path, stitched)
        

def stitch_three_images_side_by_side_and_save(left_img_F , middle_img_F, right_img_F, output_F):
    os.makedirs(output_F, exist_ok=True)
    left_pngs = list_and_sort_files(left_img_F)
    middle_pngs = list_and_sort_files(middle_img_F)
    right_pngs = list_and_sort_files(right_img_F)
    assert len(left_pngs) == len(middle_pngs) == len(right_pngs), "All image folders must have the same number of images."
    stitched_images = []
    for left_img, middle_img, right_img in tqdm(zip(left_pngs, middle_pngs, right_pngs),total=len(left_pngs)):
        left = cv2.imread(left_img)
        middle = cv2.imread(middle_img)
        right = cv2.imread(right_img)
        stitched = cv2.hconcat([left, middle, right])
        stitched_image_path = os.path.join(output_F, os.path.basename(left_img))
        cv2.imwrite(stitched_image_path, stitched)
        