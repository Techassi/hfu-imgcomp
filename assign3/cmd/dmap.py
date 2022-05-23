import cv2 as cv
import click

import geometry.rectification as grect
import geometry.dmaps as gdmaps

import features.features as features
import utils.images as images
import utils.input as inp


def normal(
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
    imgs, combi_mode, ref_index = inp.handle_images(base_path, preview)
    combis = images.get_combinations(imgs, combi_mode, ref_index)

    # Construct stereo params
    params = gdmaps.sgbm_params(
        speckle_size,
        speckle_range,
        min_disp,
        num_disp,
        disp_diff,
        unique_ratio,
        block_size
    )

    click.echo('\nExtracting fundamental matrices. This takes a few seconds...')
    fm_list = features.get_fundamental_matrices(imgs, combis)

    click.echo('Rectifying...')
    rm_list = grect.rectify(imgs, fm_list)

    click.echo('Computing depth maps...\n')
    dm_list = gdmaps.depth_maps(imgs, rm_list, params)

    for dm in dm_list:
        click.echo('Showing combination of image {} with image {}'.format(
            dm[1][0] + 1,
            dm[1][1] + 1,
        ))

        cv.namedWindow('disparity', cv.WINDOW_NORMAL)
        cv.imshow('disparity', dm[0])
        cv.waitKey(0)


def combine(
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
    imgs, combi_mode, ref_index = inp.handle_images(base_path, preview)
    combis = images.get_combinations(imgs, combi_mode, ref_index)

    # Construct stereo params
    params = gdmaps.sgbm_params(
        speckle_size,
        speckle_range,
        min_disp,
        num_disp,
        disp_diff,
        unique_ratio,
        block_size
    )

    click.echo('\nExtracting fundamental matrices. This takes a few seconds...')
    fm_list = features.get_fundamental_matrices(imgs, combis)

    click.echo('Rectifying...')
    rm_list = grect.rectify(imgs, fm_list)

    click.echo('Computing depth maps...')
    dm_list = gdmaps.depth_maps(imgs, rm_list, params)

    click.echo('Combining depth maps...')
    dm = gdmaps.combine_maps(dm_list)

    cv.namedWindow('disparity', cv.WINDOW_NORMAL)
    cv.imshow('disparity', dm)
    cv.waitKey(0)
