import yaml

my_params_path = "depth2loc/params.yaml"
with open(my_params_path, 'r') as f:
    params = yaml.safe_load(f)
    paths = params.get('paths', None)
    rgb_ts_f_txt = paths.get('rgb_ts_f_txt', None)
    rgb_f = paths.get('rgb_f', None)
    rgb_F = paths.get('rgb_F', None)
    depth_F_png = paths.get('depth_F_png', None)
    depth_F_npy = paths.get('depth_F_npy', None)
    seg_f_txt = paths.get('seg_f_txt', None)

    visible_s = params.get('HAR6', {}).get('visible_s', None)
    action_amount = params.get('actions', {}).get('total_amount', None)