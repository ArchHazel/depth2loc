import depth_pro
import os
import cv2
import torch
import numpy as np
from depth2loc.utils.basic_io import * 
import matplotlib.pyplot as plt
import tqdm
from matplotlib import cm
from matplotlib.colors import Normalize
import calibrateKinectv2
from  calibrateKinectv2.calibrateKinect import *
import hydra
from omegaconf import DictConfig






def draw_joint_traj():
    keypoints_3D = {}
    keypoints_2D_projected = {}
    if img_path in keypoints:
        keypoint = keypoints[img_path]
        for i in range(len(keypoint)):
            kpt = keypoint[i]
            depth_kp = depth[kpt[1], kpt[0]]
            x = kpt[0] 
            y = kpt[1] 
            # Convert to camera coordinates
            x_camera = (x - intrinsic_matrix[0, 2]) * depth_kp / intrinsic_matrix[0, 0]
            y_camera = (y - intrinsic_matrix[1, 2]) * depth_kp / intrinsic_matrix[1, 1]
            z_camera = depth_kp






            if img_path not in keypoints_3D:
                keypoints_3D[img_path] = [(x_camera, y_camera, z_camera)]
                keypoints_2D_projected[img_path] = [(x, y)]
                
            else:
                keypoints_3D[img_path].append((x_camera, y_camera, z_camera))
                keypoints_2D_projected[img_path].append((x, y))
            
        # print("Keypoints 3D:", keypoints_3D[img_path])


    # visualize on original image
    history_max = 30

    norm = Normalize(vmin=0, vmax=max_depth)
    cmap = cm.get_cmap('jet', 256)
    for img_idx, img_path in tqdm.tqdm(enumerate(imgs_path), desc="Visualizing depth on image"):
        if img_path in keypoints_3D:
            image = cv2.imread(os.path.join(rgb_folder, img_path))
            cur_img_path = img_path
            history_count = 0
            for k in range(img_idx - 1, 0, -1):
                
                prev_img_path = imgs_path[k]
                if prev_img_path not in keypoints_3D:
                    continue

                for i in range(len(keypoints_3D[cur_img_path])):

                    z = keypoints_3D[cur_img_path][i][2]
                    x = int(keypoints_2D_projected[cur_img_path][i][0])
                    y = int(keypoints_2D_projected[cur_img_path][i][1])

                    prev_x = int(keypoints_2D_projected[prev_img_path][i][0])
                    prev_y = int(keypoints_2D_projected[prev_img_path][i][1])

                    color = cmap(norm(z))
                    color = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
                    # print("z:", z)
                    # print(color)

                    if history_count == 0:
                        cv2.circle(image, (x, y), 10, color, -1)
                    cv2.line(image, (prev_x, prev_y), (x, y), color, 5)
                
                cur_img_path = prev_img_path
                history_count += 1
                if history_count >= history_max:
                    break

            cv2.imwrite(os.path.join(visualize_video_folder, img_path), image)        

    # visulize the 3d points


    plt.figure()
    # ax = fig.add_subplot(projection='3d')
    # ax = fig.add_subplot()

    # sort the keypoints_3D by time
    keypoints_3D = dict(sorted(keypoints_3D.items(), key=lambda item: int(item[0].split('.')[0][-4:])))

    for img_path,kpts in tqdm.tqdm(keypoints_3D.items(), desc="Visualizing 3D points on bird's eye view"):
        time_stamp = int(img_path.split('.')[0][-4:])
        if time_stamp % 10 != 0:
            continue
        x_vals = []
        y_vals = []
        z_vals = []
        min_time = 0
        max_time = 760
        norm = Normalize(vmin=min_time, vmax=max_time)
        cmap = cm.get_cmap('hsv', 256)
        for img_path_j, kpts_j in keypoints_3D.items():
            time_stamp_j = int(img_path_j.split('.')[0][-4:])
            if img_path_j == img_path:
                break

            


            color =  cmap(norm(time_stamp_j))

            mean_kpt = np.mean(kpts_j, axis=0)
            x_vals.append(mean_kpt[0])
            y_vals.append(mean_kpt[1])
            z_vals.append(mean_kpt[2])
            plt.scatter(mean_kpt[0], mean_kpt[2], c=color, marker='o')
            plt.xlim(-3, 3)
            # ax.set_ylim(-3, 3)
            plt.ylim(0, 6)
        
            



        plt.plot(x_vals, z_vals, color='black', alpha=0.5)
        plt.xlabel('Right (x) /M')
        # ax.set_ylabel('Down (y) /M')
        plt.ylabel('Forward (z) /M')
        plt.grid(False)
        # ax.view_init(elev=0, azim=-90)

        plt.savefig(os.path.join(visualize_video_folder, f'floorplan_{img_path}.png'), dpi=300)
                    

def depth_pro_init():
    model, transform = depth_pro.create_model_and_transforms(device=torch.device("cuda:0") ,precision= torch.float16)
    model.eval()
    return model, transform

def depth_pro_infer(image_path, model, transform):
    image, _, f_px = depth_pro.load_rgb(image_path)
    # f_px = np.mean([color_intrinsics[0,0], color_intrinsics[1,1]])
    # print(f"Focal length in pixels: {f_px}")
    image = transform(image)
    prediction = model.infer(image, f_px=f_px)
    depth = prediction["depth"]  # Depth in [m].
    depth = depth.detach().cpu().numpy()
    print(f"estimated focal length in pixels: {prediction['focallength_px']}")
    return depth

@hydra.main(config_path="/home/hhan2/Scripts/hof", config_name="config",version_base=None)
def main(cfg: DictConfig):
    extract_rgb_frames_smart_termination_if_done_before(cfg.model.paths.rgb_f,cfg.model.paths.rgb_F)
    imgs_path = list_images_with_human_presence()
    model, transform = depth_pro_init()

    for img_path in tqdm.tqdm(imgs_path, desc="Estimating depth"):
        depth = depth_pro_infer(os.path.join(cfg.model.paths.rgb_F, img_path), model, transform)
        save_predicted_depth_in_png_and_npy(depth,img_path)


if __name__ == "__main__":
    main()
