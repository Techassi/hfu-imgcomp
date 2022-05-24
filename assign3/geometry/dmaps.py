import numpy as np
import cv2 as cv

from thints.geometry import DepthMapsList, RectificationMatricesList, SGBMParams
from thints.images import ImageList


def depth_maps(imgs: ImageList, rm_list: RectificationMatricesList, sgbm_params: SGBMParams) -> DepthMapsList:
    '''
    Compute depth maps for each image combination via semi global matching.

    Parameters
    ----------
    imgs : ImageList
        List of images (matrices)
    rm_list : RectificationMatricesList
        List of rectification matrices
    sgbm_params : SGBMParams
        Semi global matching params

    Returns
    -------
    maps_list : DepthMapsList
        List of depth maps for each combination
    '''
    maps_list: DepthMapsList = []

    stereo_sgbm = cv.StereoSGBM_create(**sgbm_params)

    for rm in rm_list:
        disp_sgbm = stereo_sgbm.compute(imgs[rm[4][0]][0], imgs[rm[4][1]][0]).astype(np.float32)
        disp_sgbm = cv.normalize(disp_sgbm, 0, 255, cv.NORM_MINMAX)

        maps_list.append((
            disp_sgbm,
            rm[4]
        ))

    return maps_list


def combine_maps(dm_list: DepthMapsList) -> np.ndarray:
    ''''''
    if len(dm_list) == 1:
        return dm_list[0][0]

    disp = dm_list[0][0]
    for i in range(1, len(dm_list)):
        disp = np.add(disp, dm_list[i][0])

    return cv.normalize(disp, 0, 255, cv.NORM_MINMAX)


def sgbm_params(
    speckle_size: int,
    speckle_range: int,
    min_disp: int,
    num_disp: int,
    disp_diff: int,
    unique_ratio: int,
    block_size: int
) -> SGBMParams:
    '''
    Construct a new SGBMParams typed dict.
    '''
    p: SGBMParams = {
        'speckleWindowSize': speckle_size,
        'uniquenessRatio': unique_ratio,
        'numDisparities': num_disp,
        'disp12MaxDiff': disp_diff,
        'minDisparity': min_disp,
        'speckleRange': speckle_range,
        'blockSize': block_size
    }
    return p
