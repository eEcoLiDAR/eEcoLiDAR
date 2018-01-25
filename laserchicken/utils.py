import numpy as np
from laserchicken import keys

def get_point(pc,index):
    return pc[keys.point]["x"]["data"][index],pc[keys.point]["y"]["data"][index],pc[keys.point]["z"]["data"][index]

def copy_pointcloud(pc_in, array_mask = None):
    """
    Makes a deep copy of a point cloud dict using the array mask when copying the points.
    :param pc_in: Input point cloud
    :param array_mask: A mask indicating which points to copy.
    :return: The copy including only the masked points.
    """
    result = {}
    for key, value in pc_in.items():
        if isinstance(value, dict):
            new_value = copy_pointcloud(value, array_mask)
        elif isinstance(value, np.ndarray):
            if array_mask is not None:
                new_value = value[array_mask] if any(value) else np.copy(value)
            else:
                new_value = np.copy(value)
        else:
            new_value = value
        result[key] = new_value
    return result