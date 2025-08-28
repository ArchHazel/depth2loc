### To use depth-pro, first install depth-pro and download its checkpoint.
```bash
cd depth2loc
pip install -e .
source get_pretrained_models.sh 
```

### Activate environment.
```bash
conda activate depth-pro
```

### Quick check "subjects in the view" video length 
You can specify the sensor name `calculate_duration.sensor_name` @ `depth-pro.yaml`.
If visiable list for that sensor does not exist in the params.yaml, it needs be annotated manually.
```bash
python -m depth2loc.utils.helper
```

### Slice video using timetable of activity. (ffmpeg is for acceleration)
Keep in mind, typically we do not actually slice video since it is very time consuming. Instead, we save the `action_labels_per_frame`.
```bash
python -m depth2loc.modules.assign_per_frame_label_using_action_label_file
```

You may set `visualize_sliced_video` @ `depth-pro.yaml` as `True` while debugging. Sliced video clips are put in the same folder as original color video `rgb.avi` with name `rgb_00.mp4` - `rgb_37.mp4`.

> I have confirmed that sessions after 2025/04/22 have and only have 38 activities. If you are dealing with earlier sessions, I suggest printing out the timetable first and paying closer attention.

### Run Depth estimation on frames with human presence
```bash
python -m depth2loc.run_depth_estimation_on_masked_video
```


### Human in the loop
```yaml
2025/08/26: annotate the visiable actions captured by HAR6 [recorded in params.yaml as HAR6.visible_s]
```