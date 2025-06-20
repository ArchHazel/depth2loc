import cv2
import os
import numpy as np

movie_name = 'IMG_1872'
output_folder = f'/home/hazel/Datasets/image-online/{movie_name}_visualize_sti'

img_names = os.listdir(output_folder)
img_names.sort()


# make the images into a video
video_name = os.path.join(output_folder, f'{movie_name}_stitch.avi')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 1
frame_size = (2560 , 720)  # Assuming all images are the same size
video_writer = cv2.VideoWriter(video_name, fourcc, fps, frame_size)
for img_name in img_names:
    img_path = os.path.join(output_folder, img_name)
    print(img_path)
    img = cv2.imread(img_path)
    video_writer.write(img)
video_writer.release()
print(f"Video saved to {video_name}")
