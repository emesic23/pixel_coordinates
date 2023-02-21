import numpy as np
import cv2
import pandas as pd
from scipy.spatial.transform import Rotation

def rectify(cam_mtx, D, image):
    height, width, _ = image.shape
    map1,map2=cv2.initUndistortRectifyMap(cam_mtx, D, None, None, (width, height), cv2.CV_32FC1)
    mapped = cv2.remap(image, map1, map2, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    return map1, map2, mapped

def get_image_data(alignment_fp, image_fp):
    alignment_data = pd.read_csv(alignment_fp)
    alignment_data = alignment_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    image_data = alignment_data[alignment_data['image'] == image_fp]
    return image_data

def get_world_coords(K, R, T, camera_coords):
    RT = np.concatenate((R, T.reshape(-1, 1)), axis=1)
    # Camera coordinates
    camera_coords_homo = cv2.convertPointsToHomogeneous(camera_coords)
    world_coords = []
    for coord in camera_coords_homo:
        world_coords.append(np.linalg.pinv(K @ RT) @ coord[0])
    return np.array(world_coords)

def get_world_latlon(world_coords, lat, lon):
    m_to_deg = 111320
    latlons = []
    for coord in world_coords:
        lat_pix = lat + coord[1] / m_to_deg
        lon_pix = lon + coord[0] / (m_to_deg * np.cos(lat))
        latlons.append([lat_pix, lon_pix])
    return np.array(latlons)

def euler_method(image, image_data, camera_mtx):
    height, width, _ = image.shape
    alt = image_data['  camNED_D'].values.astype(float)[0]
    quat = image_data[["camNED_qw", "camNED_qx", "camNED_qy", "camNED_qz"]].values[0]
    rot = Rotation.from_quat(quat)


    euler = rot.as_euler("xyz", degrees=False)
    pitch = euler[1]
    theta = 1.5708 - pitch

    distance_to_mid = -alt * np.tan(theta)
    
    fovy = 2 * np.arctan(height / (2 * (camera_mtx[1][1])))
    fovx = 2 * np.arctan(width / (2 * camera_mtx[0][0]))
    return