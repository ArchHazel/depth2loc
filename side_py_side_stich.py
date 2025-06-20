import os
movie_name = 'IMG_1872'
visualize_video_folder = f'/home/hazel/Datasets/image-online/{movie_name}_visualize'
output_folder = f'/home/hazel/Datasets/image-online/{movie_name}_visualize_sti'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
import cv2

files = os.listdir(visualize_video_folder)
img_2trajectory_dict = {}
class My_img_path:
    def __init__(self, path_t, path_f):
        self.path_t = path_t
        self.path_f = path_f

for file in files:
    idx = file.split('.')[0].split('_')[-1]
    idx = int(idx)
    if idx not in img_2trajectory_dict:
        img_path = My_img_path('', '')
    else:
        img_path = img_2trajectory_dict[idx]

    if file.startswith('floorplan'):
        img_path.path_f = os.path.join(visualize_video_folder, file)
    elif file.startswith('frame'):
        img_path.path_t = os.path.join(visualize_video_folder, file)
    
    img_2trajectory_dict[idx] = img_path

x = []
y = []

for idx,my_pth in img_2trajectory_dict.items():
    print(idx)
    if my_pth.path_f != '' and my_pth.path_t != '':
        img_f = cv2.imread(my_pth.path_f)
        img_t = cv2.imread(my_pth.path_t)
        # img_f at left, img_t at right
        img_f = cv2.resize(img_f, (img_t.shape[1], img_t.shape[0]))
        # img_t = cv2.cvtColor(img_t, cv2.COLOR_BGR2RGB)
        img = cv2.hconcat([img_f, img_t])
        cv2.imwrite(os.path.join(output_folder, f'stich_{idx}.jpg'), img)
        x.append(idx)
        y.append(1)


for i in range(0,570,10):
    if i not in img_2trajectory_dict:
        x.append(i)
        y.append(0)



print(x)
print(y)
import matplotlib.pyplot as plt
plt.scatter(x, y, c='blue', alpha=0.5)
plt.xlabel('Frame index')
plt.ylabel('Existence of floorplan')
plt.title('Existence of floorplan in each frame')
plt.show()


