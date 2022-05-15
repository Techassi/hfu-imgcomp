import numpy as np
import cv2 as cv
import click

import geometry.geometry as geometry
import features.features as features
import utils.input as inp


def single(
    base_path: str,
    preview: bool,
    speckle_size: int,
    speckle_range: int,
    min_disp: int,
    num_disp: int,
    disp_diff: int,
    unique_ratio: int,
    block_size: int
):
    imgs = inp.handle_images(base_path, preview)

    # Construct stereo params
    params = geometry.sgbm_params(
        speckle_size,
        speckle_range,
        min_disp,
        num_disp,
        disp_diff,
        unique_ratio,
        block_size
    )

    click.echo('\nExtracting fundamental matrices. This takes a few seconds...\n')
    fm_list = features.get_fundamental_matrices(imgs)

    click.echo('Rectifying...')
    rm_list = geometry.rectify(imgs, fm_list)

    click.echo('Computing depth maps...')
    dm_list = geometry.depth_maps_single(imgs, rm_list, params)

    for dm in dm_list:
        cv.namedWindow('disparity', cv.WINDOW_NORMAL)
        cv.imshow('disparity', dm[0])
        cv.waitKey(0)


def multi(
    base_path: str,
    preview: bool,
    speckle_size: int,
    speckle_range: int,
    min_disp: int,
    num_disp: int,
    disp_diff: int,
    unique_ratio: int,
    block_size: int
):
    imgs = inp.handle_images(base_path, preview)

    # Construct stereo params
    sgbm_params = geometry.sgbm_params(
        speckle_size,
        speckle_range,
        min_disp,
        num_disp,
        disp_diff,
        unique_ratio,
        block_size
    )

    bm_params = geometry.bm_params(num_disp, block_size)

    click.echo('\nExtracting fundamental matrices. This takes a few seconds...\n')
    fm_list = features.get_fundamental_matrices(imgs)

    click.echo('Rectifying...')
    rm_list = geometry.rectify(imgs, fm_list)

    click.echo('Computing and combining depth maps...')
    dm_list = geometry.depth_maps_multi(imgs, rm_list, bm_params, sgbm_params)

    for dm in dm_list:
        cv.namedWindow('disparity', cv.WINDOW_NORMAL)
        cv.imshow('disparity', dm[0])
        cv.waitKey(0)
