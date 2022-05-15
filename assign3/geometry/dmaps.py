import numpy as np
import cv2 as cv

from thints.geometry import BMParams, DepthMapsList, RectificationMatricesList, SGBMParams
from thints.images import ImageList


def depth_maps_multi(
    imgs: ImageList,
    rm_list: RectificationMatricesList,
    bm_params: BMParams,
    sgbm_params: SGBMParams
) -> DepthMapsList:
    '''
    Compute multiple depth maps and combine them into one based on two images. This returns depth maps for each
    combination of images.

    Parameters
    ----------
    imgs : ImageList
        List of images (matrices)
    rm_list : RectificationMatricesList
        List of rectification matrices
    bm_params : BMParams

    sgbm_params : SGBMParams
    '''
    maps_list: DepthMapsList = []

    stereo_sgbm = cv.StereoSGBM_create(**sgbm_params)
    stereo_bm = cv.StereoBM_create(**bm_params)

    for rm in rm_list:
        disp_sgbm = stereo_sgbm.compute(imgs[rm[4][0]], imgs[rm[4][1]]).astype(np.float32)
        disp_bm = stereo_bm.compute(imgs[rm[4][0]], imgs[rm[4][1]]).astype(np.float32)

        disp_sgbm = cv.normalize(disp_sgbm, 0, 255, cv.NORM_MINMAX)
        disp_bm = cv.normalize(disp_bm, 0, 255, cv.NORM_MINMAX)

        disp = np.add(disp_sgbm, disp_bm)
        disp = cv.normalize(disp, 0, 255, cv.NORM_MINMAX)

        maps_list.append((
            disp_sgbm,
            rm[4]
        ))

    return maps_list


def depth_maps_single(imgs: ImageList, rm_list: RectificationMatricesList, sgbm_params: SGBMParams) -> DepthMapsList:
    ''''''
    maps_list: DepthMapsList = []

    stereo_sgbm = cv.StereoSGBM_create(**sgbm_params)

    for rm in rm_list:
        disp_sgbm = stereo_sgbm.compute(imgs[rm[4][0]], imgs[rm[4][1]]).astype(np.float32)
        disp_sgbm = cv.normalize(disp_sgbm, 0, 255, cv.NORM_MINMAX)

        maps_list.append((
            disp_sgbm,
            rm[4]
        ))

    return maps_list


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


def bm_params(num_disp: int, block_size: int) -> BMParams:
    '''
    Construct a new BMParams typed dict.
    '''
    p: BMParams = {
        'numDisparities': num_disp,
        'blockSize': block_size,
    }
    return p
