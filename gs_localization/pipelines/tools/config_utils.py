import yaml
from tools import read_write_model

def load_config(path, default_path=None):
    """
    Loads config file.

    Args:
        path (str): path to config file.
        default_path (str, optional): whether to use default path. Defaults to None.

    Returns:
        cfg (dict): config dict.

    """
    # load configuration from per scene/dataset cfg.
    with open(path, "r") as f:
        cfg_special = yaml.full_load(f)

    inherit_from = cfg_special.get("inherit_from")

    if inherit_from is not None:
        cfg = load_config(inherit_from, default_path)
    elif default_path is not None:
        with open(default_path, "r") as f:
            cfg = yaml.full_load(f)
    else:
        cfg = dict()

    # merge per dataset cfg. and main cfg.
    update_recursive(cfg, cfg_special)

    return cfg


def update_recursive(dict1, dict2):
    """
    Update two config dictionaries recursively. dict1 get masked by dict2, and we retuen dict1.

    Args:
        dict1 (dict): first dictionary to be updated.
        dict2 (dict): second dictionary which entries should be used.
    """
    for k, v in dict2.items():
        if k not in dict1:
            dict1[k] = dict()
        if isinstance(v, dict):
            update_recursive(dict1[k], v)
        else:
            dict1[k] = v

def set_config(tr_dirs, config):
    cameras, _, _ = read_write_model.read_model(tr_dirs, ".bin")
    config["Dataset"]["dataset_path"] = tr_dirs
    config["Dataset"]["Calibration"]["fx"] = cameras[1][4][0]
    config["Dataset"]["Calibration"]["fy"] = cameras[1][4][1]
    config["Dataset"]["Calibration"]["cx"] = cameras[1][4][2]
    config["Dataset"]["Calibration"]["cy"] = cameras[1][4][3]
    config["Dataset"]["Calibration"]["width"] = cameras[1][2]
    config["Dataset"]["Calibration"]["height"] = cameras[1][3]
    return config
