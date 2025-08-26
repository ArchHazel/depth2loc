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
Please specify the sensor name. 
If visiable list for that sensor does not exist in the params.yaml, it needs be annotated manually.
```bash
python -m depth2loc.utils.helper --sensor_name HAR6
```

### Slice video using timetable of activity.
Sliced video clips are put in the same folder as original color video `rgb.avi` with name `rgb_00.avi` - `rgb_37.avi`.
> I have confirmed that sessions after 2025/04/22 have and only have 38 activities. If you are dealing with earlier sessions, I suggest printing out the timetable first and paying closer attention.


### Human in the loop
```yaml
2025/08/26: annotate the visiable actions captured by HAR6 [recorded in params.yaml as HAR6.visible_s]
```